from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langsmith import Client
from src.config import MODEL_NAME

PROMPT_NAME = "llmops-demo-system-prompt"

client = Client()

def build_chain():
    # Pulls the latest version of the prompt from LangSmith Prompt Hub
    prompt = client.pull_prompt(PROMPT_NAME)
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0.3)
    return prompt | llm | StrOutputParser()

chain = build_chain()