# Admissions Review Platform

Automates the first pass of university transfer-admission eligibility review: a transcript
is uploaded, extracted by Gemini, run through a multi-agent validation layer, checked against
rules an LLM parsed out of the admissions handbook, and verified against a course catalog —
producing a draft recommendation a human admissions officer reviews before anything is final.

> **Portfolio / educational project.** Entirely synthetic data — no real applicant records,
> no real institution's data, and not affiliated with any real university. See
> [`data/handbooks/sample_admissions_handbook.md`](data/handbooks/sample_admissions_handbook.md)
> for the fictional "Brightwater University" policy document the rules-extraction pipeline
> parses.

## Status

Built in phases, each verified before moving to the next.

| Phase | Status |
|---|---|
| 1. Foundation (data model, synthetic generators, LLM client interface, Docker Compose) | ✅ done |
| 2. Extraction (real Gemini wiring, upload → extract → store) | ⬜ not started |
| 3. Multi-agent validation + handbook rules extraction | ⬜ not started |
| 4. Course catalog (mock, pluggable for a real source later) | ⬜ not started |
| 5. Decision engine + human-in-the-loop review | ⬜ not started |
| 6. Reporting (secondary) | ⬜ not started |
| Later: real catalog integration, Cloud Run deploy, CI/CD, monitoring | not planned yet |

## Why this exists

A friend's university used to manually read every transfer applicant's transcript to check
eligibility — slow, expensive, and inconsistent. This reproduces the shape of the automation
system they built (transcript ingestion, multi-agent validation, LLM-parsed handbook rules,
scraped-catalog verification, human-reviewed decisions) as a portfolio project, adapted where
the original stack assumed cloud infrastructure unavailable here (real GCP credentials,
Databricks, GitLab CI).

## Tech stack

- **Backend**: Python, FastAPI, SQLAlchemy + Alembic migrations.
- **Database**: PostgreSQL via Docker Compose (the real target); SQLite for fast unit tests
  through the same engine abstraction (`db.py`).
- **LLM**: Google Gemini (`google-genai`), behind an `LLMClient` interface — a `GeminiClient`
  for real calls and a `FakeLLMClient` for tests, so no test suite ever makes a network call.
- **File storage**: local disk with soft-delete + restore, structured to swap in a cloud
  backend later without touching callers.
- **Frontend**: Next.js (App Router) + TypeScript + Tailwind.
- **Containerization**: Docker + Docker Compose (api, postgres; frontend service to follow).

## Repository structure

```
admissions-review-platform/
├── src/admissions_platform/
│   ├── config.py, db.py, models.py   # paths; SQLite-or-Postgres engine; the 9-table schema
│   ├── llm/client.py                  # LLMClient / GeminiClient / FakeLLMClient
│   ├── storage/local.py               # local-disk document storage
│   ├── ingestion/documents.py         # applicant/document CRUD, soft-delete + restore
│   ├── synthetic/                     # transcript generator (3 PDF layouts) + sample handbook
│   └── api/main.py                    # FastAPI app (health check only so far)
├── db/migrations/                     # Alembic
├── data/handbooks/                    # the fictional sample admissions handbook
├── frontend/                          # Next.js app
├── tests/                             # 28 tests (Phase 1)
├── docker-compose.yml, Dockerfile, scripts/docker-entrypoint.sh
└── alembic.ini
```

## Run it

Backend:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
alembic upgrade head          # creates the schema (SQLite by default; see .env.example for Postgres)
uvicorn admissions_platform.api.main:app --reload --port 8010
```

Frontend (separate terminal):
```bash
cd frontend
npm install
npm run dev                    # http://localhost:3000 — shows live backend health status
```

Tests:
```bash
pytest tests/ -v                # backend, 28 tests
cd frontend && npm run test     # frontend, 3 tests
```

**Docker Compose** (`docker-compose.yml`, `Dockerfile`, `scripts/docker-entrypoint.sh`) is
written and reviewed — runs migrations on container startup, Postgres on port 5433 (so it
doesn't collide with another Postgres instance) — but **not executed**: no Docker daemon was
available in this project's development environment. Verified instead against real SQLite and
the identical `DATABASE_URL`-driven engine abstraction every script uses.

## Design notes worth knowing

- **ORM + Alembic, not a hand-written schema.sql.** This schema has many related entities that
  will grow across several build phases — migrations evolve it incrementally.
- **`Optional[X]` / `List[X]`, not `X | None` / `list[X]`, in `models.py`.** Only Python 3.9 is
  available in this dev environment, and SQLAlchemy's declarative mapper evaluates annotations
  at class-definition time — `X | None` genuinely fails at runtime pre-3.10, not just a style
  preference. Every other module uses `from __future__ import annotations` and modern syntax
  freely; `models.py` is the one place that can't.
- **Soft-delete, never a real delete**, for uploaded documents — matches the project's
  retention/restore requirement. Permanent purging is a separate, explicit function nothing
  calls automatically.
- **PDFs go to Gemini directly** (native multimodal PDF understanding) rather than through a
  separate OCR step — simpler and more robust than OCR-then-regex, and is why the synthetic
  transcript generator renders real PDF files (three different layouts) rather than just
  producing JSON fixtures.

Full build plan: see the project's plan history. Each phase gets its own section here as it
lands.
