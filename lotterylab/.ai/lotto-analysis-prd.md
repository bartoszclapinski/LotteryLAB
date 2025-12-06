
# Product Requirements Document (PRD)
## System Analizy Matematycznej Losowań – Lottery Lab

**Wersja:** 1.0  
**Data:** Wrzesień 2025  
**Status:** Draft

---

## 1. PODSUMOWANIE WYKONAWCZE

### 1.1 Cel Projektu
Stworzenie zaawansowanego systemu analizy statystycznej i matematycznej historycznych danych losowań loterii (start: Lotto w Polsce, z możliwością rozszerzenia na inne gry), umożliwiającego badanie wzorców, testowanie hipotez o losowości oraz wizualizację trendów.

### 1.2 Kluczowe Założenia
- System ma charakter **badawczy i edukacyjny**
- Analiza oparta na rzeczywistych danych historycznych
- Weryfikacja matematycznej losowości systemów loteryjnych
- NIE jest to system do przewidywania wyników

### 1.3 Stack Technologiczny
- **Backend:** Python 3.11+
- **Analiza:** NumPy, Pandas, SciPy, Scikit-learn
- **Wizualizacja:** Plotly, Matplotlib, Seaborn
- **Frontend (public UI):** FastAPI + Jinja2 + HTMX (Python‑first, progresywne ulepszenia)
- **Frontend (research/internal):** Jupyter Notebooks (eksperymenty i szybkie prototypy)
- **Baza danych:** SQLite (dev) / PostgreSQL (prod)
- **API:** FastAPI

---

## 2. ARCHITEKTURA SYSTEMU

### 2.1 Komponenty Główne

```
lottery-lab/
├── .design/                    # Artefakty UI/UX (makiety, prototypy, specyfikacje)
│   └── main-design.html        # Główny szkic interfejsu
├── templates/                  # Szablony Jinja2 (UI publiczne)
├── static/                     # Zasoby statyczne (CSS/JS/obrazy)
├── src/
│   ├── data_acquisition/
│   │   ├── api_client.py         # Klienci API różnych loterii
│   │   ├── file_parser.py        # Parser CSV/TXT/Excel
│   │   ├── data_validator.py     # Walidacja danych
│   │   └── scheduler.py          # Automatyczna aktualizacja
│   │
│   ├── database/
│   │   ├── models.py             # Modele SQLAlchemy
│   │   ├── repository.py         # Warstwa dostępu do danych
│   │   └── migrations/           # Migracje bazy danych
│   │
│   ├── analysis/
│   │   ├── statistical/
│   │   │   ├── frequency.py      # Analiza częstości
│   │   │   ├── distributions.py  # Rozkłady statystyczne
│   │   │   ├── correlation.py    # Korelacje i zależności
│   │   │   └── randomness.py     # Testy losowości
│   │   │
│   │   ├── time_series/
│   │   │   ├── trends.py         # Analiza trendów
│   │   │   ├── seasonality.py    # Sezonowość
│   │   │   ├── arima.py          # Modele ARIMA
│   │   │   └── forecast.py       # Prognozowanie (eksperymentalne)
│   │   │
│   │   ├── patterns/
│   │   │   ├── sequences.py      # Wykrywanie sekwencji
│   │   │   ├── combinations.py   # Analiza kombinacji
│   │   │   ├── gaps.py           # Analiza przerw między wystąpieniami
│   │   │   └── clustering.py     # Grupowanie liczb
│   │   │
│   │   └── advanced/
│   │       ├── ml_models.py      # Modele uczenia maszynowego
│   │       ├── neural_nets.py    # Sieci neuronowe
│   │       ├── chaos_theory.py   # Teoria chaosu
│   │       └── monte_carlo.py    # Symulacje Monte Carlo
│   │
│   ├── visualization/
│   │   ├── charts.py             # Wykresy statyczne
│   │   ├── interactive.py        # Wykresy interaktywne
│   │   ├── heatmaps.py           # Mapy ciepła
│   │   └── dashboard.py          # Materiały pomocnicze (research)
│   │
│   ├── api/
│   │   ├── endpoints.py         # Endpointy REST API
│   │   ├── schemas.py           # Schematy Pydantic
│   │   └── auth.py              # Autentykacja (opcjonalnie)
│   │
│   └── utils/
│       ├── config.py            # Konfiguracja
│       ├── logger.py            # Logowanie
│       └── validators.py        # Walidatory
│
├── tests/
│   ├── unit/                    # Testy jednostkowe
│   ├── integration/             # Testy integracyjne
│   └── fixtures/                # Dane testowe
│
├── notebooks/                   # Jupyter notebooks do eksploracji
├── data/                        # Dane lokalne
├── docs/                        # Dokumentacja
└── docker/                      # Kontenery Docker
```

