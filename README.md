[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=yellow)](https://www.python.org)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![formula1-race-analysis-build](https://github.com/KrisKulbych/formula1-race-analysis/actions/workflows/build.yaml/badge.svg)](https://github.com/KrisKulbych/formula1-race-analysis/actions/workflows/build.yaml)

# Formula 1 Race Analysis
Formula 1 Race Analysis is a command-line tool for analyzing and displaying the results of Formula 1 qualifying sessions, specifically Q1. It provides sorting, filtering, and reporting options to analyze driver performance effectively.

****This project is at the early stages of development. 

## Installation
Copy and run the following command:
```console
pip install -i https://test.pypi.org/simple/ formula1-race-analysis
```
Formula 1 Race Analysis supports Python >= 3.12.

## Currently supported tools:
- pre-commit;
- ruff;
- uv;
- pytest.

## Interface
The primary command to use is generate_report. It takes the following options:
```console
f1_racing_results generate-report --data_dir <PATH_TO_DATA> [--order asc|des] [--driver DRIVER_NAME]
```

Options:

`--data_dir` (Required): The path to the directory containing qualifying session data files.

`--order` (Optional): Sort the qualifying results.
- asc (default): Ascending order.
- des: Descending order.

`--driver` (Optional): Filter the report by the driver's name.

`--ignore_errors` (Optional): Skip lines with incorrect data format.

Generate a report in ascending order:
```console
f1_racing_results generate-report --data_dir <PATH_TO_DATA>
```
Generate a report in ascending order:
```console
f1_racing_results generate-report --data_dir <PATH_TO_DATA>
```
Generate a report in descending order:
```console
f1_racing_results generate-report --data_dir <PATH_TO_DATA> --order des
```
Skip lines with incorrect data format:
```console
f1_racing_results generate-report --data_dir <PATH_TO_DATA> --ignore_errors
```
Filter the report for a specific driver:
```console
f1_racing_results generate-report --data_dir <PATH_TO_DATA> --driver "Lewis Hamilton"
```

## Logging
This project uses Structlog and Python's built-in logging module for structured and detailed logging.
Example Logger Output:
```console
2024-12-25 15:31:57 [debug    ] Starting report generation. Data directory: 'src\data'. [display.q1_report_generator]
2024-12-25 15:31:57 [error    ] Failed during report generation: InvalidFormatDataError - Error! Incorrect data format: 
```

## Setup Pre-commit Hooks:
Run this command after cloning the project to enable pre-commit:
```console
pre-commit install
```

## For Contributors
This project is managed with uv. All python dependencies have to be specified inside pyproject.toml file. 
1. Install uv globally:
```console
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
2. Activate virtual environment
```console
python -m venv .venv
.venv/bin/activate
```
3. Install Development Dependencies:
```console
uv sync --all-extras --dev
```
4. Lint and formate code:
```console
uv run ruff check
uv run ruff format
uv run mypy .
```
5. Automatically format code, check linting, and ensure clean commits.
```console
pre-commit run 
```
6. Run tests
```console
pytest tests\
```

tags: `python` `python3` `problem-solving` `programming` `learn-python` `formula1_race_analysis` `uv` `cli` `testpypi`
