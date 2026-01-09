# 📚 Product Backlog (prioritized)

Legend: [P] Priority (1=highest), [E] Epic, [S] Size (t-shirt)
Status: ✅ Completed, 🚧 In Progress, 📋 Planned

---

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

## Sprint 002.5 — UI Redesign 🚧 (~98% Complete)

### Phase 1: Design System ✅
26. [P1][E8][S:M] ✅ `design-system.css` — CSS variables, design tokens (430+ lines)
27. [P1][E8][S:M] ✅ `components.css` — Reusable components (842+ lines)
28. [P1][E8][S:S] ✅ `theme-toggle.js` — Dark/Light theme toggle with localStorage (127 lines)

### Phase 2: Homepage ✅
29. [P1][E8][S:M] ✅ `home.html` — Landing page with hero, features, how-it-works (283 lines)
30. [P1][E8][S:S] ✅ Route `/` separate from `/app`

### Phase 3: Methodology ✅ (5/6)
31. [P1][E8][S:M] ✅ `methodology.html` — Overview page with 6 method cards (365 lines)
32. [P1][E8][S:L] ✅ `methodology/chi-square.html` — Detail page with interactive demo (469 lines)
33. [P1][E8][S:M] ✅ `methodology/kolmogorov-smirnov.html` — Detail page
34. [P1][E8][S:M] ✅ `methodology/runs-test.html` — Detail page
35. [P1][E8][S:M] ✅ `methodology/autocorrelation.html` — Detail page
36. [P1][E8][S:M] ✅ `methodology/entropy.html` — Detail page
37. [P1][E8][S:M] ✅ `methodology/monte-carlo.html` — Detail page (500+ lines, interactive demo)

### Phase 4: App & Cleanup 🚧
38. [P2][E8][S:M] ✅ Move analyzer to /app route
39. [P2][E8][S:M] 📋 Multi-lottery selector UI
40. [P1][E8][S:S] ✅ Cleanup test data (999997/999998) — verified clean

### Phase 5: I18n 🚧
41. [P1][E8][S:M] ✅ Expand translations for new pages (homepage, methodology)
42. [P2][E8][S:S] 📋 URL-based i18n (/pl/..., /en/...)

---

## Sprint 003 — ML Baseline 📋
43. [P2][E5][S:L] 📋 Feature engineering for ML models
44. [P2][E5][S:L] 📋 Baseline models (Random Forest, XGBoost, MLP)
45. [P2][E5][S:M] 📋 Cross-validation framework
46. [P2][E5][S:M] 📋 Feature importance analysis
47. [P2][E5][S:M] 📋 Backtesting on historical data
48. [P2][E5][S:S] 📋 Educational disclaimer & limitations documentation

## Sprint 004 — Advanced/Research 📋
49. [P3][E6][S:M] 📋 Chaos metrics prototype (Lyapunov exponent, fractal dimension)
50. [P3][E6][S:M] 📋 Advanced Monte Carlo simulation framework
51. [P3][E7][S:S] 📋 Redis cache for common queries
52. [P3][E7][S:S] 📋 Rate limiting & access logging

## Sprint 005 — Production 📋
53. [P2][E7][S:M] 📋 Docker containerization
54. [P2][E7][S:M] 📋 CI/CD pipeline (GitHub Actions)
55. [P2][E7][S:M] 📋 Deployment (Railway/Render)
56. [P2][E7][S:S] 📋 Comprehensive documentation

## Nice-to-have (Future)
57. [P4][E3][S:S] 📋 Mobile-first responsive improvements (beyond basic)
58. [P4][E4][S:S] 📋 WebSocket for real-time updates
59. [P4][E1][S:M] 📋 Lotto API integration (when key available)
60. [P4][E8][S:M] 📋 Additional lotteries (UK, US, EU)
61. [P4][E8][S:S] 📋 PWA support (offline mode)

---

## Notes
- API client work is blocked pending Lotto OpenAPI key; use CSV first 🚧
- Maintain educational positioning; avoid “prediction” claims ✅
- API client work is blocked pending Lotto OpenAPI key; using CSV/MBNet ✅
- Maintain educational positioning; avoid "prediction" claims ✅
- Current data: ~9300+ historical draws from 1957
- Sprint 002.5 is ~98% complete — only optional P2 tasks remaining (URL i18n, multi-lottery)

---

*Last updated: 2025-01-09*

