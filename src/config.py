import os
from dotenv import load_dotenv

load_dotenv()

# LangSmith reads these env vars automatically once set — no extra code needed
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "llmops-demo")

MODEL_NAME = "gpt-4o-mini"