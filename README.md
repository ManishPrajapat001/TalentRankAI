# TalentRankAI

TalentRankAI is a modular AI hiring agent built with Python, LangGraph, OpenRouter, ChromaDB, sentence-transformers, and pypdf. It acts like a lightweight recruiter assistant: it parses job descriptions, extracts requirements, retrieves resumes with RAG, ranks candidates, explains the ranking, compares candidates, and generates interview questions.

## Features

- PDF resume loading from `data/resumes`
- Text chunking and sentence-transformers embeddings
- Persistent ChromaDB vector search
- LLM-based job requirement extraction through OpenRouter
- Hybrid scoring:
  - skill match: 40%
  - experience match: 30%
  - semantic similarity: 20%
  - nice-to-have bonus: 10%
- Missing skill penalties and readable explanations
- LangGraph workflow with a simple feedback refinement loop
- Conversational CLI intents:
  - search candidates
  - refine with constraints
  - compare top candidates
  - explain why one candidate ranked higher
  - generate interview questions

## Architecture

```text
app/
  agent/      LangGraph state, nodes, workflow, conversational wrapper
  rag/        PDF loading, chunking, embeddings, ChromaDB, retrieval
  ranking/    hybrid scoring, reranking, explainability
  tools/      requirement extraction, comparisons, question generation
  prompts/    prompt templates
  utils/      configuration, LLM wrapper, helpers
```

The LangGraph flow is:

## LangGraph Workflow

```mermaid
graph LR

    A[START]
    --> B[Parse JD]
    --> C[Extract Requirements]
    --> D[Search Resumes]
    --> E[Rank Candidates]
    --> F[Generate Report]
    --> G{Feedback?}

    G -->|Yes| C
    G -->|No| H[END]
```

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Configure OpenRouter.

```bash
cp .env.example .env
```

Set:

```text
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

4. Add PDF resumes to:

```text
data/resumes/
```

Or generate sample data:

```bash
python scripts/generate_test_data.py --clean
python scripts/smoke_test_data.py
```

This creates realistic fake PDF resumes in `data/resumes/` and job descriptions in `data/jds/`.

## Run

From the project directory:

```bash
python cli.py
```

Index resumes first:

```text
Recruiter: index
Agent: Indexed 24 resume chunks.
```

Then search:

```text
Recruiter: Find React developers with 3+ years experience
Agent: Ranked candidates:
1. John Doe - score 0.82 - Strong Hire
   Strengths: Matches required skills: React, Node.js; Meets or exceeds the experience requirement
   Gaps: Missing: AWS
```

Refine the search:

```text
Recruiter: Only consider candidates with AWS
```

Compare candidates:

```text
Recruiter: Compare top 3 candidates
```

Generate questions:

```text
Recruiter: Generate interview questions
```

## Notes

- If `OPENROUTER_API_KEY` is missing, extraction falls back to local heuristic parsing so the project remains runnable.
- The first embedding run may download the sentence-transformers model.
- This project intentionally avoids APIs, authentication, Docker, and microservices.
