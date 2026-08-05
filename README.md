![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly)
![GitHub last commit](https://img.shields.io/github/last-commit/rajnyandini/n100)
![GitHub repo size](https://img.shields.io/github/repo-size/rajnyandini/n100)
![GitHub issues](https://img.shields.io/github/issues/rajnyandini/n100)
![Status](https://img.shields.io/badge/Status-Active_Development-orange)
# N100 Financial Intelligence Platform

A comprehensive financial intelligence platform designed to collect, validate, process, and analyze financial data for NIFTY 100 companies. The project focuses on building a reliable data pipeline that transforms raw financial statements into structured datasets for analytical and business intelligence applications.

---

## Overview

The N100 Financial Intelligence Platform provides an end-to-end ETL (Extract, Transform, Load) workflow for financial datasets. It ingests company financial information, validates data quality, stores the processed data in a relational database, and generates metrics that can be used for dashboards, reporting, and investment analysis.

This project was developed as part of the **Bluestock Fintech Internship Program**.

---

## Features

- Automated ETL pipeline
- Data normalization and cleaning
- Data quality validation
- SQLite database integration
- Financial ratio calculations
- Unit tested data processing modules
- Modular project architecture
- Ready for dashboard and analytics integration

---

## Project Structure

```text
N100/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── db/
│   ├── nifty100.db
│   └── schema.sql
│
├── output/
│
├── src/
│   ├── etl/
│   │   ├── loader.py
│   │   ├── validator.py
│   │   ├── calculate_ratios.py
│   │   └── normalize.py
│   │
│   └── utils/
│
├── tests/
│
├── notebooks/
│
├── requirements.txt
├── Makefile
├── .env.example
└── README.md
```

---

## Technology Stack

- Python 3.x
- SQLite
- Pandas
- NumPy
- Plotly
- Matplotlib
- SQLAlchemy
- Pytest
- Jupyter Notebook

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/n100.git
cd n100
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file based on the example below.

```env
DB_NAME=nifty100.db
DB_PATH=db/nifty100.db

RAW_DATA_PATH=data/raw
PROCESSED_DATA_PATH=data/processed

OUTPUT_PATH=output
```

---

## Running the Project

### Load Raw Data

```bash
python src/etl/loader.py
```

### Validate Data

```bash
python src/etl/validator.py
```

### Calculate Financial Ratios

```bash
python src/etl/calculate_ratios.py
```

### Run Tests

```bash
pytest
```

---

## Data Pipeline

```
Raw Financial Files
        │
        ▼
Data Loading
        │
        ▼
Normalization
        │
        ▼
Data Quality Validation
        │
        ▼
SQLite Database
        │
        ▼
Financial Ratio Calculation
        │
        ▼
Analytics & Dashboard
```

---

## Key Functionalities

- Financial data ingestion
- Data cleaning and preprocessing
- Company information management
- Balance Sheet processing
- Profit & Loss processing
- Cash Flow processing
- Data quality validation rules
- Financial ratio computation
- Database storage
- Analytics-ready output

---

## Testing

The project includes automated unit tests covering:

- Data normalization
- ETL pipeline
- Validation rules
- Utility functions

Run all tests using:

```bash
pytest -v
```

---

## Future Enhancements

- Interactive dashboard
- REST API integration
- Real-time stock data
- Automated scheduled ETL
- Portfolio analytics
- Machine Learning based financial insights

---

## Author

**Rajnandini Singh Solanki**

B.Tech Computer Science (AI & ML)

---

## Acknowledgements

Developed as part of the **Bluestock Fintech Internship Program** under the **N100 Financial Intelligence Platform** project.

---

## License

This project is intended for educational and internship purposes.