Nota: Folder `.design/` przechowuje spójne artefakty UI/UX, które będą odwzorowywane w komponentach frontendowych (np. Jinja2+HTMX, notebooks) w kolejnych sprintach.

---

## 3. WYMAGANIA FUNKCJONALNE

### 3.1 Pozyskiwanie Danych

#### F-001: Import Danych Historycznych
- **Opis:** System musi umożliwić import danych z różnych źródeł
- **Źródła:**
  - API Lotto (developers.lotto.pl)
  - Pliki CSV/TXT/Excel
  - Web scraping (jako backup)
- **Kryteria akceptacji:**
  - Obsługa dat od 1957 roku
  - Walidacja integralności danych
  - Obsługa różnych formatów (Lotto, Lotto Plus, Mini Lotto)

#### F-002: Automatyczna Aktualizacja
- **Opis:** Codzienna aktualizacja po losowaniach
- **Harmonogram:** Wtorek, czwartek, sobota po 22:00
- **Retry policy:** 3 próby co 15 minut

### 3.2 Analizy Statystyczne

#### F-003: Analiza Częstości
```python
class FrequencyAnalysis:
    def calculate_frequency(self, date_range=None):
        """Częstość występowania każdej liczby"""
        
    def hot_cold_numbers(self, window_days=30):
        """Gorące i zimne liczby w okresie"""
        
    def expected_vs_actual(self):
        """Porównanie z rozkładem teoretycznym"""
```

#### F-004: Testy Losowości
- Test chi-kwadrat
- Test Kołmogorowa-Smirnowa
- Test serii (runs test)
- Test autokorelacji
- Entropia Shannona
- NIST Statistical Test Suite

#### F-005: Analiza Wzorców
- Sekwencje kolejnych liczb
- Liczby z tej samej dziesiątki
- Rozkład parzystych/nieparzystych
- Sumy wylosowanych liczb
- Rozstęp między liczbami

### 3.3 Analizy Zaawansowane

#### F-006: Machine Learning
```python
class MLAnalysis:
    models = {
        'random_forest': RandomForestClassifier(),
        'xgboost': XGBClassifier(),
        'neural_network': MLPClassifier(),
        'lstm': Sequential()  # dla szeregów czasowych
    }
    
    def train_models(self, features, labels):
        """Trenowanie modeli ML"""
        
    def feature_importance(self):
        """Ważność cech w predykcji"""
        
    def cross_validate(self, cv=5):
        """Walidacja krzyżowa"""
```

#### F-007: Teoria Chaosu
- Wykładnik Lapunowa
- Wymiar fraktalny
- Atraktor dziwny
- Analiza przestrzeni fazowej

### 3.4 Wizualizacje

#### F-008: Dashboard Analityczny / UI Publiczne
- **Komponenty:**
  - Histogram częstości
  - Mapa ciepła korelacji
  - Wykres trendu czasowego
  - Rozkład sum liczb
  - Tabela ostatnich wyników
  - Statystyki podsumowujące

Nota: Publiczny interfejs oparty o FastAPI + Jinja2 + HTMX (lekki, szybki, Python‑first). Jupyter notebooks wykorzystywane wewnętrznie do badań/eksperymentów.

#### F-009: Raporty
- Generowanie PDF z analizami
- Export do Excel
- Interaktywne wykresy HTML

---

## 4. WYMAGANIA NIEFUNKCJONALNE

### 4.1 Wydajność
- Czas ładowania dashboardu < 2s
- Analiza 10,000 losowań < 5s
- Obsługa 100 równoczesnych użytkowników

### 4.2 Skalowalność
- Architektura mikroserwisowa (opcjonalnie)
- Cache Redis dla częstych zapytań
- Możliwość działania w chmurze (AWS/GCP/Azure)

