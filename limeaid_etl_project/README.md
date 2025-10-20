# LimeAid ETL Project

This project implements a CSV-to-SQLite ETL pipeline with Quality Assurance (QA) and Descriptive Statistics, following Python data science best practices.

## Overview

The pipeline consists of three main stages:
1. **ETL**: Extract data from CSV files, transform/clean it, and load into a SQLite database.
2. **QA**: Run data quality checks on the loaded data.
3. **Stats**: Compute descriptive statistics and generate reports.

## Setup

1. Clone the repository and navigate to the project directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Place your CSV files in `data/raw/`.
4. Configure paths and settings in `config/config.yaml`.

## Running the Pipeline

- Run ETL: `python scripts/run_etl.py`
- Run QA: `python scripts/run_qa.py`
- Run Stats: `python scripts/run_stats.py`
- Full pipeline: `python scripts/main.py`

## Testing

Run tests with: `pytest tests/`

## Project Structure

- `config/`: Configuration files
- `data/`: Data artifacts (raw, processed, db)
- `src/`: Core source code modules
- `scripts/`: Entry-point scripts
- `tests/`: Unit and integration tests
- `notebooks/`: Exploratory analysis notebooks