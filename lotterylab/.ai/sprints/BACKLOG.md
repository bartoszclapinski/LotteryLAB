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

## Sprint 002.5 — UI Redesign 🚧 (CURRENT)
26. [P1][E8][S:M] 🚧 Design System: CSS variables, tokens, themes
27. [P1][E8][S:M] 📋 Homepage landing page (hero, features, how-it-works)
28. [P1][E8][S:M] 📋 Methodology overview page (all methods grid)
29. [P1][E8][S:L] 📋 Methodology detail pages (chi-square, KS, runs, autocorr, entropy, monte-carlo)
30. [P1][E8][S:S] 📋 Dark/Light theme toggle with localStorage
31. [P1][E8][S:S] 📋 Cleanup test data (999997/999998)
32. [P2][E8][S:M] 📋 Move analyzer to /app route
33. [P2][E8][S:M] 📋 Multi-lottery selector UI
34. [P2][E8][S:S] 📋 URL-based i18n (/pl/..., /en/...)
35. [P2][E8][S:S] 📋 Expand translations for new pages

## Sprint 003 — ML Baseline 📋
36. [P2][E5][S:L] 📋 Feature engineering for ML models
37. [P2][E5][S:L] 📋 Baseline models (Random Forest, XGBoost, MLP)
38. [P2][E5][S:M] 📋 Cross-validation framework
39. [P2][E5][S:M] 📋 Feature importance analysis
40. [P2][E5][S:M] 📋 Backtesting on historical data
41. [P2][E5][S:S] 📋 Educational disclaimer & limitations documentation

## Sprint 004 — Advanced/Research 📋
42. [P3][E6][S:M] 📋 Chaos metrics prototype (Lyapunov exponent, fractal dimension)
43. [P3][E6][S:M] 📋 Advanced Monte Carlo simulation framework
44. [P3][E7][S:S] 📋 Redis cache for common queries
45. [P3][E7][S:S] 📋 Rate limiting & access logging

## Sprint 005 — Production 📋
46. [P2][E7][S:M] 📋 Docker containerization
47. [P2][E7][S:M] 📋 CI/CD pipeline (GitHub Actions)
48. [P2][E7][S:M] 📋 Deployment (Railway/Render)
49. [P2][E7][S:S] 📋 Comprehensive documentation

## Nice-to-have (Future)
50. [P4][E3][S:S] 📋 Mobile-first responsive improvements (beyond basic)
51. [P4][E4][S:S] 📋 WebSocket for real-time updates
52. [P4][E1][S:M] 📋 Lotto API integration (when key available)
53. [P4][E8][S:M] 📋 Additional lotteries (UK, US, EU)
54. [P4][E8][S:S] 📋 PWA support (offline mode)

## Notes
- API client work is blocked pending Lotto OpenAPI key; using CSV/MBNet ✅
- Maintain educational positioning; avoid "prediction" claims ✅
- Current data: ~9300+ historical draws from 1957
