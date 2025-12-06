# Metody Matematyczne w Projekcie Lottery Lab

## Wprowadzenie

Projekt Lottery Lab to narzędzie do naukowej analizy danych loterii, wykorzystujące rygorystyczne metody statystyczne do weryfikacji hipotezy o losowości wyników. Wszystkie metody służą do **testowania hipotezy zerowej** (H₀): "Wyniki loterii są całkowicie losowe i niezależne".

**Poziom istotności**: α = 0,05 (5% ryzyko błędu I rodzaju)
**Typ testów**: Dwustronne (szukamy zarówno nadmiaru jak i niedoboru wzorców)

---

## 1. Test zgodności χ² (Chi-square Goodness-of-Fit Test)

### Cel
Sprawdza czy rozkład empiryczny (obserwowany) jest zgodny z teoretycznym rozkładem równomiernym.

### Teoria matematyczna
Statystyka testowa:
```
χ² = Σᵢ (Oᵢ - Eᵢ)² / Eᵢ
```
gdzie:
- Oᵢ - obserwowana częstość i-tej kategorii
- Eᵢ - oczekiwana częstość i-tej kategorii
- Stopnie swobody: k-1 (gdzie k = liczba kategorii)

### Przykład obliczeń
Załóżmy lotto 6/49 z 100 losowaniami:

**Dane obserwowane:**
- Liczba 1: 8 razy
- Liczba 2: 5 razy
- Liczba 3: 12 razy
- ... (itd. dla wszystkich 49 liczb)
- Suma wszystkich obserwacji: 600 (100 × 6)

**Oczekiwane częstości:**
Dla rozkładu równomiernego: Eᵢ = 600 / 49 ≈ 12,245 dla każdej liczby

**Obliczenia dla jednej liczby:**
```
χ²_przykład = (8 - 12,245)² / 12,245 + (5 - 12,245)² / 12,245 + (12 - 12,245)² / 12,245 + ...
```

**Interpretacja:**
- χ² > wartość krytyczna → odrzucamy H₀ (rozkład nie jest równomierny)
- χ² ≤ wartość krytyczna → brak podstaw do odrzucenia H₀

### Implementacja w kodzie
```python
def chi_square_goodness_of_fit(observed_frequencies: Dict[int, int]) -> Dict[str, float]:
    total_observations = sum(observed_frequencies.values())
    expected_frequency = total_observations / len(observed_frequencies)

    chi_square = 0
    for observed in observed_frequencies.values():
        chi_square += (observed - expected_frequency) ** 2 / expected_frequency

    # Obliczenie p-value (przybliżenie)
    degrees_of_freedom = len(observed_frequencies) - 1
    # Używamy przybliżenia rozkładu chi-kwadrat

    return {
        "chi_square_statistic": chi_square,
        "degrees_of_freedom": degrees_of_freedom,
        "p_value": p_value,
        "is_random": p_value > 0.05
    }
```

---

## 2. Test Kołmogorowa-Smirnowa (Kolmogorov-Smirnov Test)

### Cel
Porównuje empiryczną dystrybuantę z teoretyczną dystrybuantą rozkładu równomiernego.

### Teoria matematyczna
Statystyka testowa:
```
D = max|Fₙ(x) - F(x)|
```
gdzie:
- Fₙ(x) - empiryczna dystrybuanta (funkcja rozkładu z danych)
- F(x) - teoretyczna dystrybuanta (dla rozkładu równomiernego dyskretnego)

Dla rozkładu równomiernego dyskretnego {1,2,...,49}:
```
F(x) = (floor(x) - 0.5) / 49  dla x ∈ [1,49]
```

### Przykład obliczeń
Mamy próbkę: [5, 12, 23, 34, 41, 49]

**Posortowana próbka:** [5, 12, 23, 34, 41, 49]

