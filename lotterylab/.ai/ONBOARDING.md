# 🚀 LLM Onboarding Guide — Lottery Lab

> Ten plik jest przeznaczony dla asystentów AI (Claude, GPT-4, Cursor) rozpoczynających pracę nad projektem.

---

## 📋 Quick Start Checklist

```
1. Przeczytaj ten plik (ONBOARDING.md)
2. Przejrzyj ROADMAP.md — zobacz gdzie jesteśmy
3. Sprawdź BACKLOG.md — co jest do zrobienia
4. Przeczytaj log.md — ostatnie zmiany
5. Zapoznaj się z lotto-analysis-prd.md — pełny PRD
```

---

## 🎯 O Projekcie

**Lottery Lab** to system analizy statystycznej losowań loterii (Lotto PL).

### Kluczowe założenia:
- ✅ Charakter **edukacyjny i badawczy**
- ✅ Analiza oparta na **rzeczywistych danych historycznych** (~9300+ losowań)
- ✅ Weryfikacja matematycznej **losowości** systemów
- ❌ NIE jest to system do przewidywania wyników!

### Tech Stack:
| Warstwa | Technologia |
|---------|-------------|
| Backend | Python 3.11+, FastAPI |
| Frontend | Jinja2 + HTMX + Plotly.js |
| Database | SQLite (dev), PostgreSQL (prod) |
| ORM | SQLAlchemy + Alembic |
| Tests | pytest (79%+ coverage) |
| i18n | Custom dict-based (PL/EN) |

---

## 📁 Struktura Projektu

```
LotteryLAB/                     # Root repozytorium
└── lotterylab/                 # Główny katalog projektu
    ├── .ai/                    # 📚 Dokumentacja AI/LLM
    │   ├── ONBOARDING.md       # ← TEN PLIK
    │   ├── lotto-analysis-prd.md  # PRD (wymagania)
    │   ├── mathematical-methods.md # Metody statystyczne
    │   └── sprints/            # Plany sprintów
    │       ├── ROADMAP.md      # Mapa drogowa
    │       ├── BACKLOG.md      # Backlog produktu
    │       ├── log.md          # Log zmian
    │       └── sprint00X/      # Plany poszczególnych sprintów
    │
    ├── .design/                # 🎨 Makiety UI
    │   └── main-design-1.1.html  # Aktualny design reference
    │
    ├── src/                    # 🐍 Kod źródłowy
    │   ├── api/
    │   │   ├── main.py         # FastAPI app + endpointy + partiale HTMX
    │   │   └── schemas.py      # Pydantic schemas
    │   ├── analysis/
    │   │   ├── frequency.py    # Analiza częstotliwości
    │   │   ├── randomness.py   # Testy losowości (chi-sq, KS, runs)
    │   │   ├── patterns.py     # Wykrywanie wzorców
    │   │   └── visualizations.py # Wizualizacje (korelacja, trendy)
    │   ├── data_acquisition/
    │   │   ├── file_parser.py  # Parser TXT/CSV
    │   │   ├── data_validator.py
    │   │   └── scheduler.py    # Auto-update z MBNet
    │   ├── database/
    │   │   ├── models.py       # SQLAlchemy models
    │   │   ├── session.py      # DB session
    │   │   └── base.py
    │   ├── repositories/
    │   │   └── draws.py        # Repository pattern dla draws
    │   ├── services/
    │   │   ├── ingestion.py    # Import danych
    │   │   └── export.py       # PDF/Excel export
    │   └── utils/
    │       ├── config.py       # Konfiguracja
    │       ├── i18n.py         # Internacjonalizacja (PL/EN)
    │       └── logger.py       # Logowanie
    │
    ├── templates/              # 🖼️ Szablony Jinja2
    │   ├── index.html          # Główna strona
    │   └── partials/           # HTMX partiale
    │       ├── frequency.html
    │       ├── randomness.html
    │       ├── patterns.html
    │       ├── correlation.html
    │       ├── trends.html
    │       ├── generator.html
    │       ├── recent_draws.html
    │       └── stats.html
    │
    ├── static/                 # 📦 Zasoby statyczne
    │   ├── css/main.css
    │   ├── js/app.js
    │   └── favicon.svg
    │
    ├── tests/                  # 🧪 Testy
    │   ├── conftest.py
    │   ├── test_api.py
    │   ├── test_frequency.py
    │   ├── test_randomness.py
    │   └── ...
    │
    ├── scripts/                # 🔧 Skrypty pomocnicze
    │   ├── update_mbnet.py     # Aktualizacja danych
    │   └── import_txt.py       # Import początkowy
    │
    ├── alembic/                # 🗃️ Migracje bazy danych
    │
    ├── Makefile                # 🎯 Komendy make
    ├── requirements.txt        # 📋 Zależności
    ├── pyproject.toml          # 📦 Konfiguracja projektu
    └── lotterylab.db           # 💾 Baza SQLite (dev)
```

---

## 🏃 Uruchomienie Projektu

### 1. Instalacja zależności
```bash
cd lotterylab
pip install -r requirements.txt
```

### 2. Inicjalizacja bazy (jeśli nowa)
```bash
cd ..  # wróć do LotteryLAB/
alembic upgrade head
```

### 3. Import danych (jeśli pusta baza)
```bash
cd lotterylab
python scripts/update_mbnet.py
```

### 4. Uruchomienie serwera
```bash
cd lotterylab
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8001 --reload
```

### 5. Otwórz w przeglądarce
```
http://127.0.0.1:8001
```

---

## 🛠️ Komendy Make

