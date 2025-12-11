# 🎨 Sprint 002.5 — UI Redesign

- **Dates:** 2025-12-11 → 2025-12-25 (2 weeks)
- **Goal:** Stworzyć nowoczesny, przyjazny UI z homepage'em, stronami metodologii i systemem motywów
- **Scope:** 
  - IN: Design system, homepage, metodologia, themes, cleanup, i18n
  - OUT: Nowe funkcje analityczne, ML, deployment

---

## 📦 Deliverables

| # | Deliverable | Priority | Status |
|---|-------------|----------|--------|
| D1 | Design System CSS (variables, components, themes) | P1 | 📋 |
| D2 | Homepage landing page | P1 | 📋 |
| D3 | Methodology overview page | P1 | 📋 |
| D4 | Methodology detail pages (6 metod) | P1 | 📋 |
| D5 | Dark/Light theme toggle | P1 | 📋 |
| D6 | Test data cleanup (999997/999998) | P1 | 📋 |
| D7 | App route restructure (/app) | P2 | 📋 |
| D8 | Multi-lottery selector UI | P2 | 📋 |
| D9 | URL-based i18n | P2 | 📋 |

---

## 🔧 Tasks Breakdown

### Phase 1: Design System (Days 1-2)

- [ ] **T1.1** Create `static/css/design-system.css`
  - CSS variables for colors, typography, spacing
  - Dark theme tokens
  - Light theme tokens
  
- [ ] **T1.2** Create `static/css/components.css`
  - Button variants (primary, ghost, icon)
  - Card variants (feature, method, stat, info)
  - Form components (switch, select, slider)
  - Navigation components
  
- [ ] **T1.3** Create `static/js/theme-toggle.js`
  - Theme switching logic
  - localStorage persistence
  - System preference detection
  
- [ ] **T1.4** Update `templates/base.html`
  - Add `data-theme` attribute to `<html>`
  - Include new CSS files
  - Add theme toggle to header

### Phase 2: Homepage (Days 3-4)

- [ ] **T2.1** Create route `/` for homepage
  - Separate from `/app` (current analyzer)
  
- [ ] **T2.2** Create `templates/home.html`
  - Hero section with headline, disclaimer, CTAs
  - Lottery balls visual (animated)
  - Mini stats (hot/cold, χ², entropy)
  
- [ ] **T2.3** Features section
  - 6 feature cards with icons
  - Links to /app/frequency, /app/randomness, etc.
  
- [ ] **T2.4** How It Works section
  - 4 steps: Collect → Validate → Test → Interpret
  
- [ ] **T2.5** Footer with links

### Phase 3: Methodology Pages (Days 5-8)

- [ ] **T3.1** Create `templates/methodology/index.html`
  - Hero with "Metodologia badawcza"
  - Hypothesis box (H₀)
  - 6 method cards with questions, formulas, results
  - Lottery support grid (flags)
  
- [ ] **T3.2** Create `templates/methodology/_base.html`
  - 3-column layout (sidebar, content, TOC)
  - Prev/Next navigation
  - Progress indicator
  
- [ ] **T3.3** Create methodology detail pages:
  - [ ] `chi-square.html` — Test Chi-kwadrat
  - [ ] `ks-test.html` — Kołmogorow-Smirnow
  - [ ] `runs-test.html` — Test serii
  - [ ] `autocorrelation.html` — Autokorelacja
  - [ ] `entropy.html` — Entropia Shannona
  - [ ] `monte-carlo.html` — Monte Carlo
  
- [ ] **T3.4** Create API routes:
  - `GET /methodology` → overview
  - `GET /methodology/<method>` → detail

### Phase 4: App Restructure (Days 9-10)

- [ ] **T4.1** Move current analyzer to `/app`
  - Update routes in `main.py`
  - Update all internal links
  
- [ ] **T4.2** Add lottery selector
  - Dropdown in sidebar
  - Update all analysis endpoints to use selected lottery
  
- [ ] **T4.3** Cleanup test data
  - SQL script to remove draw_number > 900000
  - Verify data integrity
  
- [ ] **T4.4** Update navigation
  - Header: Home | Methodology | Analyzer | Docs
  - Sidebar: method-specific navigation

### Phase 5: I18n & Polish (Days 11-14)

- [ ] **T5.1** Expand `i18n.py`
  - Add translations for all new pages
  - Hero texts, method descriptions, UI labels
  
- [ ] **T5.2** Implement URL-based language
  - Routes: `/pl/...`, `/en/...`
  - Language detection middleware
  - Cookie/localStorage fallback
  
- [ ] **T5.3** Translate content
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
   - Clear value proposition
   - Visible disclaimer
   - Working CTAs to analyzer

2. **Methodology section** at `/methodology` with:
   - Overview of all 6 methods
   - Detail page for each method
   - Interactive demos where applicable

3. **Theme toggle** works:
   - Dark/Light switch in header
   - Preference saved in localStorage
   - All pages respect theme

4. **No test data visible**:
   - Draw numbers 999997, 999998 removed
   - Only real historical data shown

5. **i18n works**:
   - `/pl/...` shows Polish
   - `/en/...` shows English
   - Language toggle in header

---

## 🧪 Testing Plan

| Test | Description | Status |
|------|-------------|--------|
| Visual regression | Compare with design mockups | 📋 |
| Theme persistence | Toggle, refresh, verify | 📋 |
| Responsive | Test on mobile, tablet, desktop | 📋 |
| i18n coverage | All strings translated | 📋 |
| Links | No broken internal links | 📋 |
| Lighthouse | Performance > 90, A11y > 95 | 📋 |

---

## ⚠️ Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| CSS conflicts with existing styles | Medium | Medium | Use scoped CSS, namespace classes |
| Translation incomplete | Low | Low | Use fallback to PL |
| Breaking existing functionality | Medium | High | Feature flags, gradual rollout |

---

## 📊 Definition of Done

- [ ] All tasks completed
- [ ] Design mockups matched
- [ ] Theme toggle working
- [ ] i18n for PL/EN
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
- 📋 Next: Start implementing design system CSS

---

*Sprint created: 2025-12-11*