**Empiryczna dystrybuanta Fₙ(x):**
- Fₙ(x) = 0 dla x < 5
- Fₙ(x) = 1/6 ≈ 0.167 dla 5 ≤ x < 12
- Fₙ(x) = 2/6 ≈ 0.333 dla 12 ≤ x < 23
- Fₙ(x) = 3/6 = 0.5 dla 23 ≤ x < 34
- Fₙ(x) = 4/6 ≈ 0.667 dla 34 ≤ x < 41
- Fₙ(x) = 5/6 ≈ 0.833 dla 41 ≤ x < 49
- Fₙ(x) = 1 dla x ≥ 49

**Teoretyczna dystrybuanta F(x) dla rozkładu równomiernego:**
- F(x) = (floor(x) - 0.5) / 49

**Statystyka D:**
D = max |Fₙ(x) - F(x)| dla wszystkich x

### Implementacja w kodzie
```python
def kolmogorov_smirnov_test(observed_frequencies: Dict[int, int]) -> Dict[str, float]:
    # Konwersja częstości na próbkę
    sample = []
    for number, freq in observed_frequencies.items():
        sample.extend([number] * freq)

    sample.sort()
    n = len(sample)

    # Obliczenie statystyki KS
    ks_statistic = 0
    for i, x in enumerate(sample):
        # Empiryczna dystrybuanta
        empirical = (i + 1) / n
        # Teoretyczna dystrybuanta (równomierna)
        theoretical = (x - 0.5) / 49  # dla lotto 6/49

        ks_statistic = max(ks_statistic, abs(empirical - theoretical))

    # Przybliżone p-value dla dużej próbki
    p_value = 2 * math.exp(-2 * n * ks_statistic**2)

    return {
        "ks_statistic": ks_statistic,
        "p_value": p_value,
        "appears_random": p_value > 0.05
    }
```

---

## 3. Test serii (Runs Test)

### Cel
Sprawdza czy sekwencja binarna jest losowa (czy nie ma zbyt długich serii takich samych wartości).

### Teoria matematyczna
Dla sekwencji binarnej (0,1):

**Liczba serii R:**
- Seria to maksymalny ciąg identycznych wartości
- Przykład: 001110011 → serie: 00, 111, 00, 11 → R = 4

**Statystyki dla dużej próbki:**
```
μ_R = (2n₁n₂)/(n₁+n₂) + 1
σ_R = √[(2n₁n₂(2n₁n₂ - n₁ - n₂))/((n₁+n₂)²(n₁+n₂-1))]
Z = (R - μ_R) / σ_R
```

### Warianty testu w projekcie

#### a) Test mediany
Konwertuje liczby na wartości binarne względem mediany wszystkich możliwych liczb.

**Przykład:**
Dla lotto 6/49, mediana = 25
Liczby [3, 15, 28, 35, 42, 49] → [0, 0, 1, 1, 1, 1] (0=poniżej mediany, 1=powyżej)

#### b) Test parzystości
Konwertuje na parzyste/nieparzyste:
[3, 15, 28, 35, 42, 49] → [0, 0, 1, 0, 1, 0] (0=nieparzyste, 1=parzyste)

#### c) Test pozycji (wysoka/niska)
Dzieli na dwie grupy:
[3, 15, 28, 35, 42, 49] → [0, 0, 0, 1, 1, 1] (0=1-25, 1=26-49)

#### d) Test kolejności (rosnąca)
Sprawdza czy kolejne liczby rosną:
[3, 15, 28, 35, 42, 49] → [1, 1, 1, 1, 1] (1=rosnące, 0=malejące)

### Przykład obliczeń
Dla sekwencji: [0,0,1,1,1,0,0,0,1,1]

**Analiza serii:**
- Serie: 00, 111, 000, 11
- R = 4 serie
- n₁ = 6 (zer), n₂ = 4 (jedynki)
- n = 10

**Obliczenia:**
```
μ_R = (2×6×4)/10 + 1 = 48/10 + 1 = 5.8
σ_R = √[(2×6×4×(2×6×4 - 6 - 4))/((10)²×9)] = √[192×(48-10)/(100×9)] = √[192×38/900] = √[7296/900] = √8.107 ≈ 2.847
Z = (4 - 5.8) / 2.847 ≈ (-1.8) / 2.847 ≈ -0.632
p-value ≈ 0.527 (z tabeli normalnej)
```

