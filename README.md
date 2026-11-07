# SmartBudget - CSCE 4110

**Budget Optimization Using 0/1 Knapsack and Dynamic Programming**

SmartBudget is a group project developed for CSCE 4110 - Algorithms at the University of North Texas. It is a Flask-based web application that helps users select expenses within a limited budget while maximizing their total priority score.

The project implements and compares two dynamic programming approaches to the 0/1 Knapsack problem: memoization (top-down) and tabulation (bottom-up).

## Project Features

- Enter a total budget and up to four expenses.
- Assign a name, cost, and priority score to each expense.
- Validate inputs to prevent incomplete or invalid expense entries.
- Find the optimal combination of expenses within the budget.
- Display selected expenses, maximum priority, total cost, and remaining budget.
- Compare the results of memoization and tabulation.
- Display the tabulation DP table for budgets of 20 or less.
- View the number of DP states evaluated by memoization.
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

From the main project directory, run:

```bash
python3 app.py
```

Then open the following address in your browser:

http://127.0.0.1:5000

You can also use:

http://localhost:5000

**Note:** SmartBudget currently runs on a local Flask development server. The terminal running Flask must remain open while using the application. To stop the server, press `Control + C`.

The localhost address is accessible only from the computer running the server. It is not a public website.

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

The project includes automated algorithm tests in `test_algorithms.py`.

Run:

```bash
python3 -m unittest -v test_algorithms
```

The tests cover cases including exact-budget selection, the original $500 example, a single expense, a small budget, and zero-priority expenses.

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

The additional budget-scaling experiment is currently being reviewed in a separate Pull Request and is not yet part of the main branch.

Once merged, it can be run using:

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
├── app.py
├── Memoization.py
├── Tabulation.py
├── benchmark.py
├── benchmark_results.csv
├── runtime_comparison.png
├── test_algorithms.py
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

Additional performance-analysis files will be included when their Pull Request is merged.

## Team Contributions

| Team Member | Main Responsibilities |
|---|---|
| Pragyan Gaire | Flask application, expense input and validation, algorithm integration, DP table display, performance analysis, and documentation |
| Vicky (Bicky) | Tabulation algorithm and result reconstruction |
| Roshan | Memoization algorithm and automated testing |

Team members also collaborate through GitHub branches, Pull Requests, code reviews, and testing.

## Technologies Used

- Python
- Flask
- HTML
- Dynamic Programming
- Git and GitHub
- Matplotlib
- CSV

## Project Purpose

The goal of SmartBudget is to demonstrate how dynamic programming can solve practical optimization problems. By comparing memoization and tabulation, the project explores algorithm correctness, time complexity, evaluated DP states, and observed execution performance.