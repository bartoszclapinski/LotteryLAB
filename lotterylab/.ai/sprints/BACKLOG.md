# 📚 Product Backlog (prioritized)

Legend: [P] Priority (1=highest), [E] Epic, [S] Size (t-shirt)
Status: ✅ Completed, 🚧 In Progress, 📋 Planned

## Recently Completed (Sprint 001 MVP)
1. [P1][E1][S:M] ✅ CSV/Excel parser for historical draws (MBNet format)
2. [P1][E1][S:M] ✅ SQLAlchemy models: `draws`, `number_statistics`, `analyses`
3. [P1][E1][S:S] ✅ Initial migrations and DB bootstrap (SQLite dev)
4. [P1][E2][S:M] ✅ Frequency analysis service (windowed, hot/cold, expected vs actual)
5. [P1][E4][S:S] ✅ FastAPI app skeleton + `/health` endpoint
6. [P1][E3][S:S] ✅ Public UI scaffold (FastAPI + Jinja2 + HTMX)
7. [P1][E7][S:S] ✅ Config & secrets handling (envfile), logging, basic tests
8. [P2][E4][S:S] ✅ `/api/v1/draws` with filters (game_type, dates, limit)
9. [P2][E4][S:S] ✅ `/api/v1/analysis/frequency` with `window_days`
10. [P2][E1][S:M] ✅ Data validator & data import workflow (idempotent)

## Top priorities (Sprint 002)
11. [P1][E2][S:M] ✅ Randomness tests (chi-square, KS, runs, autocorr, entropy)
12. [P1][E3][S:M] ✅ Enhanced visualizations: correlation heatmap, time trends, sum distributions
13. [P1][E7][S:S] 📋 Basic packaging (pyproject/requirements), Makefile/tasks
14. [P1][E7][S:S] ✅ Comprehensive test suite (79% coverage - all 78 tests passing)

## High priorities (Sprint 003)
15. [P2][E5][S:L] 📋 Feature engineering & ML baselines (RF/XGB/MLP, CV)
16. [P2][E6][S:M] 📋 Monte Carlo simulation framework
17. [P2][E3][S:S] 📋 Reports export (PDF/Excel/HTML)

## Medium priorities (Sprint 004+)
18. [P3][E6][S:M] 📋 Chaos metrics prototype (Lyapunov, fractal dim)
19. [P3][E7][S:S] 📋 Redis cache for common queries
20. [P3][E7][S:S] 📋 Rate limiting & access logging

## Nice-to-have (Future)
21. [P4][E3][S:S] 📋 Theming and branding polish (light/dark tokens)

## Notes
- API client work is blocked pending Lotto OpenAPI key; use CSV first 🚧
- Maintain educational positioning; avoid “prediction” claims ✅