### Implementacja w kodzie
```python
def runs_test(draw_sequence: List[int], test_type: str = "median") -> Dict[str, float]:
    # Konwersja na sekwencję binarną
    if test_type == "median":
        median = 25  # dla lotto 6/49
        binary_sequence = [1 if x > median else 0 for x in draw_sequence]
    elif test_type == "even_odd":
        binary_sequence = [1 if x % 2 == 0 else 0 for x in draw_sequence]
    # ... inne typy

    # Obliczenie liczby serii
    runs = 1  # zawsze co najmniej jedna seria
    for i in range(1, len(binary_sequence)):
        if binary_sequence[i] != binary_sequence[i-1]:
            runs += 1

    n1 = sum(binary_sequence)
    n2 = len(binary_sequence) - n1

    # Statystyki
    expected_runs = (2 * n1 * n2) / (n1 + n2) + 1
    variance = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    std_dev = math.sqrt(variance)

    z_score = (runs - expected_runs) / std_dev if std_dev > 0 else 0

    # p-value (dwustronny test)
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    return {
        "observed_runs": runs,
        "expected_runs": expected_runs,
        "z_score": z_score,
        "p_value": p_value,
        "appears_random": p_value > 0.05
    }
```

---

## 4. Analiza autokorelacji (Autocorrelation Analysis)

### Cel
Sprawdza czy są zależności liniowe między wartościami oddalonymi o k kroków czasowych.

### Teoria matematyczna
Współczynnik autokorelacji r_k:
```
r_k = Σᵢ (xᵢ - μ)(x_{i+k} - μ) / Σᵢ (xᵢ - μ)²
```

**Test istotności:**
```
t = r_k * √(n-k-2) / √(1-r_k²)
```
Rozkład t-Studenta z (n-k-2) stopniami swobody.

### Przykład obliczeń
Mamy sekwencje losowań (pierwsze liczby z każdego losowania):
[5, 12, 23, 34, 41, 49, 3, 15, 28, 35]

**Średnia:** μ = (5+12+23+34+41+49+3+15+28+35)/10 = 245/10 = 24.5

**Autokorelacja dla lag=1:**
```
r₁ = Σ(xᵢ - 24.5)(x_{i+1} - 24.5) / Σ(xᵢ - 24.5)²

Obliczenia:
(5-24.5)(12-24.5) + (12-24.5)(23-24.5) + ... + (28-24.5)(35-24.5)
= (-19.5)(-12.5) + (-12.5)(-1.5) + ... + (3.5)(10.5)
= 243.75 + 18.75 + ... + 36.75

Sumy kwadratów odchyleń: Σ(xᵢ - 24.5)² ≈ 2875.5
```

**Test istotności:**
```
t = r₁ * √(10-1-2) / √(1-r₁²) = r₁ * √7 / √(1-r₁²)
p-value = 2 × P(T > |t|) gdzie T ~ t(7)
```

### Implementacja w kodzie
```python
def autocorrelation_test(draw_sequence: List[int], lags: List[int] = None) -> Dict[str, Any]:
    if lags is None:
        max_lags = min(10, len(draw_sequence) // 3)
        lags = list(range(1, max_lags + 1))

    n = len(draw_sequence)
    mean = np.mean(draw_sequence)

    results = {}
    significant_lags = []

    for lag in lags:
        if lag >= n:
            continue

        # Obliczenie współczynnika autokorelacji
        numerator = 0
        denominator = 0

        for i in range(n - lag):
            numerator += (draw_sequence[i] - mean) * (draw_sequence[i + lag] - mean)
            denominator += (draw_sequence[i] - mean) ** 2

        if denominator == 0:
            r = 0
        else:
            r = numerator / denominator

        # Test istotności
        if n - lag - 2 > 0:
            t_stat = r * math.sqrt(n - lag - 2) / math.sqrt(1 - r**2) if abs(r) < 1 else 0
            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - lag - 2))
        else:
            p_value = 1.0

        results[f'lag_{lag}'] = {
            'autocorrelation': r,
            'p_value': p_value,
            'significant': p_value < 0.05
        }

        if p_value < 0.05:
            significant_lags.append(lag)

    return {
        'autocorrelations': results,
        'significant_lags': significant_lags,
        'sample_size': n,
        'overall_significance': len(significant_lags) == 0
    }
```

