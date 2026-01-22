import requests
from dataclasses import dataclass
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# xiaomi/mimo-v2-flash:free doesn't support tool_choice
llm = init_chat_model(
  model="mistralai/devstral-2512:free",
  model_provider="openai",
  base_url="https://openrouter.ai/api/v1"
)

@dataclass
class Context:
  user_id: str

@dataclass
class ResponseFormat:
  summary: str
  temp_c: float
  temp_f: float
  humidity: float

@tool("get_weather", description="Returns weather information for a given city.")
def get_weather(city: str) -> dict:
  response = requests.get(f"https://wttr.in/{city}?format=j1")
  return response.json()

# Runtimes are a form of dependency injection
# It keeps data private and keeps context specific
@tool("locate_user", description="Gets the user's location given an id.")
def locate_user(runtime: ToolRuntime[Context]) -> str:
  match runtime.context.user_id:
    case "000":
      return "nyc"
    case "001":
      return "san_francisco"
    case "002":
      return "los_vegas"
    case _:
      return "unknown"

checkpointer = InMemorySaver()

agent = create_agent(
  model=llm,
  tools=[get_weather, locate_user],
  system_prompt="You are a helpful weather bot that has access to information about weather around the world to help users.",
  context_schema=Context,
  response_format=ResponseFormat,
  checkpointer=checkpointer
)

config: RunnableConfig = {"configurable": {"thread_id": 1}}

response = agent.invoke({
  "messages": [
    {"role": "user", "content": "What is the weather like right now?"}
  ]},
  config=config,
  context=Context(user_id="000")
)

print(response["structured_response"].summary)
print(response["structured_response"].temp_f)