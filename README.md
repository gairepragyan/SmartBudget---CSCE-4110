# SmartBudget - CSCE 4110

**Budget Optimization Using 0/1 Knapsack and Dynamic Programming**

SmartBudget is a group project developed for CSCE 4110 - Algorithms at the University of North Texas. It is a Flask-based web application that helps users select expenses within a limited budget while maximizing their total priority score.

The project implements and compares two dynamic programming approaches to the 0/1 Knapsack problem: memoization (top-down) and tabulation (bottom-up).

## Project Features
- Enter a total budget and dynamically add or remove expenses.
- Assign a name, cost, and priority score to each expense.
- Validate inputs to prevent incomplete or invalid expense entries.
- Find the optimal combination of expenses using 0/1 Knapsack.
- Compare memoization (top-down) and tabulation (bottom-up).
- Display selected expenses, maximum priority, total cost, and remaining budget.
- View a financial dashboard with budget summary cards and utilization progress.
- Display a breakdown of selected expenses.
- Visualize algorithm performance using interactive charts.
- Compare expense priority scores using a chart.
- Display budget insights and recommendations.
- Display the tabulation DP table for budgets of 20 or less.
- View DP states evaluated by memoization.
- Download optimization results as a CSV report.
- Save and load budget information using browser localStorage.
- Run automated algorithm and Flask application tests.
- Run performance benchmarks comparing execution times and DP states.

## Algorithms Used

### 1. Memoization (Top-Down Dynamic Programming)

Memoization solves the 0/1 Knapsack problem recursively and stores previously calculated results to avoid repeated computations.

Implemented in `Memoization.py`.

### 2. Tabulation (Bottom-Up Dynamic Programming)

Tabulation uses a dynamic programming table to calculate the maximum priority achievable for each combination of expenses and available budget. The algorithm also reconstructs the selected expenses.

Implemented in `Tabulation.py`.

Both approaches have worst-case time complexity of O(n × B), where n is the number of expenses and B is the budget.

## Installation and Setup

### Requirements

- Python 3
- Git
- Flask
- Matplotlib (for performance graphs)

### 1. Clone the repository

```bash
git clone https://github.com/gairepragyan/SmartBudget---CSCE-4110.git
cd SmartBudget---CSCE-4110
```

Alternatively, download the project as a ZIP file from GitHub and extract it.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```


## Running SmartBudget

After installing the dependencies, open a terminal in the project directory.

Start the Flask development server:

```bash
python3 -m flask --app app run --debug --port 5001
```

Open your browser and visit:

http://127.0.0.1:5001

Alternatively:

http://localhost:5001

### Stopping the Server

Press `Control + C` in the terminal running Flask.

### Important Notes

- The Flask server must remain running while using SmartBudget.
- Port 5001 is used in these instructions.
- SmartBudget currently runs locally, not on a publicly hosted website.
- The `--debug` option is intended for local development only.


## Example Input

Enter the following information into the SmartBudget form.

**Total Budget: $500**

| Expense | Cost | Priority |
|---|---:|---:|
| Laptop Repair | $300 | 10 |
| Course | $250 | 9 |
| Books | $150 | 8 |
| Gym | $100 | 6 |

### Expected Output

**Selected Expenses:**
- Course
- Books
- Gym

**Maximum Priority:** 23

**Total Cost:** $500

**Remaining Budget:** $0

Both memoization and tabulation should return the same maximum priority.

For a budget of 20 or less, the application also displays the tabulation DP table.


## Running Automated Tests

SmartBudget includes automated tests using Python's built-in `unittest` framework.

The project contains two testing files:

### 1. Algorithm Tests

File: `test_algorithms.py`

These five tests verify the correctness of the dynamic programming algorithms:

- Exact-budget selection
- Original $500 budget example
- Single expense
- Small budget
- Zero-priority expenses

Run the algorithm tests:

```bash
python3 -m unittest -v test_algorithms
```

### 2. Flask Application Tests

File: `test_app.py`

These six tests verify the Flask application's routes and input validation:

- Homepage loads successfully
- Budget optimization produces results
- CSV report downloads successfully
- Negative budget is rejected
- Negative expense cost is rejected
- Negative priority score is rejected

Run the Flask tests:

```bash
python3 -m unittest -v test_app
```

### 3. Run All Tests

To automatically discover and run both test files:

```bash
python3 -m unittest discover -v
```

Expected result:

```text
Ran 11 tests