---

## 5. Entropia Shannona (Shannon Entropy)

### Cel
Mierzy różnorodność lub "przypadkowość" rozkładu częstości.

### Teoria matematyczna
Entropia Shannona:
```
H = -Σᵢ pᵢ × log₂(pᵢ)
```
gdzie pᵢ - prawdopodobieństwo wystąpienia i-tej kategorii.

**Własności:**
- Maksymalna entropia: log₂(k) dla rozkładu równomiernego
- Minimalna entropia: 0 gdy jedna kategoria ma p=1
- Dla lotto 6/49: H_max = log₂(49) ≈ 5.614 bitów

### Przykład obliczeń
Częstości dla liczb 1-5 (pozostałe = 0):
[20, 15, 10, 5, 0, 0, 0, 0, 0] (suma=50)

**Prawdopodobieństwa:**
p₁ = 20/50 = 0.4
p₂ = 15/50 = 0.3
p₃ = 10/50 = 0.2
p₄ = 5/50 = 0.1
p₅+ = 0

**Entropia:**
```
H = -[0.4×log₂(0.4) + 0.3×log₂(0.3) + 0.2×log₂(0.2) + 0.1×log₂(0.1)]
  = -[0.4×(-1.3219) + 0.3×(-1.7370) + 0.2×(-2.3219) + 0.1×(-3.3219)]
  = -[-0.5288 - 0.5211 - 0.4644 - 0.3322]
  = -[-1.8465] = 1.8465 bitów
```

**Interpretacja:**
- H = 1.85 bitów (dużo mniej niż maksymalne 5.61)
- Rozkład jest skoncentrowany na kilku liczbach
- System nie jest maksymalnie losowy

### Implementacja w kodzie
```python
def shannon_entropy(frequencies: Dict[int, int]) -> float:
    total = sum(frequencies.values())
    if total == 0:
        return 0.0

    entropy = 0.0
    for count in frequencies.values():
        if count > 0:
            probability = count / total
            entropy -= probability * math.log2(probability)

    return entropy

def calculate_entropy_randomness(frequencies: Dict[int, int]) -> Dict[str, float]:
    observed_entropy = shannon_entropy(frequencies)
    max_entropy = math.log2(len(frequencies))  # dla rozkładu równomiernego
    normalized_entropy = observed_entropy / max_entropy if max_entropy > 0 else 0

    return {
        'shannon_entropy': observed_entropy,
        'max_entropy': max_entropy,
        'normalized_entropy': normalized_entropy,
        'entropy_ratio': observed_entropy / max_entropy,
        'appears_random': normalized_entropy > 0.9  # heurystyka
    }
```

---

## 6. Analiza częstości (Frequency Analysis)

### Cel
Identyfikuje liczby, które wypadają częściej lub rzadziej niż oczekiwano.

### Teoria matematyczna
**Test proporcji:**
```
Z = (p̂ - p₀) / √(p₀(1-p₀)/n)
```
gdzie:
- p̂ - obserwowana proporcja
- p₀ - oczekiwana proporcja (1/49 dla lotto)
- n - liczba obserwacji

**Klasyfikacja:**
- **Gorące liczby**: p̂ > p₀ + 2σ (wypadają znacząco częściej)
- **Zimne liczby**: p̂ < p₀ - 2σ (wypadają znacząco rzadziej)

### Przykład obliczeń
100 losowań lotto 6/49 (600 liczb):

