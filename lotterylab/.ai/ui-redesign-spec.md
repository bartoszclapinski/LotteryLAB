# 🎨 UI Redesign Specification — Lottery Lab v2

**Wersja:** 1.0  
**Data:** Grudzień 2025  
**Status:** Draft → Review

---

## 1. EXECUTIVE SUMMARY

### 1.1 Problem Statement

Obecny UI ma kilka krytycznych problemów:
- ❌ **Brak landing page** — użytkownik trafia od razu w analizę bez kontekstu
- ❌ **Information overload** — zbyt dużo danych na raz (chi-kwadrat, entropia...)
- ❌ **Brak onboardingu** — nie wyjaśniamy PO CO to wszystko
- ❌ **Testowe dane w produkcji** — numery 999997/999998 widoczne
- ❌ **Tylko dark theme** — brak wyboru dla użytkownika

### 1.2 Solution Overview

Kompletny redesign UI z:
- ✅ **Prawdziwy Homepage** — landing page z wartością edukacyjną
- ✅ **Hierarchia informacji** — stopniowe wprowadzanie w szczegóły
- ✅ **Metodologia** — osobne strony wyjaśniające metody
- ✅ **Theme system** — Dark + Light mode
- ✅ **i18n ready** — PL/EN z możliwością rozszerzenia
- ✅ **Multi-lottery** — architektura wspierająca różne loterie

### 1.3 Design Principles

1. **Progressive Disclosure** — pokazuj szczegóły stopniowo
2. **Education First** — wyjaśniaj zanim pokażesz dane
3. **Clarity over Density** — lepiej czytelnie niż gęsto
4. **Consistent Theming** — spójny design system
5. **Accessibility** — WCAG 2.1 AA compliance

---

## 2. INFORMATION ARCHITECTURE

### 2.1 Site Map

```
/                                   ← Homepage (Landing)
│
├── /methodology                    ← Metodologia: Przegląd
│   ├── /methodology/chi-square     ← Szczegóły: Test Chi-kwadrat
│   ├── /methodology/ks-test        ← Szczegóły: Kołmogorow-Smirnow
│   ├── /methodology/runs-test      ← Szczegóły: Test serii
│   ├── /methodology/autocorrelation← Szczegóły: Autokorelacja
│   ├── /methodology/entropy        ← Szczegóły: Entropia Shannona
│   └── /methodology/monte-carlo    ← Szczegóły: Monte Carlo
│
├── /app                            ← Analizator (główna aplikacja)
│   ├── /app/frequency              ← Analiza częstości
│   ├── /app/randomness             ← Testy losowości
│   ├── /app/patterns               ← Wzorce i sekwencje
│   ├── /app/correlation            ← Mapa korelacji
│   ├── /app/trends                 ← Trendy czasowe
│   └── /app/generator              ← Generator liczb
│
├── /docs                           ← Dokumentacja techniczna
│   ├── /docs/api                   ← API Reference
│   └── /docs/data                  ← Format danych
│
└── /about                          ← O projekcie
    ├── /about/team                 ← Zespół (opcjonalnie)
    └── /about/license              ← Licencja MIT
```

### 2.2 URL Strategy dla i18n

**Opcja A: Path-based (rekomendowane)**
```
/pl/methodology/chi-square
/en/methodology/chi-square
```

**Opcja B: Query-based**
```
/methodology/chi-square?lang=pl
/methodology/chi-square?lang=en
```

**Decyzja:** Path-based — lepsze SEO, czytelniejsze URL-e.

### 2.3 URL Strategy dla Multi-Lottery

```
/app?lottery=lotto_pl              ← Lotto PL (domyślne)
/app?lottery=lotto_plus_pl         ← Lotto Plus PL
/app?lottery=mini_lotto_pl         ← Mini Lotto PL
/app?lottery=eurojackpot           ← Eurojackpot
/app?lottery=powerball_us          ← Powerball US (future)
```

---

## 3. DESIGN SYSTEM

### 3.1 Color Palette