### 4.3 Niezawodność
- Uptime 99.9%
- Backup danych co 24h
- Odtwarzanie po awarii < 1h

### 4.4 Bezpieczeństwo
- Szyfrowanie danych wrażliwych
- Rate limiting API
- Logowanie dostępu
- GDPR compliance

---

## 5. MODELE DANYCH

### 5.1 Schemat Bazy Danych

```sql
-- Tabela główna losowań
CREATE TABLE draws (
    id SERIAL PRIMARY KEY,
    draw_number INTEGER UNIQUE NOT NULL,
    draw_date DATE NOT NULL,
    game_type VARCHAR(20) NOT NULL, -- 'lotto', 'lotto_plus', 'mini_lotto'
    game_provider VARCHAR(50),      -- np. 'pl_totalizator', 'uk_national_lottery'
    numbers INTEGER[] NOT NULL,
    jackpot DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela statystyk liczb
CREATE TABLE number_statistics (
    id SERIAL PRIMARY KEY,
    number INTEGER NOT NULL,
    game_type VARCHAR(20) NOT NULL,
    total_appearances INTEGER DEFAULT 0,
    last_appearance DATE,
    average_gap_days FLOAT,
    max_gap_days INTEGER,
    min_gap_days INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(number, game_type)
);

-- Tabela analiz
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    analysis_type VARCHAR(50) NOT NULL,
    parameters JSONB,
    results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indeksy dla wydajności
CREATE INDEX idx_draws_date ON draws(draw_date);
CREATE INDEX idx_draws_game_type ON draws(game_type);
CREATE INDEX idx_number_stats_appearances ON number_statistics(total_appearances DESC);
```

### 5.2 Modele Pydantic

```python
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class DrawBase(BaseModel):
    draw_number: int
    draw_date: date
    game_type: str
    game_provider: Optional[str]
    numbers: List[int]
    jackpot: Optional[float]

class StatisticsResponse(BaseModel):
    number: int
    frequency: int
    percentage: float
    last_seen_days_ago: int
    is_hot: bool
    is_cold: bool
    
class AnalysisRequest(BaseModel):
    analysis_type: str
    date_from: Optional[date]
    date_to: Optional[date]
    parameters: dict
```

---

## 6. API SPECIFICATION

### 6.1 Endpoints

```yaml
openapi: 3.0.0
info:
  title: Lottery Lab API
  version: 1.0.0

paths:
  /api/v1/draws:
    get:
      summary: Get historical draws
      parameters:
        - name: game_type
          in: query
          schema:
            type: string
            enum: [lotto, lotto_plus, mini_lotto]
        - name: game_provider
          in: query
          schema:
            type: string
        - name: date_from
          in: query
          schema:
            type: string
            format: date
        - name: date_to
          in: query
          schema:
            type: string
            format: date
        - name: limit
          in: query
          schema:
            type: integer
            default: 100

  /api/v1/analysis/frequency:
    get:
      summary: Get frequency analysis
      parameters:
        - name: game_type
          in: query
          schema:
            type: string
            enum: [lotto, lotto_plus, mini_lotto]
        - name: game_provider
          in: query
          schema:
            type: string
        - name: window_days
          in: query
          schema:
            type: integer
            default: 365
        - name: date_from
          in: query
          schema:
            type: string
            format: date
        - name: date_to
          in: query
          schema:
            type: string
            format: date
```

---

## 7. ALGORYTMY KLUCZOWE

### 7.1 Test Losowości Chi-Kwadrat

```python
def chi_square_test(observed_frequencies, expected_frequency=None):
    """
    H0: Rozkład jest równomierny (system jest losowy)
    H1: Rozkład nie jest równomierny
    """
    if expected_frequency is None:
        expected_frequency = sum(observed_frequencies) / len(observed_frequencies)
    
    chi_square = sum((obs - expected_frequency) ** 2 / expected_frequency 
                     for obs in observed_frequencies)
    
    degrees_of_freedom = len(observed_frequencies) - 1
    p_value = 1 - chi2.cdf(chi_square, degrees_of_freedom)
    
    return {
        'chi_square': chi_square,
        'p_value': p_value,
        'is_random': p_value > 0.05,
        'confidence': (1 - p_value) * 100
    }
```

