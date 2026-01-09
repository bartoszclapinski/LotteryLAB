# 🎨 Sprint 002.5 — UI Redesign

- **Dates:** 2025-12-11 → 2025-12-25 (2 weeks)
- **Goal:** Stworzyć nowoczesny, przyjazny UI z homepage'em, stronami metodologii i systemem motywów
- **Scope:** 
  - IN: Design system, homepage, metodologia, themes, cleanup, i18n
  - OUT: Nowe funkcje analityczne, ML, deployment
- **Status:** ✅ ~98% Complete (Only optional P2 tasks remaining)

---

## 📦 Deliverables

| # | Deliverable | Priority | Status |
|---|-------------|----------|--------|
| D1 | Design System CSS (variables, components, themes) | P1 | ✅ Done |
| D2 | Homepage landing page | P1 | ✅ Done |
| D3 | Methodology overview page | P1 | ✅ Done |
| D4 | Methodology detail pages (6 metod) | P1 | ✅ Done |
| D5 | Dark/Light theme toggle | P1 | ✅ Done |
| D6 | Test data cleanup (999997/999998) | P1 | ✅ Done (already clean) |
| D7 | App route restructure (/app) | P2 | ✅ Done |
| D8 | Multi-lottery selector UI | P2 | 📋 Pending |
| D9 | URL-based i18n | P2 | 📋 Pending |

---

## 🔧 Tasks Breakdown

### Phase 1: Design System (Days 1-2) ✅ COMPLETE

- [x] **T1.1** Create `static/css/design-system.css`
  - CSS variables for colors, typography, spacing
  - Dark theme tokens
  - Light theme tokens
  - 430+ lines of design tokens
  
- [x] **T1.2** Create `static/css/components.css`
  - Button variants (primary, secondary, ghost, outline, icon)
  - Card variants (feature, method, stat, info)
  - Form components (switch-group, theme-toggle, select, input, slider)
  - Navigation components (header, logo, nav, breadcrumb, sidebar)
  - Lottery balls, formula box, code blocks
  - 842+ lines of components
  
- [x] **T1.3** Create `static/js/theme-toggle.js`
  - Theme switching logic
  - localStorage persistence
  - System preference detection
  - 127 lines
  
- [x] **T1.4** Update templates with `data-theme`
  - Add `data-theme` attribute to `<html>`
  - Include new CSS files
  - Add theme toggle to header

### Phase 2: Homepage (Days 3-4) ✅ COMPLETE

- [x] **T2.1** Create route `/` for homepage
  - Separate from `/app` (current analyzer)
  
- [x] **T2.2** Create `templates/home.html`
  - Hero section with headline, disclaimer, CTAs
  - Lottery balls visual
  - Mini stats (hot/cold, χ², entropy)
  - 283 lines
  
- [x] **T2.3** Features section
  - 6 feature cards with icons
  - Links to /app
  
- [x] **T2.4** How It Works section
  - 4 steps: Collect → Validate → Test → Interpret
  
- [x] **T2.5** Footer with links

### Phase 3: Methodology Pages (Days 5-8) ✅ COMPLETE

- [x] **T3.1** Create `templates/methodology.html` (overview)
  - Hero with "Metodologia badawcza"
  - Hypothesis box (H₀)
  - 6 method cards with questions, formulas, results
  - Lottery support grid (8 lotteries with flags)
  - Workflow steps
  - CTA section
  - 365 lines
  
- [x] **T3.2** Create methodology detail layout
  - 3-column layout (sidebar, content, TOC)
  - Prev/Next navigation
  - Progress indicator
  - Breadcrumbs
  
- [x] **T3.3** Create methodology detail pages:
  - [x] `chi-square.html` — Test Chi-kwadrat (469 lines, interactive demo!)
  - [x] `kolmogorov-smirnov.html` — Test Kołmogorowa-Smirnowa
  - [x] `runs-test.html` — Test serii
  - [x] `autocorrelation.html` — Autokorelacja
  - [x] `entropy.html` — Entropia Shannona
  - [x] `monte-carlo.html` — Monte Carlo ✅ DONE
  
- [x] **T3.4** Create API routes:
  - `GET /methodology` → overview
  - `GET /methodology/<method>` → detail

### Phase 4: App Restructure (Days 9-10) 🚧 PARTIAL

- [x] **T4.1** Move current analyzer to `/app`
  - Routes updated in `main.py`
  - Internal links updated
  
- [ ] **T4.2** Add lottery selector
  - Dropdown in sidebar
  - Update all analysis endpoints to use selected lottery
  
- [x] **T4.3** Cleanup test data
  - SQL script to remove draw_number > 900000
  - Verify data integrity
  - ✅ Verified 2025-01-09: No test records found, database is clean
  
- [x] **T4.4** Update navigation
  - Header: Home | Methodology | Analyzer | Docs
  - Sidebar navigation on methodology pages

### Phase 5: I18n & Polish (Days 11-14) 🚧 PARTIAL

