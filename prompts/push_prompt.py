"""
One-time (or occasional) script to push a prompt to LangSmith Prompt Hub.
Run this whenever you want to create a NEW version of the prompt.
"""

import src.config  # loads .env before anything else
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client

client = Client()

PROMPT_NAME = "llmops-demo-system-prompt"

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant that explains technical concepts simply."),
    ("user", "{question}")
])

if __name__ == "__main__":
    url = client.push_prompt(PROMPT_NAME, object=prompt)
    print(f"Prompt pushed to LangSmith Hub: {url}")