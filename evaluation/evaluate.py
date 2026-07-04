from langchain_openai import ChatOpenAI
from langsmith.evaluation import evaluate
from src.chain import chain
from evaluation.dataset import DATASET_NAME

# --- Target function (what gets evaluated) ---

def target(inputs: dict) -> dict:
    result = chain.invoke({"question": inputs["question"]})
    return {"answer": result}


# --- Evaluator 1: Keyword match (existing, simple heuristic) ---

def keyword_match(run, example) -> dict:
    """Checks if expected keyword appears in the answer."""
    expected = example.outputs.get("expected", "").lower()
    actual = run.outputs.get("answer", "").lower()
    score = 1 if expected in actual else 0
    return {"key": "keyword_match", "score": score}


# --- Evaluator 2: LLM-as-judge (new) ---

judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

JUDGE_PROMPT = """You are grading an AI assistant's answer for correctness.

Question: {question}
Expected concept: {expected}
Actual answer: {actual}

Does the actual answer correctly convey the expected concept?
Respond with ONLY one word: "correct" or "incorrect"."""


def llm_judge(run, example) -> dict:
    """Uses an LLM to judge whether the answer conveys the expected concept."""
    question = example.inputs.get("question", "")
    expected = example.outputs.get("expected", "")
    actual = run.outputs.get("answer", "")

    prompt = JUDGE_PROMPT.format(question=question, expected=expected, actual=actual)
    verdict = judge_llm.invoke(prompt).content.strip().lower()

    score = 1 if "incorrect" not in verdict and "correct" in verdict else 0
    return {"key": "llm_judge", "score": score, "comment": verdict}


# --- Run evaluation with both evaluators ---

if __name__ == "__main__":
    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[keyword_match, llm_judge],
        experiment_prefix="llmops-demo-eval",
    )
    print("Evaluation complete. View results in LangSmith dashboard.")