**Dla liczby 7:**
- Obserwowana częstość: 15 razy
- Oczekiwana częstość: 600 × (1/49) ≈ 12.245
- p̂ = 15/600 = 0.025
- p₀ = 1/49 ≈ 0.0204

**Statystyka Z:**
```
Z = (0.025 - 0.0204) / √(0.0204 × 0.9796 / 600)
  = 0.0046 / √(0.0200 / 600)
  = 0.0046 / √0.0000333
  = 0.0046 / 0.00577 ≈ 0.797
```

**Interpretacja:**
Z = 0.797 < 1.96 → brak istotnej różnicy od oczekiwanej częstości.

### Implementacja w kodzie
```python
def analyze_frequency_hotspots(draws_data: List[Dict]) -> Dict[str, Any]:
    # Ekstrakcja wszystkich liczb
    all_numbers = []
    for draw in draws_data:
        numbers_str = draw.get('numbers', '')
        numbers = [int(x.strip()) for x in numbers_str.split(',') if x.strip()]
        all_numbers.extend(numbers)

    total_draws = len(draws_data)
    total_numbers = len(all_numbers)
    expected_per_number = total_numbers / 49  # dla lotto 6/49

    # Obliczenie częstości
    from collections import Counter
    frequencies = Counter(all_numbers)

    hot_numbers = []
    cold_numbers = []

    for number in range(1, 50):
        observed = frequencies.get(number, 0)
        expected = expected_per_number

        # Test proporcji
        p_hat = observed / total_numbers
        p0 = 1/49

        if total_numbers > 0:
            se = math.sqrt(p0 * (1 - p0) / total_numbers)
            z_score = (p_hat - p0) / se if se > 0 else 0
        else:
            z_score = 0

        # Klasyfikacja
        if z_score > 2.0:  # 95% przedział ufności
            hot_numbers.append({
                'number': number,
                'frequency': observed,
                'expected': expected,
                'z_score': z_score,
                'deviation': observed - expected
            })
        elif z_score < -2.0:
            cold_numbers.append({
                'number': number,
                'frequency': observed,
                'expected': expected,
                'z_score': z_score,
                'deviation': observed - expected
            })

    return {
        'total_draws': total_draws,
        'total_numbers': total_numbers,
        'expected_per_number': expected_per_number,
        'hot_numbers': sorted(hot_numbers, key=lambda x: x['z_score'], reverse=True),
        'cold_numbers': sorted(cold_numbers, key=lambda x: x['z_score']),
        'analysis_summary': {
            'hot_count': len(hot_numbers),
            'cold_count': len(cold_numbers),
            'normal_count': 49 - len(hot_numbers) - len(cold_numbers)
        }
    }
```

---

## 7. Analiza korelacji (Correlation Analysis)

### Cel
Sprawdza liniowe zależności między wystąpieniami różnych liczb.

### Teoria matematyczna
**Współczynnik korelacji Pearsona:**
```
r = Σᵢ (xᵢ - μ_x)(yᵢ - μ_y) / √[Σᵢ(xᵢ - μ_x)² × Σᵢ(yᵢ - μ_y)²]
```

**Test istotności:**
```
t = r × √(n-2) / √(1-r²)
```
Rozkład t-Studenta z (n-2) stopniami swobody.

### Przykład obliczeń
Macierz 3×3 dla liczb 1,2,3:

**Dane binarne (obecność w losowaniu):**
```
Losowanie 1: [1, 0, 1]  # liczby 1 i 3
Losowanie 2: [0, 1, 1]  # liczby 2 i 3
Losowanie 3: [1, 1, 0]  # liczby 1 i 2
Losowanie 4: [0, 0, 1]  # liczba 3
```

**Korelacja między liczbami 1 i 3:**
Średnie: μ₁ ≈ 0.5, μ₃ ≈ 0.75