OK
```

All 11 automated tests passed during local verification.


## Performance Analysis

SmartBudget includes experiments that compare the execution times and DP state counts of memoization and tabulation.

### Experiment 1: Increasing the Number of Expenses

Run:

```bash
python3 benchmark.py
```

This experiment holds the budget at $500 and tests different numbers of expenses.

It generates:

- `benchmark_results.csv`
- `runtime_comparison.png`

### Experiment 2: Increasing the Budget

The budget-scaling experiment is included in the main branch and compares memoization and tabulation as the available budget increases.

Run the budget-scaling experiment using:

```bash
python3 benchmark_budget.py
```

It holds the number of expenses at 20 while testing budgets of $100, $250, $500, $1,000, and $2,000.

It generates:

- `budget_benchmark_results.csv`
- `budget_runtime_comparison.png`
- `budget_states_comparison.png`

The benchmarks help demonstrate how different dynamic programming approaches perform as input size and budget capacity change.


## Project Structure

```text
SmartBudget---CSCE-4110/
│
├── app.py
├── Memoization.py
├── Tabulation.py
│
├── benchmark.py
├── benchmark_budget.py
├── benchmark_results.csv
├── budget_benchmark_results.csv
│
├── runtime_comparison.png
├── budget_runtime_comparison.png
├── budget_states_comparison.png
│
├── test_algorithms.py
├── test_app.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── requirements.txt
├── .gitignore
└── README.md
```

### File Descriptions

- `app.py` - Flask application, routes, form validation, and CSV export.
- `Memoization.py` - Top-down dynamic programming implementation.
- `Tabulation.py` - Bottom-up dynamic programming implementation.
- `benchmark.py` - Performance testing with increasing expense counts.
- `benchmark_budget.py` - Performance testing with increasing budgets.
- `test_algorithms.py` - Five automated algorithm tests.
- `test_app.py` - Six automated Flask application tests.
- `templates/index.html` - Web application interface and JavaScript functionality.
- `static/style.css` - Dashboard styling.
- `requirements.txt` - Python dependencies.
- `README.md` - Project documentation.

The CSV files contain benchmark results, while the PNG files contain generated performance comparison graphs.



## Team Contributions

| Team Member | Main Responsibilities |
|---|---|
| Pragyan Gaire | Flask application, expense input and validation, algorithm integration, DP table display, performance analysis, and documentation |
| Bicky | Tabulation algorithm and result reconstruction, dashboard enhancements, financial summary cards, interactive charts, budget insights, CSV export, Save/Load Budget functionality, and automated Flask application tests |
| Roshan | Memoization algorithm and automated algorithm testing |

Team members collaborated through GitHub feature branches, Pull Requests, code reviews, integration t


## Technologies Used

### Backend
- Python 3
- Flask
- Python unittest framework

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js for interactive charts

### Algorithms
- 0/1 Knapsack Problem
- Dynamic Programming
- Memoization (Top-Down)
- Tabulation (Bottom-Up)

### Data and Storage
- CSV for exporting reports and storing benchmark results
- Browser localStorage for saving and loading budget information

### Performance Analysis
- Matplotlib for generating benchmark graphs
- Python performance measurement tools

### Version Control
- Git
- GitHub
- Feature branches and Pull Requests


## Project Purpose

The goal of SmartBudget is to demonstrate how dynamic programming can solve practical optimization problems. By comparing memoization and tabulation, the project explores algorithm correctness, time complexity, evaluated DP states, and observed execution performance.

## Web Application Validation Testing

The SmartBudget Flask application was manually tested with
the following scenarios:

- Original $500 budget example: Both algorithms returned
  maximum priority 23 and selected Course, Books, and Gym.
- Missing expense cost: The application displayed an error
  message and preserved the entered values.
- Negative priority: Input validation rejected the invalid value.
- Zero budget: Input validation prevented a zero budget.

These tests help verify the application's input handling,
algorithm integration, and user experience.