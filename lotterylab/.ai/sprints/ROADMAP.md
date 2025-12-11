# 🗺️ Lottery Lab Roadmap (v2)

Timeboxes are indicative. Adjust based on API access and findings.

## 🧩 Epics
- E1: Data acquisition & storage
- E2: Core statistical analysis & randomness tests
- E3: Visualization & dashboard
- E4: API surface (FastAPI)
- E5: ML baseline & backtesting (educational)
- E6: Advanced analyses (chaos, Monte Carlo)
- E7: Quality, docs, and deployment
- **E8: UI/UX Redesign & Multi-lottery** ← NEW

## 🧭 Planned sprints
- Sprint 000 — Kickoff (pre-API-key) — 1 week ✅
  - Repo scaffolding, config, data schema, CSV import path
- Sprint 001 — MVP — 2 weeks ✅
  - DB models+migrations, ingestion (CSV first), frequency analysis, basic API, FastAPI + Jinja2 + HTMX UI scaffold, packaging, comprehensive tests
- Sprint 002 — Core Analyses — 2 weeks ✅
  - Randomness tests (chi-square, KS, runs, autocorr, entropy), pattern detection, correlation heatmap, time series trends, PDF/Excel export, i18n (PL/EN)
- **Sprint 002.5 — UI Redesign — 2 weeks 🚧 CURRENT**
  - Homepage landing, methodology pages, design system, dark/light themes, multi-lottery architecture
- Sprint 003 — ML Baseline — 3 weeks 📋
  - Feature prep, baseline models (RF/XGB/MLP), cross-validation, feature importance, backtesting
- Sprint 004 — Advanced/Research — 3 weeks 📋
  - Chaos metrics, Monte Carlo simulations, exploratory notebooks
- Sprint 005 — Production — 2 weeks 📋
  - Tests, docs, Docker, CI/CD, deployment

## 🎯 Milestones
- M1: MVP usable dashboard and API health endpoint ✅
- M2: Randomness test suite with reproducible results ✅
- **M2.5: Modern UI with landing page, methodology docs, theme support 🚧**
- M3: Baseline ML experiments with documented limitations 📋
- M4: Packaging and deployment readiness 📋

## 📊 Success metrics (aligned to PRD)
- >80% code coverage; p95 API < 500ms; >99.9% uptime targets
- 1k+ users month 1; 50+ analyses/day; clear educational disclaimer
- **Lighthouse Performance > 90; Accessibility > 95** ← NEW

## 🔗 Sprint index
- See `sprint000/plan.md`
- See `sprint001/plan.md`
- See `sprint002/plan.md`
- **See `sprint002.5/plan.md`** ← UI Redesign

## 📈 Current Status (as of 2025-12-11)
| Sprint | Status | Key Deliverables |
|--------|--------|------------------|
| 000 | ✅ Done | Scaffolding, DB schema, CSV import |
| 001 | ✅ Done | MVP UI, API, frequency analysis, tests |
| 002 | ✅ Done | Randomness tests, patterns, correlation, trends, export, i18n |
| **002.5** | **🚧 Current** | **UI Redesign: homepage, methodology, themes** |
| 003 | 📋 Next | ML baseline (educational) |
