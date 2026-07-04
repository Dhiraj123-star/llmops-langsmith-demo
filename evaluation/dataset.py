import src.config
from langsmith import Client

client = Client()
DATASET_NAME = "llmops-demo-eval-set"

examples = [
    {"question": "What is blue-green deployment?", "expected": "involves two environments"},
    {"question": "What is canary deployment?", "expected": "gradual rollout to subset"},
    {"question": "What is a rolling deployment?", "expected": "gradual replacement of instances"},
]

def create_dataset():
    if client.has_dataset(dataset_name=DATASET_NAME):
        print("Dataset already exists.")
        return client.read_dataset(dataset_name=DATASET_NAME)

    dataset = client.create_dataset(dataset_name=DATASET_NAME)
    for ex in examples:
        client.create_example(
            inputs={"question": ex["question"]},
            outputs={"expected": ex["expected"]},
            dataset_id=dataset.id,
        )
    print(f"Created dataset '{DATASET_NAME}' with {len(examples)} examples.")
    return dataset

if __name__ == "__main__":
    create_dataset()