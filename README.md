# 🧪 Lottery Lab

<div align="center">

**Where Luck Meets Science**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](lotterylab/LICENSE)
[![Tests](https://img.shields.io/badge/Tests-78%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-79%25-yellowgreen.svg)]()

*A comprehensive statistical analysis platform for lottery draws*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api) • [Contributing](#-contributing)

</div>

---

## 📖 About

**Lottery Lab** is a research and educational platform for statistical analysis of lottery draws. It provides comprehensive tools to analyze randomness, detect patterns, and visualize correlations in historical lottery data.

> ⚠️ **Disclaimer**: This is a research/educational tool. Lottery outcomes are truly random and cannot be predicted. This software does NOT claim to predict winning numbers.

## ✨ Features

### 📊 Statistical Analysis
- **Frequency Analysis** — Hot/cold numbers, expected vs actual distributions
- **Randomness Tests** — Chi-square, Kolmogorov-Smirnov, Runs test, Autocorrelation
- **Pattern Detection** — Consecutive numbers, arithmetic sequences, digit analysis
- **Correlation Heatmaps** — Number co-occurrence patterns and relationships

### 🎯 Tools
- **Number Generator** — Generate sets based on statistical analysis
- **Shannon Entropy** — Measure randomness/unpredictability
- **Historical Data** — Browse and filter past lottery draws

### 🌐 Modern Web Interface
- Clean, responsive UI inspired by Google ML Crash Course
- Real-time updates with HTMX
- Interactive Plotly.js charts
- Bilingual support (Polish/English)

### 🔧 Developer-Friendly
- RESTful API with OpenAPI documentation
- Comprehensive test suite (79% coverage)
- Automatic data updates from MBNet
- Makefile for common tasks

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy |
| **Frontend** | Jinja2, HTMX, Plotly.js |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **Analysis** | NumPy, Pandas, SciPy |
| **Testing** | pytest, pytest-cov |

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip or pipenv

### Quick Start

```bash
# Clone the repository
git clone https://github.com/bartoszclapinski/LotteryLAB.git
cd LotteryLAB/lotterylab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
make db-init

# Import historical data (optional)
python scripts/update_mbnet.py

# Start the server
make server
```

The application will be available at **http://127.0.0.1:8000**

## 🚀 Usage

### Web Interface

Navigate to `http://127.0.0.1:8000` and explore:

1. **Frequency Analysis** — View number frequency distributions
2. **Randomness Tests** — Run statistical tests on draw data
3. **Pattern Analysis** — Detect sequences and patterns
4. **Correlation Heatmap** — Visualize number relationships
5. **Number Generator** — Generate weighted number sets

### Makefile Commands

```bash
make help          # Show all available commands
make server        # Start development server
make test          # Run all tests
make test-cov      # Run tests with coverage report
make update        # Fetch latest draws from MBNet
make db-upgrade    # Run database migrations
make clean         # Clean build artifacts
```

## 📡 API

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/draws` | List draws with filters |
| GET | `/api/v1/analysis/frequency` | Frequency analysis |
| GET | `/api/v1/analysis/randomness` | Randomness tests |
| GET | `/api/v1/analysis/patterns` | Pattern detection |
| GET | `/api/v1/analysis/correlation` | Correlation analysis |

### Example Request

```bash
curl "http://127.0.0.1:8000/api/v1/analysis/frequency?game_type=lotto&window_days=365"
```

### Example Response

```json
{
  "game_type": "lotto",
  "window_days": 365,
  "num_draws": 156,
  "frequency": {"1": 18, "2": 21, ...},
  "expected_each": 19.1,
  "hot_numbers": [7, 23, 34, 45],
  "cold_numbers": [3, 11, 28, 39]
}
```

## 📁 Project Structure

```
LotteryLAB/
├── lotterylab/
│   ├── src/
│   │   ├── api/              # FastAPI endpoints
│   │   ├── analysis/         # Statistical analysis modules
│   │   │   ├── frequency.py  # Frequency analysis
│   │   │   ├── randomness.py # Randomness tests
│   │   │   ├── patterns.py   # Pattern detection
│   │   │   └── visualizations.py
│   │   ├── database/         # SQLAlchemy models
│   │   ├── data_acquisition/ # Data import/update
│   │   ├── repositories/     # Data access layer
│   │   └── utils/            # Helpers, i18n, logging
│   ├── templates/            # Jinja2 templates
│   ├── static/               # CSS, JS, images
│   ├── tests/                # Test suite
│   ├── scripts/              # CLI utilities
│   ├── alembic/              # Database migrations
│   └── .ai/                  # Sprint docs, PRD
├── alembic.ini
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/test_randomness.py -v
```

## 🌍 Internationalization

The UI supports multiple languages:
- 🇵🇱 Polish (default)
- 🇬🇧 English

Switch languages using the toggle in the header.

## 📈 Statistical Methods

### Chi-Square Goodness-of-Fit Test
Tests if observed number frequencies match expected uniform distribution.

### Kolmogorov-Smirnov Test
Compares empirical distribution against theoretical uniform distribution.

### Runs Test
Analyzes sequence randomness by counting "runs" of consecutive values.

### Autocorrelation Analysis
Detects temporal dependencies between successive draws.

### Shannon Entropy
Quantifies randomness/uncertainty in the number distribution.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](lotterylab/LICENSE) file for details.

## 🙏 Acknowledgments

- Data source: [MBNet](http://www.mbnet.com.pl/) for historical Polish Lotto data
- UI inspiration: Google ML Crash Course
- Statistical methods: SciPy documentation

---

<div align="center">

**Lottery Lab** — Research & Education

Made with ❤️ for data science enthusiasts

</div>

