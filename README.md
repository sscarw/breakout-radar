# 📡 Breakout Radar

![Python](https://img.shields.io/badge/Python-3.13-blue)
![OpenAI Agents SDK](https://img.shields.io/badge/OpenAI-Agents_SDK-green)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![RAG](https://img.shields.io/badge/RAG-Semantic_Search-orange)

**Breakout Radar** is a multi-agent AI system that discovers small, fast-growing open-source projects before they become mainstream.

It combines GitHub repository metrics, developer discussions, vector search, and AI agents to detect early breakout signals — and explains *why* a project may be worth watching. Instead of ranking by raw star count, it looks for **acceleration**: repositories that are starting to gain momentum.

---

## What it does

- Converts a natural-language request into an optimized GitHub and discussion search plan
- Finds promising open-source repositories using the GitHub Search API
- Stores repositories, scan runs, and dated metric snapshots in PostgreSQL
- Tracks repository growth over time using a **momentum score**
- Collects developer discussions from Hacker News
- Stores discussion embeddings in Qdrant for **semantic search (RAG)**
- Uses AI agents to analyze projects by metrics, momentum, sentiment, and growth status
- Produces a ranked, human-readable Markdown report explaining which projects look most promising and why

---

## Architecture

Breakout Radar is built around **three AI agents** and a deterministic data pipeline.

### Agents

| Agent | Responsibility | Output |
|---|---|---|
| **Query Planner** | Converts the user request into a GitHub search query and a discussion search query | `SearchPlan` |
| **Analyst** | Analyzes one repository using metrics, momentum, and semantic discussion search | `ProjectAnalysis` |
| **Report Writer** | Ranks analyzed projects and generates the final human-readable report | `FinalReport` |

### Data sources & storage

| Component | Purpose |
|---|---|
| **GitHub API** | Repository discovery and live metrics |
| **Hacker News API** | Developer discussion signals |
| **PostgreSQL** | Repositories, scan runs, and time-series metrics |
| **Qdrant** | Vector storage for semantic search over discussions |

### Data flow

```text
User query
   │
   ▼
[Query Planner Agent]
   │
   ├──► GitHub query
   │        │
   │        ▼
   │   GitHub Search API
   │        │
   │        ▼
   │   Repositories ───────────────► PostgreSQL
   │        │                           │
   │        ▼                           ▼
   │   GitHub Metrics API          Metrics history
   │        │                           │
   │        ▼                           ▼
   │   Dated metrics snapshot      Momentum score (function)
   │
   ├──► Discussion query
   │        │
   │        ▼
   │   Hacker News API
   │        │
   │        ▼
   │   Discussion embeddings ─────► Qdrant
   │
   ▼
[Analyst Agent]  (per repository)
   │
   ├── repository metrics (tool)
   ├── precomputed momentum score
   └── semantic discussion search (tool)
   │
   ▼
ProjectAnalysis[]
   │
   ▼
[Report Writer Agent]
   │
   ▼
Final Markdown Report
```

### Design principle

Breakout Radar deliberately separates deterministic logic from AI reasoning:

- **Functions** handle API calls, database writes, embeddings, and momentum scoring.
- **AI agents** handle query planning, qualitative analysis, ranking, and explanation.
- The momentum score is computed by code and passed *into* the Analyst agent, so the model never invents numeric growth values.

---

## Tech Stack

- **Python 3.13**
- **OpenAI Agents SDK** — multi-agent orchestration
- **OpenAI API** — LLM reasoning and embeddings (`text-embedding-3-small`, 1536-dim)
- **PostgreSQL** (`psycopg3`) — repository data, scan history, and metric snapshots
- **Qdrant** — vector database for semantic search
- **httpx** — async API clients
- **Pydantic** — structured data validation
- **Docker Compose** — local infrastructure
- **python-dotenv** — environment variable management

---

## How it works

1. The user describes what kind of open-source projects they want to discover, e.g.:

   ```text
   underrated AI agent frameworks with growth potential
   ```

2. The **Query Planner** generates a GitHub search query and a Hacker News discussion query.
3. Hacker News discussions are fetched, embedded, and stored in Qdrant.
4. GitHub repositories are fetched and stored in PostgreSQL with a dated metrics snapshot.
5. A momentum score is calculated from historical metric snapshots.
6. The **Analyst** agent analyzes each repository (metrics + momentum + semantic discussion search → sentiment and growth status).
7. The **Report Writer** ranks the analyzed projects and generates a Markdown report.

### Momentum note

Momentum is based on metric history over time. On the first run, most projects will have a momentum score of `0.0` because only one snapshot exists. Real growth signals emerge after repeated scans across multiple days, as history accumulates.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/sscarw/breakout-radar.git
cd breakout-radar
```

### 2. Start infrastructure

```bash
docker compose up -d
```

This starts:

- PostgreSQL on `localhost:5432`
- Qdrant on `localhost:6333`

### 3. Create `.env`

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here

POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=breakout-radar
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

QDRANT_URL=http://localhost:6333
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply the database schema

```bash
psql -h localhost -U your_postgres_user -d breakout-radar -f schema.sql
```

Or run `schema.sql` through your database tool.

### 6. Run the app

```bash
python main.py
```

You will be prompted for a search topic:

```text
Describe the projects you're looking for: underrated AI agent frameworks with growth potential
```

---

## Example output

```markdown
# 📡 Breakout Radar Report

**Query:** underrated AI agent frameworks with growth potential

## Summary

The analyzed projects show historical interest (stars and forks) but limited new
momentum, because only one metrics snapshot is currently available. Growth signals
become meaningful as more daily snapshots accumulate.

---

## 1. neuron-core/neuron-ai

- Momentum: 0.00
- Sentiment: neutral
- Growth status: stable

Verdict: Moderate interest and reasonable positioning in the AI agent ecosystem,
but current breakout evidence is limited.

Growth signals:

- Moderate historical GitHub stars and forks
- Relevant positioning in the AI agent ecosystem
- No strong negative sentiment detected
- Momentum history is still too short for reliable growth analysis
```

---

## Project structure

```text
breakout-radar/
├── main.py              # Pipeline orchestration
├── pipeline.py          # Agent definitions (Query Planner, Analyst, Report Writer)
├── agent_tools.py       # Function tools exposed to the Analyst agent
├── models.py            # Pydantic models (data + agent outputs)
├── github_client.py     # GitHub API client
├── hn_client.py         # Hacker News API client
├── vector_store.py      # Qdrant client + semantic search
├── embeddings.py        # OpenAI embeddings
├── db.py                # PostgreSQL access (psycopg3)
├── scoring.py           # Momentum score (deterministic)
├── report_formatter.py  # FinalReport → readable Markdown
├── schema.sql           # Database schema
└── docker-compose.yml   # PostgreSQL + Qdrant
```
