from dotenv import load_dotenv
from typing import Any
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from tavily import TavilyClient

load_dotenv()
tavily_client = TavilyClient()

llm = AzureChatOpenAI(
  model="internyl-api-backend-grok-3-mini",
  api_version="2024-05-01-preview",
  temperature=0,
  timeout=60,
  max_retries=2
)

@tool
def web_search(query: str) -> dict[str, Any]:
  "Search the web for up-to-date information"
  return tavily_client.search(query)

agent = create_agent(
  model=llm,
  tools=[web_search],
  system_prompt="You are a helpful web searching agent to help the user complete his research tasks."
)

for chunk in agent.stream(
    {
      "messages": [
        HumanMessage(content="Who is the current mayor of NYC?")
      ]
    }
  ):
  print(chunk)
  print("----------")