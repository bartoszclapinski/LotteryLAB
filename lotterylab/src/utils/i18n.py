"""
Internationalization (i18n) utilities for Lottery Lab.

Supports Polish (default) and English languages.
Uses Babel for translation management.
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional
from functools import lru_cache

from babel import Locale
from babel.support import Translations

# Supported languages
SUPPORTED_LANGUAGES = ['pl', 'en']
DEFAULT_LANGUAGE = 'pl'

# Translations directory
TRANSLATIONS_DIR = Path(__file__).resolve().parents[2] / 'translations'


@lru_cache(maxsize=10)
def get_translations(language: str) -> Translations:
    """
    Load translations for a given language.
    
    Args:
        language: Language code ('pl', 'en')
        
    Returns:
        Translations object for the language
    """
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    
    try:
        return Translations.load(
            dirname=str(TRANSLATIONS_DIR),
            locales=[language]
        )
    except Exception:
        # Fallback to NullTranslations if loading fails
        return Translations()


def get_locale(language: str) -> Locale:
    """
    Get Babel Locale object for a language.
    
    Args:
        language: Language code ('pl', 'en')
        
    Returns:
        Babel Locale object
    """
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    return Locale.parse(language)


def detect_language(
    cookie_lang: Optional[str] = None,
    query_lang: Optional[str] = None,
    accept_language: Optional[str] = None
) -> str:
    """
    Detect user's preferred language from various sources.
    
    Priority:
    1. Query parameter (?lang=en)
    2. Cookie (lang=pl)
    3. Accept-Language header
    4. Default (pl)
    
    Args:
        cookie_lang: Language from cookie
        query_lang: Language from query parameter
        accept_language: Accept-Language header value
        
    Returns:
        Detected language code
    """
    # 1. Query parameter has highest priority
    if query_lang and query_lang in SUPPORTED_LANGUAGES:
        return query_lang
    
    # 2. Cookie
    if cookie_lang and cookie_lang in SUPPORTED_LANGUAGES:
        return cookie_lang
    
    # 3. Accept-Language header
    if accept_language:
        # Parse Accept-Language header (e.g., "pl-PL,pl;q=0.9,en;q=0.8")
        for lang_part in accept_language.split(','):
            lang_code = lang_part.split(';')[0].strip().split('-')[0].lower()
            if lang_code in SUPPORTED_LANGUAGES:
                return lang_code
    
    # 4. Default
    return DEFAULT_LANGUAGE


# UI text translations (fallback before .po files are ready)
# This will be replaced by proper .po/.mo files
UI_TEXTS = {
    'en': {
        'site_title': 'Lottery Lab',
        'tagline': 'Where Luck Meets Science',
        'nav_overview': 'Overview',
        'nav_analysis': 'Analysis',
        'nav_experiments': 'Experiments',
        'nav_docs': 'Docs',
        'new_study': 'New Study',
        'controls': 'Controls',
        'game_type_label': 'Game type',
        'window_days_label': 'Window (days)',
        'methods': 'Methods',
        'frequency_analysis': 'Frequency analysis',
        'randomness_tests': 'Randomness tests',
        'number_generator': 'Number generator',
        'pattern_analysis': 'Pattern analysis',
        'correlation_heatmap': 'Correlation heatmap',
        'hypothesis_tests': 'Hypothesis tests',
        'statistical_analysis': 'Statistical analysis of draws',
        'explore_frequency': 'Explore frequency distributions and compare with the expected uniform baseline.',
        'tip': 'Tip',
        'tip_window': 'Use shorter windows (e.g. 90 days) to emphasize recency; longer windows smooth variance.',
        'loading': 'Loading…',
        'loading_recent': 'Loading recent draws…',
        'footer': 'Research & Education',
        'hot_numbers_title': 'Hot Numbers',
        'cold_numbers_title': 'Cold Numbers',
        'hot_desc': 'Appearing more frequently than expected',
        'cold_desc': 'Appearing less frequently than expected',
        'view_all': 'View All Numbers',
        'draws': 'Draws',
        'expected_each': 'Expected each',
        'days': 'days',
        'recent_draws': 'Recent Draws',
        'draw_number': 'Draw #',
        'date': 'Date',
        'numbers': 'Numbers',
        'type': 'Type',
        'game': 'Game',
        'provider': 'Provider',
        # Randomness Analysis
        'randomness_title': 'Randomness Analysis',
        'randomness_subtitle': 'Statistical tests to determine if lottery draws follow expected random patterns',
        'appears_random': 'Appears Random',
        'not_random': 'Not Random',
        'chi_square_title': 'Chi-Square Goodness-of-Fit Test',
        'ks_title': 'Kolmogorov-Smirnov Test',
        'runs_title': 'Runs Test (Sequence Randomness)',
        'autocorr_title': 'Autocorrelation Analysis',
        'p_value': 'p-value',
        'significant': 'Significant',
        'not_significant': 'Not significant',
        'test_statistic': 'Test statistic',
        'degrees_freedom': 'Degrees of Freedom',
        'sample_info': 'Sample Information',
        'total_draws': 'Total Draws',
        'total_numbers': 'Total Numbers',
        'coverage': 'Coverage',
        'entropy_title': 'Information Entropy',
        'low_randomness': 'Low Randomness',
        'high_randomness': 'High Randomness',
        'shannon_entropy': 'Shannon Entropy',
        'bits_per_number': 'bits per number',
        'max_possible': 'Maximum Possible',
        'interpretation': 'Statistical Interpretation',
        'educational_note': 'Educational Note',
        'educational_disclaimer': 'This analysis tests for statistical randomness, not prediction power. Even truly random systems can show temporary patterns in finite samples. Lottery outcomes remain unpredictable regardless of statistical properties.',
        # Pattern Analysis
        'pattern_title': 'Pattern Analysis',
        'pattern_subtitle': 'Detection of statistical patterns and sequences in lottery draws',
        'consecutive_title': 'Consecutive Numbers',
        'arithmetic_title': 'Arithmetic Sequences',
        'digit_title': 'Digit Analysis',
        'sum_title': 'Sum Analysis',
        'sequences_found': 'sequences found',
        'total_sequences': 'Total Sequences',
        'max_length': 'Max Length',
        'avg_length': 'Avg Length',
        'found_sequences': 'Found Sequences',
        # Correlation Analysis
        'correlation_title': 'Number Correlation Analysis',
        'correlation_subtitle': 'Exploring relationships and clustering patterns between lottery numbers',
        'correlation_overview': 'Correlation Overview',
        'draws_analyzed': 'draws analyzed',
        'numbers_analyzed': 'Numbers Analyzed',
        'avg_correlation': 'Avg Correlation',
        'strongest_link': 'Strongest Link',
        'top_pairs': 'Top Correlated Number Pairs',
        'analysis_insights': 'Analysis Insights',
        # Generator
        'generator_title': 'Number Generator',
        'generator_desc': 'Generate a number set based on recent frequency analysis. This favors recently hot numbers while avoiding extreme cold numbers.',
        'your_set': 'Your Generated Set',
        'generate_new': 'Generate New Set',
        'hot': 'hot',
        'neutral': 'neutral',
        'cold': 'cold',
        'generator_disclaimer': 'This is for entertainment only. Lottery outcomes are truly random.',
    },
    'pl': {
        'site_title': 'Lottery Lab',
        'tagline': 'Gdzie Szczęście Spotyka Naukę',
        'nav_overview': 'Przegląd',
        'nav_analysis': 'Analiza',
        'nav_experiments': 'Eksperymenty',
        'nav_docs': 'Dokumentacja',
        'new_study': 'Nowe badanie',
        'controls': 'Kontrolki',
        'game_type_label': 'Typ gry',
        'window_days_label': 'Okno (dni)',
        'methods': 'Metody',
        'frequency_analysis': 'Analiza częstości',
        'randomness_tests': 'Testy losowości',
        'number_generator': 'Generator liczb',
        'pattern_analysis': 'Analiza wzorców',
        'correlation_heatmap': 'Mapa korelacji',
        'hypothesis_tests': 'Testy hipotez',
        'statistical_analysis': 'Analiza statystyczna losowań',
        'explore_frequency': 'Eksploruj rozkłady częstości i porównaj z oczekiwanym rozkładem jednostajnym.',
        'tip': 'Wskazówka',
        'tip_window': 'Krótsze okna (np. 90 dni) podkreślają aktualność; dłuższe wygładzają wariancję.',
        'loading': 'Ładowanie…',
        'loading_recent': 'Ładowanie ostatnich losowań…',
        'footer': 'Badania i Edukacja',
        'hot_numbers_title': 'Gorące liczby',
        'cold_numbers_title': 'Zimne liczby',
        'hot_desc': 'Pojawiają się częściej niż oczekiwano',
        'cold_desc': 'Pojawiają się rzadziej niż oczekiwano',
        'view_all': 'Pokaż wszystkie liczby',
        'draws': 'Losowania',
        'expected_each': 'Oczekiwana częstość',
        'days': 'dni',
        'recent_draws': 'Ostatnie losowania',
        'draw_number': 'Nr losowania',
        'date': 'Data',
        'numbers': 'Liczby',
        'type': 'Typ',
        'game': 'Gra',
        'provider': 'Dostawca',
        # Randomness Analysis
        'randomness_title': 'Analiza losowości',
        'randomness_subtitle': 'Testy statystyczne sprawdzające czy losowania podążają za oczekiwanymi wzorcami losowymi',
        'appears_random': 'Wygląda na losowe',
        'not_random': 'Nie jest losowe',
        'chi_square_title': 'Test Chi-kwadrat dopasowania',
        'ks_title': 'Test Kołmogorowa-Smirnowa',
        'runs_title': 'Test serii (losowość sekwencji)',
        'autocorr_title': 'Analiza autokorelacji',
        'p_value': 'wartość p',
        'significant': 'Istotne',
        'not_significant': 'Nieistotne',
        'test_statistic': 'Statystyka testowa',
        'degrees_freedom': 'Stopnie swobody',
        'sample_info': 'Informacje o próbce',
        'total_draws': 'Liczba losowań',
        'total_numbers': 'Liczba liczb',
        'coverage': 'Pokrycie',
        'entropy_title': 'Entropia informacyjna',
        'low_randomness': 'Niska losowość',
        'high_randomness': 'Wysoka losowość',
        'shannon_entropy': 'Entropia Shannona',
        'bits_per_number': 'bitów na liczbę',
        'max_possible': 'Maksimum możliwe',
        'interpretation': 'Interpretacja statystyczna',
        'educational_note': 'Nota edukacyjna',
        'educational_disclaimer': 'Ta analiza testuje losowość statystyczną, nie zdolność przewidywania. Nawet prawdziwie losowe systemy mogą wykazywać tymczasowe wzorce w skończonych próbkach. Wyniki loterii pozostają nieprzewidywalne niezależnie od właściwości statystycznych.',
        # Pattern Analysis
        'pattern_title': 'Analiza wzorców',
        'pattern_subtitle': 'Wykrywanie statystycznych wzorców i sekwencji w losowaniach',
        'consecutive_title': 'Liczby kolejne',
        'arithmetic_title': 'Ciągi arytmetyczne',
        'digit_title': 'Analiza cyfr',
        'sum_title': 'Analiza sum',
        'sequences_found': 'sekwencji znaleziono',
        'total_sequences': 'Łączna liczba sekwencji',
        'max_length': 'Maks. długość',
        'avg_length': 'Średnia długość',
        'found_sequences': 'Znalezione sekwencje',
        # Correlation Analysis
        'correlation_title': 'Analiza korelacji liczb',
        'correlation_subtitle': 'Badanie zależności i wzorców grupowania między liczbami loterii',
        'correlation_overview': 'Przegląd korelacji',
        'draws_analyzed': 'losowań przeanalizowano',
        'numbers_analyzed': 'Przeanalizowano liczb',
        'avg_correlation': 'Średnia korelacja',
        'strongest_link': 'Najsilniejszy związek',
        'top_pairs': 'Najbardziej skorelowane pary',
        'analysis_insights': 'Wnioski z analizy',
        # Generator
        'generator_title': 'Generator liczb',
        'generator_desc': 'Generuj zestaw liczb na podstawie analizy częstości. Preferuje ostatnio gorące liczby, unikając skrajnie zimnych.',
        'your_set': 'Twój wygenerowany zestaw',
        'generate_new': 'Generuj nowy zestaw',
        'hot': 'gorące',
        'neutral': 'neutralne',
        'cold': 'zimne',
        'generator_disclaimer': 'To tylko rozrywka. Wyniki loterii są naprawdę losowe.',
    }
}


def t(key: str, lang: str = DEFAULT_LANGUAGE) -> str:
    """
    Get translated text by key.
    
    Args:
        key: Translation key
        lang: Language code
        
    Returns:
        Translated text or key if not found
    """
    if lang not in UI_TEXTS:
        lang = DEFAULT_LANGUAGE
    return UI_TEXTS.get(lang, {}).get(key, key)


def get_all_texts(lang: str = DEFAULT_LANGUAGE) -> dict:
    """
    Get all UI texts for a language.
    
    Args:
        lang: Language code
        
    Returns:
        Dictionary of all UI texts
    """
    if lang not in UI_TEXTS:
        lang = DEFAULT_LANGUAGE
    return UI_TEXTS.get(lang, UI_TEXTS[DEFAULT_LANGUAGE])

