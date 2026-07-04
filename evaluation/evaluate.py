from langsmith.evaluation import evaluate
from src.chain import chain
from evaluation.dataset import DATASET_NAME

def target(inputs: dict) -> dict:
    result = chain.invoke({"question": inputs["question"]})
    return {"answer": result}

def keyword_match(run, example) -> dict:
    """Simple custom evaluator: checks if expected keyword appears in the answer."""
    expected = example.outputs.get("expected", "").lower()
    actual = run.outputs.get("answer", "").lower()
    score = 1 if expected in actual else 0
    return {"key": "keyword_match", "score": score}

if __name__ == "__main__":
    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[keyword_match],
        experiment_prefix="llmops-demo-eval",
    )
    print("Evaluation complete. View results in LangSmith dashboard.")