```bash
make help        # Lista wszystkich komend
make dev         # Uruchom serwer deweloperski
make test        # Uruchom testy
make coverage    # Testy z coverage
make update      # Pobierz nowe losowania z MBNet
make lint        # Sprawdź kod (ruff)
make format      # Formatuj kod (black)
```

---

## 📝 Konwencje Kodowania

### Python
- **Style**: PEP 8, Black formatter
- **Docstrings**: Google style
- **Type hints**: Wymagane dla funkcji publicznych
- **Imports**: Sortowane przez isort

### Nazewnictwo
- `snake_case` dla funkcji i zmiennych
- `PascalCase` dla klas
- `UPPER_SNAKE_CASE` dla stałych

### Git
- Branch naming: `feature/nazwa-feature`, `fix/opis-buga`
- Commit messages: Konwencjonalne (feat:, fix:, docs:, refactor:)
- PR do `develop`, potem do `master`

---

## 🔄 Wzorzec Implementacji Endpointu

Każdy nowy endpoint analityczny wymaga:

### 1. Funkcja analizy (`src/analysis/`)
```python
def analyze_something(session, game_type: str, window_days: int) -> dict:
    """Analiza czegoś."""
    # ... logika ...
    return {"key": "value", "game_type": game_type}
```

### 2. API endpoint (`src/api/main.py`)
```python
@app.get("/api/v1/analysis/something")
async def something_analysis(game_type: str = "lotto", window_days: int = 365):
    with SessionLocal() as session:
        return analyze_something(session, game_type, window_days)
```

### 3. HTMX partial endpoint (`src/api/main.py`)
```python
@app.get("/partials/something", response_class=HTMLResponse)
async def something_partial(request: Request, game_type: str = "lotto", window_days: int = 365):
    with SessionLocal() as session:
        result = analyze_something(session, game_type, window_days)
    
    # WAŻNE: Usuń klucze które kolidują z template context!
    result.pop("game_type", None)
    result.pop("window_days", None)
    
    ctx = get_template_context(
        request,
        game_type=game_type,
        window_days=window_days,
        **result
    )
    return templates.TemplateResponse("partials/something.html", ctx)
```

### 4. Szablon Jinja2 (`templates/partials/something.html`)
```html
<div class="card" id="something">
  <h2>{{ something_title }}</h2>
  <!-- treść -->
</div>
```

### 5. Tłumaczenia (`src/utils/i18n.py`)
```python
TRANSLATIONS = {
    "pl": {
        "something_title": "Analiza czegoś",
    },
    "en": {
        "something_title": "Something Analysis",
    }
}
```

### 6. Sidebar link (`templates/index.html`)
```html
<a href="#" class="sidebar-item" 
   hx-get="/partials/something" 
   hx-target="#main-content" 
   hx-swap="innerHTML">
  <span>📊</span>
  <span>{{ something_title }}</span>
  <span class="duration">10 min</span>
</a>
```

### 7. Test (`tests/test_something.py`)
```python
def test_analyze_something(test_session):
    result = analyze_something(test_session, "lotto", 365)
    assert "key" in result
```

---

## ⚠️ Znane Pułapki

### 1. Konflikt `**result` w template context
Gdy przekazujesz `**result` do `get_template_context()`, usuń najpierw klucze które są też przekazywane explicite:
```python
result.pop("game_type", None)
result.pop("window_days", None)
# dopiero teraz: **result
```

### 2. Ścieżka do bazy danych
- Baza jest w `lotterylab/lotterylab.db`
- Alembic uruchamiaj z `LotteryLAB/` (root), nie z `lotterylab/`

### 3. Cache JavaScript w przeglądarce
Przy zmianach w `app.js`, zwiększ wersję cache-buster:
```html
<script src="/static/js/app.js?v=5" defer></script>
```

### 4. Zamykający tag `</script>`
Zawsze sprawdź czy `<script>` ma zamykający tag!

---

## 📊 Aktualny Status (Grudzień 2025)

### Ukończone Sprinty
- ✅ **Sprint 000** — Scaffolding, DB, import CSV
- ✅ **Sprint 001** — MVP (UI, API, frequency analysis)
- ✅ **Sprint 002** — Core Analyses (randomness, patterns, correlation, trends, export)

### Następny Sprint
- 📋 **Sprint 003** — ML Baseline (feature engineering, RF/XGB/MLP, backtesting)

### Kluczowe Metryki
- 📈 ~9300+ losowań w bazie
- 🧪 78+ testów, 79% coverage
- 🌍 i18n: Polski (default) + English
- 📱 Responsywne UI (desktop-first)

---

## 🔗 Przydatne Linki

- **PRD**: `.ai/lotto-analysis-prd.md`
- **Metody matematyczne**: `.ai/mathematical-methods.md`
- **Roadmap**: `.ai/sprints/ROADMAP.md`
- **Backlog**: `.ai/sprints/BACKLOG.md`
- **Design reference**: `.design/main-design-1.1.html`

---

## ❓ FAQ

### Jak dodać nowe tłumaczenie?
Edytuj `src/utils/i18n.py` → `TRANSLATIONS` dict, dodaj klucz dla `pl` i `en`.

### Jak uruchomić jeden test?
```bash
pytest tests/test_api.py::test_frequency_endpoint -v
```

### Gdzie jest główny plik API?
`src/api/main.py` — zawiera FastAPI app, wszystkie endpointy i partiale HTMX.

### Jak zaktualizować bazę danych?
```bash
make update  # lub: python scripts/update_mbnet.py
```

---

*Ostatnia aktualizacja: 2025-12-10*