### 7.2 Wykrywanie Anomalii

```python
def detect_anomalies(data, method='isolation_forest'):
    """
    Wykrywanie nietypowych wzorców w losowaniach
    """
    if method == 'isolation_forest':
        from sklearn.ensemble import IsolationForest
        clf = IsolationForest(contamination=0.1)
        predictions = clf.fit_predict(data)
        anomalies = data[predictions == -1]
        
    elif method == 'statistical':
        mean = np.mean(data)
        std = np.std(data)
        threshold = 3  # 3-sigma rule
        anomalies = data[np.abs(data - mean) > threshold * std]
        
    return anomalies
```

### 7.3 Analiza Sekwencji

```python
def analyze_sequences(draws):
    """
    Analiza występowania sekwencji liczb
    """
    patterns = {
        'consecutive_pairs': 0,
        'consecutive_triplets': 0,
        'arithmetic_sequences': 0,
        'same_ending': 0,  # np. 11, 21, 31
        'fibonacci_like': 0
    }
    
    for draw in draws:
        sorted_draw = sorted(draw)
        
        # Consecutive numbers
        for i in range(len(sorted_draw) - 1):
            if sorted_draw[i+1] - sorted_draw[i] == 1:
                patterns['consecutive_pairs'] += 1
                if i < len(sorted_draw) - 2:
                    if sorted_draw[i+2] - sorted_draw[i+1] == 1:
                        patterns['consecutive_triplets'] += 1
        
        # Arithmetic sequences
        for i in range(len(sorted_draw) - 2):
            diff1 = sorted_draw[i+1] - sorted_draw[i]
            diff2 = sorted_draw[i+2] - sorted_draw[i+1]
            if diff1 == diff2 and diff1 > 0:
                patterns['arithmetic_sequences'] += 1
        
        # Same ending digit
        endings = [n % 10 for n in draw]
        if len(endings) != len(set(endings)):
            patterns['same_ending'] += 1
    
    return patterns
```

---

## 8. PLAN IMPLEMENTACJI

### Faza 1: MVP (2-3 tygodnie)
- [ ] Setup projektu i środowiska
- [ ] Implementacja pobierania danych (API + pliki)
- [ ] Podstawowa baza danych
- [ ] Analiza częstości
- [x] Prosty dashboard w FastAPI + Jinja2 + HTMX

### Faza 2: Analizy Podstawowe (2-3 tygodnie)
- [x] Testy losowości (chi-square, KS, runs, autocorr, entropy)
- [ ] Analiza wzorców
- [ ] Wizualizacje zaawansowane
- [x] API REST podstawowe

### Faza 3: Machine Learning (3-4 tygodnie)
- [ ] Przygotowanie features
- [ ] Implementacja modeli ML
- [ ] Walidacja i tuning
- [ ] Analiza feature importance

### Faza 4: Analizy Zaawansowane (3-4 tygodnie)
- [ ] Teoria chaosu
- [ ] Symulacje Monte Carlo
- [ ] Sieci neuronowe (LSTM)
- [ ] Analiza fraktalna

### Faza 5: Produkcja (2 tygodnie)
- [ ] Testy jednostkowe i integracyjne
- [ ] Dokumentacja
- [ ] Docker i CI/CD
- [ ] Deployment

---

## 9. RYZYKA I MITYGACJE

| Ryzyko | Prawdopodobieństwo | Wpływ | Mitygacja |
|--------|-------------------|--------|-----------|
| Zmiana API Lotto | Średnie | Wysoki | Backup sources, web scraping |
| Niewystarczająca moc obliczeniowa | Niskie | Średni | Cloud computing, optymalizacja |
| Brak wzorców (pełna losowość) | Wysokie | Niski | Fokus na weryfikacji losowości |
| GDPR/Legal issues | Niskie | Wysoki | Konsultacja prawna, tylko dane publiczne |

---

## 10. METRYKI SUKCESU

### Metryki Techniczne
- Code coverage > 80%
- Czas odpowiedzi API < 500ms (p95)
- Zero krytycznych bugów w produkcji
- Uptime > 99.9%

