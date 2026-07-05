# LLMOps Observability Pipeline with LangSmith

A simple project demonstrating core LLMOps concepts: tracing, evaluation, and monitoring an LLM app using LangSmith.

## What This Does

- Runs an LLM chain (LangChain + OpenAI) that automatically logs every call to LangSmith
- Creates a golden evaluation dataset
- Runs automated evaluations against that dataset using two evaluators:
  - **Keyword match** — simple heuristic check
  - **LLM-as-judge** — uses `gpt-4o-mini` to judge whether the answer conveys the expected concept

## Project Structure

```
llmops-langsmith-demo/
├── .env                    # API keys (never commit this)
├── requirements.txt
├── pytest.ini               # Fixes module resolution for tests
├── src/
│   ├── __init__.py
│   ├── chain.py             # The LLM chain being traced
│   ├── config.py            # LangSmith + model config, loads .env
│   └── run.py                # Entry point to run queries
├── evaluation/
│   ├── dataset.py            # Creates eval dataset in LangSmith
│   └── evaluate.py           # Runs evaluations: keyword match + LLM-as-judge
├── tests/
│   └── test_chain.py
└── README.md
```

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Create your `.env` file**
```
OPENAI_API_KEY=your_openai_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your_langsmith_key_here
LANGCHAIN_PROJECT=llmops-demo
```

Get your LangSmith API key from smith.langchain.com → Settings → API Keys.

## Usage

**Run a traced query**
```bash
python -m src.run
```
Logs a single LLM call to LangSmith automatically.

**Create the evaluation dataset**
```bash
python -m evaluation.dataset
```
Creates `llmops-demo-eval-set` in LangSmith (skips if it already exists).

**Run evaluation**
```bash
python -m evaluation.evaluate
```
Runs the chain against every example in the dataset and scores each response with:
- `keyword_match` — 1 if expected keyword is present, else 0
- `llm_judge` — 1 if an LLM judges the answer as conceptually correct, else 0

**Run tests**
```bash
pytest tests/
```

## Viewing Results

Go to [smith.langchain.com](https://smith.langchain.com) and open your project (`llmops-demo`):

- **Traces tab** — every LLM call, latency, token usage, cost
- **Datasets & Testing** — your eval set, experiment runs, and both evaluator scores side-by-side

## Troubleshooting

**`401 Unauthorized: Invalid token`**
- Make sure `src/config.py` (which loads `.env`) is imported *before* creating a `Client()` in any script.
- Regenerate your API key if it's old — use a Personal Access Token, not a Service Key.

**Traces not showing up**
- Confirm `LANGCHAIN_TRACING_V2=true` is set.
- Traces can take a few seconds to appear in the dashboard.

**`ModuleNotFoundError: No module named 'src'` when running pytest**
- Make sure `pytest.ini` exists at the project root with:
  ```
  [pytest]
  pythonpath = .
  ```
- Make sure `src/__init__.py` exists.

## Notes

- Free LangSmith Developer plan: 5,000 traces/month, 14-day retention — more than enough for this project.
- Each evaluation run counts as traces, and the LLM-as-judge evaluator makes an extra OpenAI call per example (roughly doubles API cost per eval run).