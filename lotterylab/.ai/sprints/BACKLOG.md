# 📚 Product Backlog (prioritized)

Legend: [P] Priority (1=highest), [E] Epic, [S] Size (t-shirt)
Status: ✅ Completed, 🚧 In Progress, 📋 Planned

## Sprint 000 — Completed ✅
1. [P1][E1][S:M] ✅ CSV/Excel parser for historical draws (MBNet format)
2. [P1][E1][S:M] ✅ SQLAlchemy models: `draws`, `number_statistics`, `analyses`
3. [P1][E1][S:S] ✅ Initial migrations and DB bootstrap (SQLite dev)
4. [P1][E2][S:M] ✅ Frequency analysis service (windowed, hot/cold, expected vs actual)
5. [P1][E4][S:S] ✅ FastAPI app skeleton + `/health` endpoint
6. [P1][E3][S:S] ✅ Public UI scaffold (FastAPI + Jinja2 + HTMX)
7. [P1][E7][S:S] ✅ Config & secrets handling (envfile), logging, basic tests

## Sprint 001 — Completed ✅
8. [P2][E4][S:S] ✅ `/api/v1/draws` with filters (game_type, dates, limit)
9. [P2][E4][S:S] ✅ `/api/v1/analysis/frequency` with `window_days`
10. [P2][E1][S:M] ✅ Data validator & data import workflow (idempotent)
11. [P1][E7][S:S] ✅ Packaging (pyproject.toml, Makefile)
12. [P1][E7][S:S] ✅ Comprehensive test suite (78 tests, 79% coverage)

## Sprint 002 — Completed ✅
13. [P1][E2][S:M] ✅ Chi-square goodness-of-fit test
14. [P1][E2][S:M] ✅ Kolmogorov-Smirnov test for distribution comparison
15. [P1][E2][S:M] ✅ Runs test for sequence randomness
16. [P1][E2][S:M] ✅ Autocorrelation analysis for temporal dependencies
17. [P1][E2][S:M] ✅ Shannon entropy for randomness quantification
18. [P1][E2][S:M] ✅ Pattern detection (consecutive, arithmetic, digit analysis)
19. [P1][E3][S:M] ✅ Correlation heatmap visualization
20. [P1][E3][S:M] ✅ Time series trend analysis with period controls
21. [P1][E3][S:M] ✅ PDF export (ReportLab)
22. [P1][E3][S:M] ✅ Excel export (OpenPyXL)
23. [P1][E7][S:S] ✅ Internationalization (i18n) — Polish + English
24. [P1][E7][S:S] ✅ Auto-update on server startup (lifespan handler)
25. [P1][E3][S:M] ✅ UI alignment with design mockup (Stats Grid, Formula Box, Progress Bar, Monte Carlo demo)

## Sprint 003 — ML Baseline 📋 (NEXT)
26. [P2][E5][S:L] 📋 Feature engineering for ML models
27. [P2][E5][S:L] 📋 Baseline models (Random Forest, XGBoost, MLP)
28. [P2][E5][S:M] 📋 Cross-validation framework
29. [P2][E5][S:M] 📋 Feature importance analysis
30. [P2][E5][S:M] 📋 Backtesting on historical data
31. [P2][E5][S:S] 📋 Educational disclaimer & limitations documentation

## Sprint 004+ — Advanced/Research 📋
32. [P3][E6][S:M] 📋 Chaos metrics prototype (Lyapunov exponent, fractal dimension)
33. [P3][E6][S:M] 📋 Advanced Monte Carlo simulation framework
34. [P3][E7][S:S] 📋 Redis cache for common queries
35. [P3][E7][S:S] 📋 Rate limiting & access logging

## Sprint 005 — Production 📋
36. [P2][E7][S:M] 📋 Docker containerization
37. [P2][E7][S:M] 📋 CI/CD pipeline (GitHub Actions)
38. [P2][E7][S:M] 📋 Deployment (Railway/Render)
39. [P2][E7][S:S] 📋 Comprehensive documentation

## Nice-to-have (Future)
40. [P4][E3][S:S] 📋 Dark mode theme polish
41. [P4][E3][S:S] 📋 Mobile-first responsive improvements
42. [P4][E4][S:S] 📋 WebSocket for real-time updates
43. [P4][E1][S:M] 📋 Lotto API integration (when key available)

## Notes
- API client work is blocked pending Lotto OpenAPI key; using CSV/MBNet ✅
- Maintain educational positioning; avoid "prediction" claims ✅
- Current data: ~9300+ historical draws from 1957
