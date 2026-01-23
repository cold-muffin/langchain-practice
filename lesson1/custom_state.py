from dotenv import load_dotenv
from dataclasses import dataclass
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()

llm = AzureChatOpenAI(
  model="internyl-api-backend-grok-3-mini",
  api_version="2024-05-01-preview",
  temperature=1.0,
  timeout=60,
  max_retries=2,
  max_completion_tokens=10000
)

# Unpersisted agent state, not saved by the checkpointer (request time variable)
@dataclass
class Context:
  user_id: int

# Persisted agent state, saved by checkpointer
@dataclass
class CustomState(AgentState):
  name: str
  misc_info: str

@tool
def get_name_from_id(runtime: ToolRuntime[Context]) -> str:
  "Get the name of the user from their ID"
  match runtime.context.user_id:
    case 0:
      return "Bob"
    case 1:
      return "Hobb"
    case 2:
      return "Job"
    case 99:
      return "Qwob"
    case _:
      return "USER ID NOT FOUND"

# The memory can't actually remember the conversation. But the `Command` class and `ToolMessage`
# is saved to the state so the model thinks it's remembering conversation history
# If the model called a tool, it can remember the prompt that caused the tool call.
@tool
def remember_name(name: str, runtime: ToolRuntime) -> Command:
  "Update the state to reflect the user's name"
  return Command(
    update={
      "name": name,
      "messages": [ToolMessage(content="Succesfully updated name", tool_call_id=runtime.tool_call_id)]
    }
  )

@tool
def remember_misc_info(misc_info: str, runtime: ToolRuntime) -> Command:
  "Update the state to reflect any misc. info about the user"
  return Command(
    update={
      "misc_info": misc_info,
      "messages": [ToolMessage(content="Succesfully updated misc. info", tool_call_id=runtime.tool_call_id)]
    }
  )

@tool
def return_user_info(runtime: ToolRuntime) -> str:
  "Returns all remembered information about the user"
  return str(runtime.state)

agent = create_agent(
  model=llm,
  tools=[remember_name, remember_misc_info, return_user_info],
  checkpointer=InMemorySaver(),
  #context_schema=Context,
  state_schema=CustomState,
  system_prompt="You are a competitor for the Memory-Star competition. You are being trained by the user who will talk to you about information that you are tasked to remember."
)

inp = input("> ")
while inp != "quit":
  for chunk in agent.stream(
    {
      "messages": [
        HumanMessage(content=inp)
      ],
    },
    {
      "configurable": {
        "thread_id": 1
      }
    },
    context=Context(user_id=99),
  ):
    try:
      print(chunk["model"]["messages"][-1].content, end="\n---\n")
    except Exception as e:
      print(chunk, end="\n---\n")
  inp = input("> ")