```
r₁₃ = Σ(x₁-0.5)(x₃-0.75) / √[Σ(x₁-0.5)² × Σ(x₃-0.75)²]
    = [(1-0.5)(1-0.75) + (0-0.5)(1-0.75) + (1-0.5)(0-0.75) + (0-0.5)(1-0.75)]
    = [0.5×0.25 + (-0.5)×0.25 + 0.5×(-0.75) + (-0.5)×0.25]
    = [0.125 - 0.125 - 0.375 - 0.125] = -0.5

    Licznik: -0.5
    Mianownik: √[Σ(x₁-0.5)² × Σ(x₃-0.75)²] = √[(0.25+0.25+0.25+0.25) × (0.0625+0.0625+0.5625+0.0625)]
    Mianownik: √[1 × 0.75] = √0.75 ≈ 0.866

    r₁₃ = -0.5 / 0.866 ≈ -0.577
```

### Implementacja w kodzie
```python
def calculate_number_correlations(session, game_type="lotto", window_days=None):
    # Pobieranie danych losowań
    repo = DrawRepository(session)
    draws = repo.list(limit=5000, game_type=game_type)

    # Konwersja na macierz binarną
    all_numbers = sorted(set(num for draw in draws
                           for num in draw['numbers'].split(',')))
    number_to_idx = {num: idx for idx, num in enumerate(all_numbers)}

    presence_matrix = np.zeros((len(draws), len(all_numbers)))
    for draw_idx, draw in enumerate(draws):
        numbers = [int(x.strip()) for x in draw['numbers'].split(',') if x.strip()]
        for num in numbers:
            if str(num) in number_to_idx:
                presence_matrix[draw_idx, number_to_idx[str(num)]] = 1

    # Macierz korelacji
    corr_matrix = np.corrcoef(presence_matrix.T)

    # Analiza par z istotną korelacją
    significant_pairs = []
    n = len(draws)

    for i in range(len(all_numbers)):
        for j in range(i + 1, len(all_numbers)):
            corr_value = corr_matrix[i, j]

            # Test istotności (przybliżony)
            if n > 2:
                t_stat = abs(corr_value) * math.sqrt(n - 2) / math.sqrt(1 - corr_value**2)
                p_value = 2 * (1 - stats.t.cdf(t_stat, n - 2))
            else:
                p_value = 1.0

            if abs(corr_value) >= 0.05:  # próg minimalny
                significant_pairs.append({
                    'number1': int(all_numbers[i]),
                    'number2': int(all_numbers[j]),
                    'correlation': float(corr_value),
                    'p_value': float(p_value),
                    'significant': p_value < 0.05
                })

    return {
        'correlation_matrix': {all_numbers[i]: {all_numbers[j]: float(corr_matrix[i,j])
                                              for j in range(len(all_numbers))}
                             for i in range(len(all_numbers))},
        'significant_pairs': significant_pairs,
        'summary_stats': {
            'average_correlation': float(np.mean(corr_matrix[np.triu_indices_from(corr_matrix, k=1)])),
            'max_correlation': float(np.max(corr_matrix)),
            'min_correlation': float(np.min(corr_matrix))
        }
    }
```

---

## 8. Wykrywanie wzorców (Pattern Detection)

### a) Wzorce kolejnych liczb
**Algorytm:** Posortowane liczby, szukanie ciągów z różnicą = 1.

```python
def detect_consecutive_numbers(draw_sequence: List[int]) -> Dict[str, Any]:
    sorted_nums = sorted(draw_sequence)
    sequences = []

    current_seq = [sorted_nums[0]]
    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] == current_seq[-1] + 1:
            current_seq.append(sorted_nums[i])
        else:
            if len(current_seq) >= 2:  # minimum 2 liczby
                sequences.append(current_seq)
            current_seq = [sorted_nums[i]]

    if len(current_seq) >= 2:
        sequences.append(current_seq)

    return {
        'total_sequences': len(sequences),
        'max_length': max(len(seq) for seq in sequences) if sequences else 0,
        'avg_length': sum(len(seq) for seq in sequences) / len(sequences) if sequences else 0,
        'sequences': sequences
    }
```