### Metryki Biznesowe
- 1000+ użytkowników w pierwszym miesiącu
- 50+ analiz dziennie
- Publikacja 3+ artykułów naukowych
- Pozytywny feedback społeczności

---

## 11. PRZYKŁADOWY KOD STARTOWY

```python
# main.py
import asyncio
from fastapi import FastAPI
from src.data_acquisition import LottoAPIClient
from src.analysis import StatisticalAnalyzer
from src.database import Database

app = FastAPI(title="Lotto Analysis System")

@app.on_event("startup")
async def startup_event():
    # Initialize database
    await Database.init()
    
    # Load historical data
    client = LottoAPIClient(api_key=CONFIG.LOTTO_API_KEY)
    await client.sync_historical_data()

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/v1/analysis/frequency")
async def get_frequency_analysis(
    game_type: str = "lotto",
    days: int = 365
):
    analyzer = StatisticalAnalyzer()
    results = await analyzer.calculate_frequency(
        game_type=game_type,
        days=days
    )
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 12. ZASOBY I ODNIESIENIA

### Dokumentacja
- [Lotto OpenAPI](https://developers.lotto.pl/)
- [NIST Statistical Test Suite](https://csrc.nist.gov/projects/random-bit-generation)
- [SciPy Statistical Functions](https://docs.scipy.org/doc/scipy/reference/stats.html)

### Literatura
- "The Mathematics of Lottery" - Catalin Barboianu
- "Statistical Analysis of Lottery Numbers" - Journal of Statistics
- "Chaos Theory and Randomness" - Edward Lorenz

### Narzędzia
- [HTMX](https://htmx.org/) - Progressive enhancement for web UI
- [FastAPI](https://fastapi.tiangolo.com/) - REST API
- [Plotly](https://plotly.com/) - Visualizations
- [PostgreSQL](https://www.postgresql.org/) - Database

---

## APPENDIX A: SŁOWNIK POJĘĆ

- **Hot Numbers** - Liczby występujące częściej niż średnia w ostatnim okresie
- **Cold Numbers** - Liczby występujące rzadziej niż średnia
- **Draw** - Pojedyncze losowanie
- **Frequency** - Częstość występowania liczby
- **Gap** - Odstęp między wystąpieniami tej samej liczby
- **Pattern** - Powtarzalny wzorzec w danych
- **Entropy** - Miara losowości/nieprzewidywalności systemu

---

## APPENDIX B: STRUKTURA DANYCH WEJŚCIOWYCH

### Format API Lotto
```json
{
  "drawSystemId": 16270,
  "drawDate": "2025-09-02T20:00:00",
  "gameType": "Lotto",
  "results": [1, 3, 6, 7, 13, 16],
  "extraResults": [18],  // dla Lotto Plus
  "jackpot": 2000000.00
}
```

### Format CSV (MBNet)
```
NR_LOSOWANIA;DATA;L1;L2;L3;L4;L5;L6
1;1957-01-27;8;12;17;23;31;37
2;1957-02-03;5;11;14;22;35;41
```

---

## APPENDIX C: BRANDING GUIDELINES

### Logo i Identyfikacja Wizualna
- **Nazwa:** Lottery Lab (Λ)
- **Tagline:** "Where Luck Meets Science"
- **Polski slogan:** "Laboratorium Analizy Loterii"
- **Kolorystyka:** 
  - Primary: Lab Blue (#0066CC)
  - Secondary: Lucky Gold (#FFD700)
  - Accent: Data Green (#00C851)
- **Font:** Roboto dla UI, Fira Code dla kodu

### Messaging
- Podkreślamy **naukowe podejście**
- Używamy terminologii **laboratoryjnej** (eksperymenty, testy, analizy)
- Zawsze dodajemy disclaimer o charakterze **edukacyjnym**
- Unikamy sugestii o "pokonaniu systemu"

### GitHub Repository
- URL: `github.com/[username]/lotterylab`
- Description: "🧪 Lottery Lab - Laboratory for Lottery Analysis. Where Luck Meets Science."
- Topics: `lottery-analysis`, `statistics`, `data-science`, `python`, `education`

---

*Dokument przygotowany dla projektu Lottery Lab*  
*Do użycia z AI assistants (GPT-4, Claude Sonnet, Cursor)*