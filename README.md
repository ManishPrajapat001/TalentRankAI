# TalentRankAI

TalentRankAI is a modular AI hiring agent built using Python, LangGraph, OpenRouter, ChromaDB, sentence-transformers, and MCP (Model Context Protocol). It acts as a recruiter assistant capable of parsing job descriptions, extracting requirements, retrieving resumes using RAG, ranking candidates, explaining hiring decisions, comparing applicants, and generating interview questions.

The project was initially built as a LangGraph-based hiring agent and later refactored to use an MCP-based filesystem architecture with JSON-RPC 2.0 communication.

---

# Features

## AI Hiring Agent

- Job description parsing
- Requirement extraction
- Resume retrieval using RAG
- Hybrid candidate ranking
- Explainable hiring recommendations
- Candidate comparison
- Interview question generation
- Conversational recruiter workflow

---

## MCP-Based Filesystem Architecture

- JSON-RPC 2.0 compliant MCP server
- Filesystem MCP client abstraction
- Resource discovery
- Directory monitoring using watch_directory()
- Batch processing using batch_process()
- Standardized filesystem access through MCP resources

---

## Retrieval-Augmented Generation (RAG)

- Resume loading
- Text chunking
- Sentence-transformer embeddings
- ChromaDB vector search
- Semantic candidate retrieval

---

## Hybrid Ranking Engine

Candidate ranking combines:

- Skill Match → 40%
- Experience Match → 30%
- Semantic Similarity → 20%
- Nice-to-Have Bonus → 10%

Additional features:

- Missing skill penalties
- Explainable strengths and gaps
- Strong Hire / Hire / Borderline / Reject recommendations

---

## Conversational Recruiter Workflow

Supported recruiter queries:

- Find React developers with AWS experience
- Only consider candidates with Docker
- Compare top 3 candidates
- Why did candidate A rank higher than candidate B?
- Generate interview questions

---

# Architecture

text app/  agent/      LangGraph workflow, state management, recruiter interface mcp/        MCP server, MCP client, JSON-RPC models, resource registry rag/        Resume loading, chunking, embeddings, retrieval ranking/    Hybrid scoring, reranking, explainability tools/      Requirement extraction, comparisons, interview generation prompts/    Prompt templates utils/      Configuration, OpenRouter wrapper, helpers 

---

# MCP Architecture

The project uses MCP (Model Context Protocol) to standardize filesystem access.

Instead of directly accessing resume files, the hiring agent communicates through a Filesystem MCP Client which interacts with a Filesystem MCP Server using JSON-RPC 2.0.

## MCP Components

- FilesystemMCPServer
- FilesystemMCPClient
- Resource Registry
- JSON-RPC Request/Response Models
- Resource Discovery
- watch_directory()
- batch_process()

---

## Agent ↔ MCP Interaction

mermaid graph TD      A[Recruiter Query]     --> B[MatchingAgent]      B --> C[Filesystem MCP Client]      C --> D[Filesystem MCP Server]      D --> E[Resume Resources]      E --> F[RAG Retrieval]      F --> G[Hybrid Ranking]      G --> H[Explainability]      H --> I[Final Report] 

---

## MCP Resource Discovery

The Filesystem MCP Server exposes:

text list_resumes load_resume load_all_resumes  list_jds load_jd load_all_jds  watch_directory batch_process 

---

# LangGraph Workflow

mermaid graph LR      A[START]     --> B[Parse JD]     --> C[Extract Requirements]     --> D[Search Resumes]     --> E[Rank Candidates]     --> F[Generate Report]     --> G{Feedback?}      G -->|Yes| C     G -->|No| H[END] 

---

# Hybrid Ranking Pipeline

mermaid graph TD      A[Retrieved Candidates]     --> B[Skill Match Score]      A --> C[Experience Match Score]      A --> D[Semantic Similarity Score]      A --> E[Nice-to-Have Bonus]      B --> F[Weighted Final Score]     C --> F     D --> F     E --> F      F --> G[Explainability Engine]      G --> H[Strong Hire]     G --> I[Hire]     G --> J[Borderline]     G --> K[Reject] 

---

# Retrieval-Augmented Generation (RAG) Pipeline

mermaid graph TD      A[PDF/TXT Resumes]     --> B[Resume Loader]      B --> C[Text Chunking]      C --> D[Sentence Transformers Embeddings]      D --> E[ChromaDB Vector Store]      F[Recruiter Query]     --> G[Semantic Search]      G --> E      E --> H[Relevant Resume Chunks]      H --> I[Candidate Profile Extraction]      I --> J[Candidate Ranking] 

