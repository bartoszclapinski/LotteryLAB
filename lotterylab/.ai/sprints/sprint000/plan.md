# 🏁 Sprint 000 — Kickoff (pre-API-key)

- Dates: <today> → +7 days
- 🚀 Goal: Establish foundations to ingest and analyze historical data via CSV while awaiting Lotto OpenAPI key.
- 🗺️ Scope: IN — repo scaffolding, config, DB schema, CSV path, frequency analysis draft. OUT — Lotto API client, production deployment.

## 📦 Deliverables
- Minimal FastAPI app with `/api/v1/health` ✅
- SQLAlchemy models for `draws`, `number_statistics`, `analyses` ✅
- SQLite dev DB + initial Alembic migration ✅
- TXT parser and validator for initial dataset ✅
- Frequency analysis function (windowed, hot/cold prototype) ✅
- Streamlit page with frequency histogram ✅

## 🔧 Stories & Tasks
- [x] Scaffold Python project (requirements + folders) and env config (.env.example)
- [x] Create FastAPI app structure and `/health`
- [x] Define SQLAlchemy models and Alembic migration
- [x] Implement TXT parser for `initial_data_*.txt`
- [x] Add validator (date parse, range 1..49, unique numbers per draw)
- [x] Import script: idempotent upsert into `draws` (+ auto-label `lotto` vs `lotto_plus` by date)
- [x] Add non-unique indexes on `draws(draw_date)` and `draws(game_type)`
- [x] Frequency analysis service (window N days; hot/cold split) + endpoint `/api/v1/analysis/frequency`
- [x] Streamlit basic page: histogram + summary stats
- [x] Unit tests (parser, validator, frequency calc)
- [x] Logging baseline and error handling

## ✅ Acceptance criteria
- Health endpoint returns `{status: healthy}`
- Importing provided sample CSV loads >= 100 historical draws
- Frequency results expose counts and percentages for 1..49 within a window
- Streamlit page renders in <2s with histogram on local data

## 🧪 Validation & Demos
- CLI import run on sample TXT; check DB row counts
- Unit tests green; quick manual E2E via Streamlit

## ⚠️ Risks & Mitigations
- TXT inconsistencies → robust validator; skip & log bad rows; fixtures
- Time constraints → prioritize ingestion and one analysis path

## 📊 Metrics / DoD
- 8+ unit tests; basic coverage report
- Lint clean; typing passes where applicable

## 🔁 Changes during sprint (running notes)
- 2025-09-06 (sprint000-d01): Project skeleton and health endpoint added ✅
- 2025-09-06 (sprint000-d01): SQLAlchemy models, Alembic initial migration, and upgrade applied ✅
- 2025-09-06 (sprint000-d01): TXT importer + auto-label Lotto/Lotto Plus by date; 9271 rows imported ✅
- 2025-09-06 (sprint000-d01): Added indexes on `draws(draw_date)` and `draws(game_type)` ✅
- 2025-09-06 (sprint000-d01): Frequency service + endpoint delivered ✅
- 2025-09-08 (sprint000-d02): Rebranded to "Lottery Lab"; added `game_provider` to schema; updated PRD ✅
- 2025-09-08 (sprint000-d02): Auto-update from MBNet implemented with raw archive and retention ✅
- 2025-09-08 (sprint000-d02): Streamlit theme and layout applied; non-auto-open browser config ✅
- 2025-09-08 (sprint000-d02): Unit tests added (parser, validator, frequency) — 7 passing ✅
- 2025-09-08 (sprint000-d02): Minimal logging baseline (UTC, rotating files) and instrumentation ✅
