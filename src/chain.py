from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config import MODEL_NAME

def build_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a concise assistant that explains technical concepts simply."),
        ("user", "{question}")
    ])
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0.3)
    return prompt | llm | StrOutputParser()

chain = build_chain()