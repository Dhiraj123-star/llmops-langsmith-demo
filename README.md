# LLMOps Observability Pipeline with LangSmith

A simple project demonstrating core LLMOps concepts: tracing, evaluation, prompt versioning, and containerized deployment using LangSmith and Docker.

## What This Does

- Runs an LLM chain (LangChain + OpenAI) that automatically logs every call to LangSmith
- Pulls its system prompt from LangSmith Prompt Hub (versioned, not hardcoded)
- Creates a golden evaluation dataset
- Runs automated evaluations against that dataset using two evaluators:
  - **Keyword match** — simple heuristic check
  - **LLM-as-judge** — uses `gpt-4o-mini` to judge whether the answer conveys the expected concept
- Fully containerized with Docker for consistent, portable runs

## Project Structure

```
llmops-langsmith-demo/
├── .env                    # API keys (never commit this)
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini               # Fixes module resolution for tests
├── src/
│   ├── __init__.py
│   ├── chain.py             # LLM chain — pulls prompt from LangSmith Hub
│   ├── config.py            # LangSmith + model config, loads .env
│   └── run.py                # Entry point to run queries
├── prompts/
│   └── push_prompt.py        # Pushes/updates prompt versions to LangSmith Hub
├── evaluation/
│   ├── dataset.py            # Creates eval dataset in LangSmith
│   └── evaluate.py           # Runs evaluations: keyword match + LLM-as-judge
├── tests/
│   └── test_chain.py
└── README.md
```

## Setup

**1. Install dependencies (local, non-Docker)**
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

**3. Push the initial prompt to LangSmith Hub (one-time)**
```bash
python -m prompts.push_prompt
```

## Usage — Local (venv)

**Run a traced query**
```bash
python -m src.run
```

**Create the evaluation dataset**
```bash
python -m evaluation.dataset
```

**Run evaluation**
```bash
python -m evaluation.evaluate
```
Scores each response with:
- `keyword_match` — 1 if expected keyword is present, else 0
- `llm_judge` — 1 if an LLM judges the answer as conceptually correct, else 0

**Run tests**
```bash
pytest tests/
```

## Usage — Docker

**Build and run a traced query**
```bash
docker compose run --rm app
```

**Run evaluations**
```bash
docker compose run --rm eval
```

**Run tests**
```bash
docker compose run --rm test
```

All Docker services read config from your local `.env` file automatically.

**Manual build/run without compose:**
```bash
docker build -t llmops-demo .
docker run --rm --env-file .env llmops-demo
```

## Updating the Prompt (creates a new version)

1. Edit the prompt text in `prompts/push_prompt.py`
2. Run:
   ```bash
   python -m prompts.push_prompt
   ```
3. Next run of `src.run` or `evaluation.evaluate` (local or Docker) automatically uses the new version — no code change needed elsewhere.

## Viewing Results

Go to [smith.langchain.com](https://smith.langchain.com):

- **Traces tab** — every LLM call, latency, token usage, cost
- **Prompts tab** — version history and diffs for `llmops-demo-system-prompt`
- **Datasets & Testing** — your eval set, experiment runs, and both evaluator scores side-by-side

## Troubleshooting

**`401 Unauthorized: Invalid token`**
- Make sure `src/config.py` (which loads `.env`) is imported *before* creating a `Client()` in any script.
- Regenerate your API key if it's old — use a Personal Access Token, not a Service Key.

**Traces not showing up**
- Confirm `LANGCHAIN_TRACING_V2=true` is set.
- Traces can take a few seconds to appear in the dashboard.

**`ModuleNotFoundError: No module named 'src'` when running pytest**
- Make sure `pytest.ini` exists at the project root with `pythonpath = .`
- Make sure `src/__init__.py` exists.

**Prompt pull fails**
- Make sure you ran `python -m prompts.push_prompt` at least once before running `src.run` or evaluations.

**Docker container can't authenticate**
- Confirm `.env` exists in the project root — `docker-compose.yml` loads it via `env_file`.

## Notes

- Free LangSmith Developer plan: 5,000 traces/month, 14-day retention — more than enough for this project.
- Each evaluation run counts as traces, and the LLM-as-judge evaluator makes an extra OpenAI call per example (roughly doubles API cost per eval run).
- Prompt versions are managed in LangSmith Hub, not in code — always check the Prompts tab to see what's currently live.