#### Dark Theme (default)
```css
/* Backgrounds */
--bg-primary: #0a0a0f;      /* Main background */
--bg-secondary: #12121a;    /* Cards, elevated surfaces */
--bg-tertiary: #1a1a24;     /* Hover states, inputs */
--bg-elevated: #22222e;     /* Tooltips, dropdowns */

/* Text */
--text-primary: #f8fafc;    /* Headings, important text */
--text-secondary: #94a3b8;  /* Body text */
--text-muted: #64748b;      /* Labels, hints */

/* Borders */
--border-primary: #1e293b;  /* Card borders */
--border-secondary: #334155;/* Input borders, dividers */

/* Accents */
--accent-blue: #3b82f6;     /* Primary actions, links */
--accent-cyan: #06b6d4;     /* Secondary highlights */
--accent-purple: #8b5cf6;   /* Tertiary, methodology */
--accent-green: #10b981;    /* Success, positive */
--accent-amber: #f59e0b;    /* Warning, hot numbers */
--accent-rose: #f43f5e;     /* Error, disclaimer */
```

#### Light Theme
```css
/* Backgrounds */
--bg-primary: #ffffff;
--bg-secondary: #f8fafc;
--bg-tertiary: #f1f5f9;
--bg-elevated: #e2e8f0;

/* Text */
--text-primary: #0f172a;
--text-secondary: #475569;
--text-muted: #94a3b8;

/* Borders */
--border-primary: #e2e8f0;
--border-secondary: #cbd5e1;

/* Accents — slightly darker for contrast */
--accent-blue: #2563eb;
--accent-cyan: #0891b2;
--accent-purple: #7c3aed;
--accent-green: #059669;
--accent-amber: #d97706;
--accent-rose: #e11d48;
```

### 3.2 Typography

```css
/* Font Families */
--font-sans: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;

/* Font Sizes */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 32px;
--text-4xl: 40px;
--text-5xl: 48px;
--text-6xl: 56px;

/* Font Weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line Heights */
--leading-tight: 1.1;
--leading-snug: 1.3;
--leading-normal: 1.6;
--leading-relaxed: 1.7;
--leading-loose: 1.8;
```

### 3.3 Spacing Scale

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
```

### 3.4 Border Radius

```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
--radius-2xl: 20px;
--radius-full: 9999px;
```

### 3.5 Shadows

```css
/* Dark Theme */
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);

