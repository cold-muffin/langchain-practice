from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()

# OPENAI_API_KEY is automatically found
# for both `init_chat_model`
# and `ChatOpenAI`
llm = init_chat_model(
  model="xiaomi/mimo-v2-flash:free",
  model_provider="openai",
  base_url="https://openrouter.ai/api/v1"
)

for chunk in llm.stream("Tell me an interesting poem."):
  print(chunk.text, end='', flush=True)