- [x] **T5.1** Expand `i18n.py`
  - Add translations for all new pages
  - Hero texts, method descriptions, UI labels
  
- [ ] **T5.2** Implement URL-based language
  - Routes: `/pl/...`, `/en/...`
  - Language detection middleware
  - Cookie/localStorage fallback
  
- [x] **T5.3** Translate content
  - Homepage (PL/EN)
  - Methodology overview (PL/EN)
  - Method details (PL/EN)
  
- [ ] **T5.4** Final polish
  - Responsive testing
  - Cross-browser testing
  - Lighthouse audit

---

## ✅ Acceptance Criteria

1. **Homepage exists** at `/` with:
   - [x] Clear value proposition
   - [x] Visible disclaimer
   - [x] Working CTAs to analyzer

2. **Methodology section** at `/methodology` with:
   - [x] Overview of all 6 methods
   - [ ] Detail page for each method (5/6 done, monte-carlo missing)
   - [x] Interactive demos where applicable

3. **Theme toggle** works:
   - [x] Dark/Light switch in header
   - [x] Preference saved in localStorage
   - [x] All pages respect theme

4. **No test data visible**:
   - [x] Draw numbers 999997, 999998 removed (verified clean)
   - [x] Only real historical data shown (max draw_number = 9377)

5. **i18n works**:
   - [ ] `/pl/...` shows Polish (not implemented - using query params)
   - [ ] `/en/...` shows English
   - [x] Language toggle in header

---

## 🧪 Testing Plan

| Test | Description | Status |
|------|-------------|--------|
| Visual regression | Compare with design mockups | ✅ Done |
| Theme persistence | Toggle, refresh, verify | ✅ Done |
| Responsive | Test on mobile, tablet, desktop | 📋 Pending |
| i18n coverage | All strings translated | ✅ Done |
| Links | No broken internal links | 🚧 1 broken (monte-carlo) |
| Lighthouse | Performance > 90, A11y > 95 | 📋 Pending |

---

## ⚠️ Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| CSS conflicts with existing styles | Medium | Medium | Use scoped CSS, namespace classes |
| Translation incomplete | Low | Low | Use fallback to PL |
| Breaking existing functionality | Medium | High | Feature flags, gradual rollout |

---

## 📊 Definition of Done

- [ ] All tasks completed (90% done)
- [x] Design mockups matched
- [x] Theme toggle working
- [x] i18n for PL/EN (query-based, not URL-based)
- [ ] No test data visible
- [ ] Lighthouse scores met
- [ ] PR reviewed and merged

---

## 🔗 Related Documents

- **Design Spec:** `.ai/ui-redesign-spec.md`
- **Design Files:** `.design/homepage-v3-themes.html`, `.design/methodology-*.html`
- **i18n:** `src/utils/i18n.py`

---

## 🔁 Daily Log

### Day 1 (2025-12-11)
- ✅ Created UI redesign specification (`.ai/ui-redesign-spec.md`)
- ✅ Updated ROADMAP with Sprint 002.5
- ✅ Updated BACKLOG with UI tasks
- ✅ Created this sprint plan
- ✅ Design mockups ready: homepage, methodology overview, methodology detail

### Days 2-10 (2025-12-12 → 2025-12-20)
- ✅ **Phase 1 Complete:** Design System CSS
  - `design-system.css` (430+ lines) — full design tokens
  - `components.css` (842+ lines) — reusable components
  - `theme-toggle.js` (127 lines) — theme switching
- ✅ **Phase 2 Complete:** Homepage
  - `home.html` (283 lines) — full landing page
  - Hero, features grid, how-it-works, footer
- ✅ **Phase 3 Complete:** Methodology Pages
  - `methodology.html` (365 lines) — overview page
  - `methodology/chi-square.html` (469 lines) — with interactive demo!
  - `methodology/kolmogorov-smirnov.html` — detail page
  - `methodology/runs-test.html` — detail page
  - `methodology/autocorrelation.html` — detail page
  - `methodology/entropy.html` — detail page
  - ❌ `methodology/monte-carlo.html` — **NOT CREATED**
- ✅ **App restructure:** `/app` route working
- ✅ **Translations:** i18n expanded for all new pages

### Day 11 (2025-01-06)
- ✅ Documentation audit — discovered sprint is ~90% complete
- ✅ Updated sprint plan, BACKLOG, ROADMAP, log.md to reflect actual state
- 📋 Next: Create monte-carlo.html, cleanup test data

---

## 📌 Remaining Work

1. ~~**Create `monte-carlo.html`**~~ ✅ DONE (2025-01-07)
2. ~~**Cleanup test data**~~ ✅ VERIFIED CLEAN (2025-01-09)
3. **URL-based i18n** (optional, P2) — ~4 hours
4. **Multi-lottery selector** (optional, P2) — ~3 hours
5. **Lighthouse audit** — ~1 hour

---

*Sprint created: 2025-12-11*
*Last updated: 2025-01-06*