/* Light Theme */
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
--shadow-md: 0 4px 16px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.12);
```

### 3.6 Gradients

```css
--gradient-primary: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
--gradient-secondary: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-green) 100%);
--gradient-warning: linear-gradient(135deg, var(--accent-amber) 0%, var(--accent-rose) 100%);
```

---

## 4. COMPONENT LIBRARY

### 4.1 Buttons

| Variant | Use Case | Example |
|---------|----------|---------|
| `btn-primary` | Main CTA | "Otwórz analizator" |
| `btn-ghost` | Secondary action | "Dowiedz się więcej" |
| `btn-icon` | Theme toggle | ☀️/🌙 |

### 4.2 Cards

| Type | Description |
|------|-------------|
| `feature-card` | Funkcje na homepage |
| `method-card` | Metody na /methodology |
| `stat-card` | Statystyki (chi², p-value) |
| `info-card` | Wskazówki, tips |

### 4.3 Forms

| Component | Description |
|-----------|-------------|
| `switch-group` | PL/EN toggle, lottery selector |
| `theme-toggle` | Dark/Light switch |
| `select` | Dropdown (game_type, window_days) |
| `slider` | Monte Carlo simulations count |

### 4.4 Navigation

| Component | Description |
|-----------|-------------|
| `header` | Fixed top navigation |
| `sidebar` | Methodology sidebar (left) |
| `breadcrumb` | Path navigation |
| `footer-nav` | Prev/Next with progress |
| `toc` | Table of contents (right panel) |

### 4.5 Data Display

| Component | Description |
|-----------|-------------|
| `formula-box` | Mathematical formulas |
| `code-block` | Python code examples |
| `lottery-balls` | Visual ball grid |
| `progress-bar` | Reading progress |

---

## 5. PAGE SPECIFICATIONS

### 5.1 Homepage (`/`)

**Cel:** Przyciągnąć, wyjaśnić, przekierować do aplikacji.

**Sekcje:**
1. **Hero** — "Gdzie szczęście spotyka naukę"
   - Headline + subtitle
   - Disclaimer (widoczny od razu!)
   - CTA buttons
   - Quick stats (9,300+ losowań, 68 lat, 12 metod)

2. **Lottery Balls Visual** — animowane kulki
   - Hot/cold visual indicators
   - Mini stats (najczęstsza, najrzadsza, χ², entropy)

3. **Features Grid** — 6 kart funkcji
   - Analiza częstości, Testy losowości, Wzorce...
   - Każda z linkiem do `/app/...`

4. **How It Works** — 4 kroki
   - Zbieramy → Walidujemy → Testujemy → Interpretujemy

5. **Footer** — links, copyright

### 5.2 Methodology Overview (`/methodology`)

**Cel:** Pokazać wszystkie metody, zachęcić do zgłębienia.

**Sekcje:**
1. **Hero** — "Metodologia badawcza"
2. **Hypothesis Box** — H₀ centralnie
3. **Methods Grid** — 6 kart z pytaniem, wzorem, wynikiem
4. **Workflow** — jak przeprowadzamy analizę
5. **Lottery Support** — siatka z flagami (PL, EU, US...)

### 5.3 Methodology Detail (`/methodology/chi-square`)

**Cel:** Szczegółowe wyjaśnienie jednej metody.

**Layout:** 3-kolumnowy
- **Left:** Sidebar navigation
- **Center:** Content (intuition, formula, demo, code)
- **Right:** TOC, tips, related

**Sekcje:**
1. **Intuition** — wyjaśnienie prostym językiem
2. **Formula** — wzór matematyczny
3. **Interactive Demo** — symulator
4. **Interpretation** — co znaczą wyniki
5. **Code** — implementacja Python

### 5.4 App/Analyzer (`/app`)

**Cel:** Główna aplikacja do analizy.

**Layout:** 3-kolumnowy (jak obecnie, ale ulepszony)
- **Left:** Controls (lottery, window_days) + sidebar nav
- **Center:** Main content (charts, tables)
- **Right:** Tips, export buttons, related

**Usprawnienia vs. obecny UI:**
- Lepszy onboarding dla nowych użytkowników
- Tooltips wyjaśniające metryki
- Lazy loading dla dużych wykresów
- Responsywność mobile

---

## 6. I18N STRATEGY

### 6.1 Translation Keys Structure

```python
TRANSLATIONS = {
    "pl": {
        "nav": {
            "home": "Strona główna",
            "methodology": "Metodologia",
            "analyzer": "Analizator",
            "docs": "Dokumentacja"
        },
        "hero": {
            "title": "Gdzie szczęście spotyka naukę",
            "subtitle": "Poznaj matematyczne tajniki loterii...",
            "disclaimer": "To nie jest system do przewidywania wyników."
        },
        "methods": {
            "chi_square": {
                "title": "Test Chi-kwadrat",
                "question": "Czy rozkład częstości jest równomierny?",
                "desc": "Porównuje obserwowane częstości z oczekiwanymi..."
            }
            # ...
        }
    },
    "en": {
        "nav": {
            "home": "Home",
            "methodology": "Methodology",
            "analyzer": "Analyzer",
            "docs": "Documentation"
        }
        # ...
    }
}
```

### 6.2 Language Detection

1. URL path (`/pl/...`, `/en/...`)
2. localStorage preference
3. Browser `Accept-Language` header
4. Default: `pl`

---

## 7. MULTI-LOTTERY SUPPORT

### 7.1 Lottery Configuration

```python
LOTTERY_CONFIG = {
    "lotto_pl": {
        "name": "Lotto",
        "country": "PL",
        "flag": "🇵🇱",
        "format": "6/49",
        "numbers_count": 6,
        "max_number": 49,
        "draw_days": ["tue", "thu", "sat"],
        "status": "active"
    },
    "lotto_plus_pl": {
        "name": "Lotto Plus",
        "country": "PL",
        "flag": "🇵🇱",
        "format": "6/49",
        "numbers_count": 6,
        "max_number": 49,
        "status": "active"
    },
    "eurojackpot": {
        "name": "Eurojackpot",
        "country": "EU",
        "flag": "🇪🇺",
        "format": "5/50 + 2/12",
        "numbers_count": 5,
        "max_number": 50,
        "bonus_count": 2,
        "bonus_max": 12,
        "status": "planned"
    },
    "powerball_us": {
        "name": "Powerball",
        "country": "US",
        "flag": "🇺🇸",
        "format": "5/69 + 1/26",
        "status": "planned"
    }
}
```

### 7.2 UI Lottery Selector

```html
<select id="lottery-selector">
    <optgroup label="🇵🇱 Polska">
        <option value="lotto_pl" selected>Lotto (6/49)</option>
        <option value="lotto_plus_pl">Lotto Plus (6/49)</option>
        <option value="mini_lotto_pl" disabled>Mini Lotto (5/42) — wkrótce</option>
    </optgroup>
    <optgroup label="🇪🇺 Europa">
        <option value="eurojackpot" disabled>Eurojackpot — wkrótce</option>
    </optgroup>
