from src.chain import chain
import src.config  # ensures env vars are set before any LLM call

def ask(question: str) -> str:
    # This call is automatically traced to LangSmith
    return chain.invoke({"question": question})

if __name__ == "__main__":
    q = "What is a rolling deployment?"
    answer = ask(q)
    print(f"Q: {q}\nA: {answer}")