### b) Sekwencje arytmetyczne
**Algorytm:** Sprawdzanie stałej różnicy między kolejnymi liczbami.

```python
def detect_arithmetic_sequences(draws: List[List[int]]) -> Dict[str, Any]:
    sequences_found = []

    for draw in draws:
        sorted_draw = sorted(draw)

        # Sprawdzaj wszystkie możliwe podciągi
        for start in range(len(sorted_draw)):
            for end in range(start + 3, len(sorted_draw) + 1):  # min 3 liczby
                subsequence = sorted_draw[start:end]

                # Sprawdź czy jest arytmetyczna
                if len(subsequence) >= 3:
                    diffs = [subsequence[i+1] - subsequence[i] for i in range(len(subsequence)-1)]
                    if all(d == diffs[0] for d in diffs):  # stała różnica
                        sequences_found.append({
                            'draw': draw,
                            'sequence': subsequence,
                            'common_difference': diffs[0],
                            'length': len(subsequence)
                        })

    return {
        'total_sequences': len(sequences_found),
        'sequences_found': sequences_found,
        'common_differences': dict(Counter(seq['common_difference'] for seq in sequences_found))
    }
```

### c) Wzorce cyfrowe
**Algorytm:** Analiza częstości cyfr 0-9 w liczbach.

```python
def detect_digit_patterns(draw_sequence: List[int]) -> Dict[str, Any]:
    all_digits = []
    for number in draw_sequence:
        all_digits.extend([int(d) for d in str(number)])

    digit_freq = Counter(all_digits)

    # Znajdź powtarzające się cyfry
    repeating_digits = {digit: count for digit, count in digit_freq.items() if count > 1}

    return {
        'digit_frequencies': dict(digit_freq),
        'repeating_digits': repeating_digits,
        'total_digits': len(all_digits),
        'unique_digits': len(digit_freq)
    }
```

### d) Wzorce sum
**Algorytm:** Analiza rozkładu sum wszystkich liczb w losowaniu.

```python
def detect_sum_patterns(draws: List[List[int]]) -> Dict[str, Any]:
    sums = []
    for draw in draws:
        draw_sums = sum(int(x) for x in draw if x)
        sums.append(draw_sums)

    sum_freq = Counter(sums)
    most_common = sum_freq.most_common(10)

    return {
        'sum_range': (min(sums), max(sums)),
        'most_common_sums': dict(most_common),
        'sum_distribution': dict(sum_freq),
        'total_draws': len(sums),
        'average_sum': sum(sums) / len(sums),
        'median_sum': sorted(sums)[len(sums)//2]
    }
```

---

## Podsumowanie metodologiczne

### Filozofia statystyczna
- **Hipoteza zerowa (H₀):** Wyniki loterii są całkowicie losowe i niezależne
- **Poziom istotności:** α = 0,05 (5% ryzyko błędu)
- **Korekta wielokrotnych porównań:** Metoda Bonferroniego gdzie potrzebne
- **Typy testów:** Dwustronne (szukamy zarówno nadmiaru jak i niedoboru wzorców)

### Własności matematyczne
- **Niezależność zdarzeń:** Brak autokorelacji między losowaniami
- **Rozkład równomierny:** Każda liczba ma takie samo prawdopodobieństwo
- **Brak pamięci:** Wyniki przeszłe nie wpływają na przyszłe
- **Niezależność liczb:** Brak korelacji między wystąpieniami różnych liczb

### Zastosowania praktyczne
1. **Weryfikacja losowości:** Potwierdzenie że loteria jest uczciwa
2. **Edukacja statystyczna:** Nauczanie metod statystycznych na realnych danych
3. **Badania naukowe:** Analiza właściwości generatorów liczb losowych
4. **Walidacja modeli:** Testowanie założeń probabilistycznych

**⚠️ Ważne zastrzeżenie:** Wszystkie te metody służą wyłącznie do analizy statystycznej i weryfikacji hipotezy o losowości. Nie mogą być używane do przewidywania przyszłych wyników loterii.
