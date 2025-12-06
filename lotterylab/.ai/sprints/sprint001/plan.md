# 🏁 Sprint 001 — MVP

- Dates: <next week> → +14 days
- 🚀 Goal: Deliver a working MVP with local historical data, frequency analysis, and a simple dashboard & API.
- 🗺️ Scope: IN — DB persistence, ingestion (CSV first), frequency endpoints & UI. OUT — Lotto API integration (pending key), advanced analyses.

## 📦 Deliverables
- Alembic-managed DB schema (SQLite dev) ✅
- Ingestion pipeline (CSV → DB) with validation and logs ✅
- Frequency analysis API: `GET /api/v1/analysis/frequency` ✅
- Draws API: `GET /api/v1/draws` with filters ✅
- FastAPI + Jinja2 + HTMX public UI scaffold (base layout, frequency page) ✅
- Apply Google ML Crash Course-inspired layout (header/tabs, sidebar, right panel) ✅
- Enhanced Jinja2+HTMX dashboard: interactive charts, hot/cold analysis, recent draws table ✅

## 🔧 Stories & Tasks
- [x] Finalize models and repository layer
- [x] Implement ingestion service (batch and incremental)
- [x] Frequency service: expected vs actual comparison
- [x] FastAPI endpoints + Pydantic schemas
- [x] Partials restyle: cards + consistent typography; remove inline styles
- [x] Theme tokens: add `html[data-theme="dark"]` overrides
- [x] Enhanced Jinja2+HTMX UI components: interactive charts, hot/cold analysis, number generator
- [x] Basic packaging (pyproject/requirements), Makefile/tasks
- [x] Tests: repositories, services, endpoints (happy paths)
- [x] UI (FastAPI + Jinja2 + HTMX) scaffold:
  - [x] Create `templates/` and `static/` (CSS, JS, images)
  - [x] Base template matching `.design/main-design.html` (header, footer, layout)
  - [x] Frequency page rendering server-side; HTMX partials for filters/sections
  - [x] Minimal CSS theme (light), ready for dark toggle later 🌗
  - [x] Mount static files; add HTML routes in FastAPI
  - [x] Optional: Plotly.js/ECharts for charts on the page
  - [x] Enable CORS if needed
  - [x] UI smoke tests (200 OK, template variables render)

## ✅ Acceptance criteria
- Import completes for full sample history without errors (bad rows logged)
- Frequency endpoint returns JSON with counts, percentages, hot/cold flags
- Dashboard (Jinja2) loads in <2s and mirrors API results
- HTMX interactions update sections without full page reload

## 🧪 Validation & Demos
- Demo notebook cross-checking API results vs direct DB queries
- Manual exploratory test of dashboard filters and HTMX interactions
- Open main dashboard in browser; verify HTMX partial updates, charts, and interactive components

## ⚠️ Risks & Mitigations
- Performance on large CSV → chunked reads, indices on `draws`
- Data quality → strict schema, validation, clear logs
- Visual fidelity → reuse `.design` assets and iterate CSS with tokens

## 📊 Metrics / DoD
- 15+ unit/integration tests
- Basic coverage reported; linting clean
- UI smoke tests for key routes ✅

## 🔁 Changes during sprint (running notes)
- 2025-09-08: Planned migration for public UI to FastAPI + Jinja2 + HTMX; tasks added 🧩
- 2025-09-08: UI scaffold implemented; base page + HTMX partials + static assets ✅
- 2025-09-08: Added Plotly.js frequency bar chart with HTMX-driven updates ✅
- 2025-09-08: Implemented GET `/api/v1/draws` with filters and Pydantic response ✅
- 2025-09-08: Enabled CORS for local development ✅
- 2025-09-08: Applied Jinja UI styling (header/logo, cards, controls, grid) ✅
- 2025-09-08: Added Recent Draws table (latest 20) ✅
- 2025-09-08: Frequency now includes expected vs actual; UI overlay with expected line ✅
- 2025-09-08: Tests extended for expected/delta; 8 tests passing ✅
- 2025-09-08: Repository layer added for draws; API refactored; 10 tests passing ✅
- 2025-09-08: Ingestion service added (batch lines/files + incremental via MBNet); tests passing ✅
- 2025-09-21: Restyled UI to 3-column layout; partials aligned; dark tokens added ✅
- 2025-09-21: Updated generator to diversify sets; new entries logged ✅
- 2025-09-22: Removed Streamlit dependency; focusing exclusively on Jinja2+HTMX interface ✅