---

# Example Conversational Flow

mermaid sequenceDiagram      participant Recruiter     participant CLI     participant Agent     participant Retriever     participant Ranking      Recruiter->>CLI: Find React developers with AWS     CLI->>Agent: recruiter query     Agent->>Retriever: semantic candidate search     Retriever-->>Agent: retrieved candidates     Agent->>Ranking: rerank candidates     Ranking-->>Agent: ranked candidates     Agent-->>CLI: final report      Recruiter->>CLI: Only consider candidates with Docker     CLI->>Agent: refinement query     Agent->>Ranking: rerank with updated requirements     Ranking-->>Agent: updated ranking     Agent-->>CLI: refined report 

---

# Setup

## 1. Create Virtual Environment

bash python -m venv .venv source .venv/bin/activate 

---

## 2. Install Dependencies

bash pip install -r requirements.txt 

---

## 3. Configure OpenRouter

bash cp .env.example .env 

Configure:

text OPENROUTER_API_KEY=your_openrouter_api_key_here OPENROUTER_MODEL=openai/gpt-4o-mini 

---

## 4. Generate Sample Data

bash python scripts/generate_resumes.py python scripts/generate_jds.py 

This creates synthetic resumes and job descriptions for testing.

---

# Integration Testing

## MCP Validation

bash python tests/test_mcp_server.py python tests/test_mcp_client.py 

Validates:

- Resource discovery
- Resume loading
- Batch processing
- Directory monitoring
- MCP client/server interaction

---

## Hiring Agent Validation

bash python tests/test_loader.py python tests/test_extraction.py python tests/test_indexing.py python tests/test_retrieval.py python tests/test_ranking.py python tests/test_agent.py 

Validates:

- Resume loading
- Requirement extraction
- Vector indexing
- Retrieval pipeline
- Hybrid ranking
- LangGraph workflow

---

# Run

From project root:

bash python cli.py 

---

## Example Search

text Recruiter: Find React developers with AWS and 3 years experience 

Example response:

text 1. John Doe - score 0.82 - Strong Hire    Strengths: Matches required skills: React, AWS    Gaps: No major gaps detected 

---

## Example Refinement

text Recruiter: Only consider candidates with Docker 

The agent dynamically reranks candidates using updated requirements.

---

## Example Comparison

text Recruiter: Compare top 3 candidates 

---

## Example Explainability

text Recruiter: Why did John rank higher than Jane? 

---

## Example Interview Questions

text Recruiter: Generate interview questions 

---

# MCP Features Demonstrated

## Resource Discovery

text discover_resources() 

Returns all available MCP resources.

---

## Batch Processing

text batch_process(paths) 

Processes multiple resumes and returns:

json {   "processed": 10,   "successful": 10,   "failed": 0 } 

---

## Directory Monitoring

text watch_directory() 

Detects newly added resumes.

---

# Technologies Used

- Python
- LangGraph
- MCP (Model Context Protocol)
- JSON-RPC 2.0
- OpenRouter
- ChromaDB
- sentence-transformers
- pypdf
- OpenAI SDK
- RAG (Retrieval-Augmented Generation)
- Hybrid Ranking Architecture

---

# Assignment Coverage

## Part A – MCP Server Implementation

- MCP-based filesystem server
- JSON-RPC 2.0 compliance
- Resource discovery
- watch_directory()
- batch_process()
- Configuration management
- Error handling

---

## Part B – Agent Refactoring

- Filesystem MCP Client integration
- Removal of direct filesystem access from agent layer
- Existing functionality preserved

---

## Part C – End-to-End Workflow

- LangGraph orchestration
- RAG retrieval
- Hybrid ranking
- Explainability
- Conversational recruiter workflow

---

# Demo Coverage

The demo video demonstrates:

1. MCP server startup
2. Resource discovery
3. Resume loading through MCP
4. Batch processing
5. Directory monitoring
6. Candidate retrieval
7. Candidate reranking
8. Candidate comparison
9. Interview question generation
10. End-to-end recruiter workflow

---

# Notes

- If OPENROUTER_API_KEY is unavailable, the system falls back to heuristic requirement extraction.
- The first embedding run may download the sentence-transformers model.
- MCP is implemented using JSON-RPC 2.0 request/response models.
- The project intentionally focuses on agent architecture and MCP integration rather than authentication, deployment, or microservices.