</select>
```

---

## 8. IMPLEMENTATION PLAN

### Phase 1: Design System & Shared CSS (3 days)
- [ ] Create `static/css/design-system.css` with variables
- [ ] Create `static/css/components.css` with reusable components
- [ ] Create `static/css/themes.css` with dark/light variants
- [ ] Add theme toggle to existing UI

### Phase 2: Homepage (2 days)
- [ ] Create `templates/home.html` (new landing page)
- [ ] Add route `/` → homepage (separate from `/app`)
- [ ] Implement hero, features, how-it-works sections

### Phase 3: Methodology Pages (3 days)
- [ ] Create `templates/methodology/index.html` (overview)
- [ ] Create `templates/methodology/detail.html` (base template)
- [ ] Create content for each method (chi-square, KS, runs...)
- [ ] Add sidebar navigation

### Phase 4: App Improvements (2 days)
- [ ] Move current UI to `/app` route
- [ ] Add lottery selector
- [ ] Improve onboarding (tooltips, help)
- [ ] Fix test data cleanup (999997/999998)

### Phase 5: I18n Full Implementation (2 days)
- [ ] Expand `i18n.py` with all new translations
- [ ] Add URL-based language switching (`/pl/...`, `/en/...`)
- [ ] Translate all new pages

---

## 9. FILE STRUCTURE

```
lotterylab/
├── static/
│   ├── css/
│   │   ├── design-system.css   ← NEW: variables, tokens
│   │   ├── components.css      ← NEW: reusable components
│   │   ├── themes.css          ← NEW: dark/light variants
│   │   ├── home.css            ← NEW: homepage styles
│   │   ├── methodology.css     ← NEW: methodology styles
│   │   └── app.css             ← RENAMED from main.css
│   └── js/
│       ├── theme-toggle.js     ← NEW: theme switching
│       └── app.js              ← existing
│
├── templates/
│   ├── base.html               ← UPDATE: add theme support
│   ├── home.html               ← NEW: landing page
│   ├── methodology/
│   │   ├── index.html          ← NEW: overview
│   │   ├── _base.html          ← NEW: detail base
│   │   ├── chi-square.html     ← NEW
│   │   ├── ks-test.html        ← NEW
│   │   └── ...
│   ├── app/
│   │   ├── index.html          ← MOVED from index.html
│   │   └── partials/           ← MOVED
│   └── partials/               ← shared partials
│
├── src/
│   └── utils/
│       └── i18n.py             ← UPDATE: expand translations
```

---

## 10. SUCCESS METRICS

| Metric | Current | Target |
|--------|---------|--------|
| Time to understand (new user) | ~5 min | < 1 min |
| Bounce rate | Unknown | < 40% |
| Pages per session | 1-2 | > 4 |
| Theme preference saved | ❌ | ✅ |
| Mobile usability | Poor | Good |
| Lighthouse Performance | ~70 | > 90 |
| Lighthouse Accessibility | ~80 | > 95 |

---

## 11. DESIGN FILES

| File | Description | Status |
|------|-------------|--------|
| `.design/homepage-v3-themes.html` | Homepage with theme toggle | ✅ Done |
| `.design/methodology-overview-v2.html` | Methodology overview | ✅ Done |
| `.design/methodology-v2.html` | Methodology detail (chi-square) | ✅ Done |
| `.design/app-v2.html` | Analyzer redesign | 📋 TODO |

---

*Dokument przygotowany: Grudzień 2025*  
*Do akceptacji przez: Product Owner*




