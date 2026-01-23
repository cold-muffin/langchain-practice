from pydantic import SecretStr
from dotenv import load_dotenv
from os import getenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()
api_key = getenv("OPENAI_API_KEY")
if not api_key:
  raise ValueError("No API key found!")

llm = ChatOpenAI(
  model="xiaomi/mimo-v2-flash:free",
  api_key=SecretStr(api_key),
  base_url="https://openrouter.ai/api/v1",
  temperature=0
)
# `llm.invoke()` -> `AIMessage(content: str)`
# llm.invoke("Say hi I invoked this request using LangChain.").pretty_print()

# You can also invoke models using ChatPromptTemplates
# This has many benefits:
# 1. Structure
# 2. System roles
# 3. Enforcement
# -  Of output

# CPT initilization with template
prompt = ChatPromptTemplate.from_template(
  template="Tell me what this partial variable says: {partial_var}"
)
print(prompt.input_variables)
formatted_prompt = prompt.format_messages(partial_var="leprechaun")
# .to_messages() isn't required since LangChain automatically converts ``
# llm.invoke(formatted_prompt).pretty_print()

# CPT initialization with tuples
prompt = ChatPromptTemplate(
  [
    ("system", "It is opposite day. That means \
    that whatever you want to say, you will say \
    the opposite of. (Eg. grass isn't green)"),
    ("human", "What year is it?")
  ]
)
formatted_prompt = prompt.format_messages()
# llm.invoke(formatted_prompt).pretty_print()

# CPT initialization with `BaseMessage`s
prompt = ChatPromptTemplate(
  [
    SystemMessage(content="You are a very empathetic and nice AI bot."),
    HumanMessage(content="I got a new cat today and its name is Hobb."),
    AIMessage(content="What a stupid name for a cat. I don't even want to talk to you anymore."),
    HumanMessage(content="{response}")
  ]
)
formatted_prompt = prompt.format_messages(response="How rude!")
llm.invoke(formatted_prompt).pretty_print()