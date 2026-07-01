# LLMOps Observability Pipeline with LangSmith

A simple project demonstrating core LLMOps concepts: tracing, evaluation, and monitoring an LLM app using LangSmith.

## What This Does

- Runs an LLM chain (LangChain + OpenAI) that automatically logs every call to LangSmith
- Creates a golden evaluation dataset
- Runs automated evaluations against that dataset and scores the results

## Project Structure

```
llmops-langsmith-demo/
├── .env                    # API keys (never commit this)
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── chain.py             # The LLM chain being traced
│   ├── config.py            # LangSmith + model config, loads .env
│   └── run.py                # Entry point to run queries
├── evaluation/
│   ├── dataset.py            # Creates eval dataset in LangSmith
│   └── evaluate.py           # Runs evaluations against the dataset
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
Runs the chain against every example in the dataset and scores it with a keyword-match evaluator.

**Run tests**
```bash
pytest tests/
```

## Viewing Results

Go to [smith.langchain.com](https://smith.langchain.com) and open your project (`llmops-demo`):

- **Traces tab** — every LLM call, latency, token usage, cost
- **Datasets & Testing** — your eval set and experiment run scores

## Troubleshooting

**`401 Unauthorized: Invalid token`**
- Make sure `src/config.py` (which loads `.env`) is imported *before* creating a `Client()` in any script.
- Regenerate your API key if it's old — use a Personal Access Token, not a Service Key.

**Traces not showing up**
- Confirm `LANGCHAIN_TRACING_V2=true` is set.
- Traces can take a few seconds to appear in the dashboard.

## Notes

- Free LangSmith Developer plan: 5,000 traces/month, 14-day retention — more than enough for this project.
- Each evaluation run also counts as traces.