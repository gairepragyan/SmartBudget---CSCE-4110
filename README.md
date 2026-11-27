# SmartBudget - CSCE 4110

**Budget Optimization Using 0/1 Knapsack and Dynamic Programming**

SmartBudget is a group project developed for CSCE 4110 - Algorithms at the University of North Texas. It is a Flask-based web application that helps users select expenses within a limited budget while maximizing their total priority score.

The project implements and compares two dynamic programming approaches to the 0/1 Knapsack problem: memoization (top-down) and tabulation (bottom-up).

## Project Features

- Enter a total budget and dynamically add, edit, or remove expenses.
- Assign a name, cost, and priority score to each expense.
- Validate budget and expense inputs and display error messages.
- Find the optimal combination of expenses using the 0/1 Knapsack algorithm.
- Choose between memoization (top-down) and tabulation (bottom-up).
- Display selected expenses, maximum priority, total spending, and remaining  budget.
- View budget summary cards, expense lists, and budget allocation charts.
- Display a Tabulation DP table for small inputs (up to 10 expenses and a budget of $50).
- Compare Memoization and Tabulation using benchmark scripts that measure execution time and DP states evaluated.
- Download optimization results as a CSV report.
- Automatically preserve expenses in browser localStorage.
- Edit and remove expenses using the dashboard controls.
- Clear all saved expenses when needed.
- Run automated algorithm and Flask application tests.

## Algorithms Used


## Algorithms Used

SmartBudget solves the 0/1 Knapsack problem using two dynamic programming approaches. Each expense has a cost (weight) and a priority score (value), while the available budget represents the knapsack capacity. Each expense can either be selected once or excluded.

### 1. Memoization (Top-Down Dynamic Programming)

Implemented in `Memoization.py`.

Memoization uses recursion to solve the problem by deciding whether to include or exclude each expense. Previously calculated subproblem results are stored in a cache to avoid repeated calculations.

Only subproblems reached during recursion need to be evaluated. However, recursion and cache management introduce additional overhead.

### 2. Tabulation (Bottom-Up Dynamic Programming)

Implemented in `Tabulation.py`.

Tabulation builds a two-dimensional DP table, where each cell represents the maximum priority achievable using a certain number of expenses and an available budget.

The algorithm fills the table from smaller subproblems to larger ones and then traces backward through the table to reconstruct the selected expenses.

For small inputs (at most 10 expenses and a budget of $50), the results page displays the Tabulation DP table so users can inspect how the optimal solution is calculated.

### Time and Space Complexity

Let:
- `n` = number of expenses
- `B` = total budget, represented as a positive integer

| Algorithm | Worst-Case Time | Worst-Case Space |
|---|---|---|
| Memoization | O(n × B) | O(n × B) |
| Tabulation | O(n × B) | O(n × B) |

Memoization may evaluate fewer states than Tabulation because it calculates only reachable subproblems. Its memory usage includes cached states and recursion stack overhead.

Tabulation systematically fills a DP table containing `(n + 1) × (B + 1)` entries.

Both algorithms have pseudo-polynomial complexity. Their running time depends on the numerical value of the budget `B`, not just the number of bits required to represent it.

### Why Greedy Selection Is Not Always Optimal

Consider a $500 budget with these expenses:

| Expense | Cost | Priority |
|---|---:|---:|
| Laptop Repair | $300 | 10 |
| Course | $250 | 9 |
| Books | $150 | 8 |
| Gym | $100 | 6 |

A greedy strategy that selects expenses in descending priority order chooses Laptop Repair ($300, priority 10) and Books ($150, priority 8). It spends $450 and achieves a total priority of 18.

The optimal dynamic programming solution instead selects Course, Books, and Gym, spending $500 and achieving a total priority of 23. This shows why a highest-priority-first greedy strategy does not always produce the optimal combination.

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

For Tabulation inputs with 10 or fewer expenses and a budget of $50 or less, SmartBudget also displays the DP table on the results page. The table shows the maximum priority achievable at each budget capacity and helps explain how the algorithm finds the optimal solution.


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

These nine tests verify the Flask application's routes, input validation, CSV export, and DP table visualization:

- Homepage loads successfully.
- Budget optimization produces the expected results.
- CSV report downloads successfully.
- Negative budget is rejected.
- Negative expense cost is rejected.
- Negative priority score is rejected.
- DP table appears correctly for small Tabulation inputs.
- DP table remains hidden for Memoization.
- DP table remains hidden for Tabulation when the budget exceeds $50.

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
Ran 14 tests

OK
```
All 14 automated tests passed during local verification, including the three tests added for DP table visualization.


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


### Benchmark Observations

The performance experiments compare Memoization and Tabulation using execution time and the number of DP states evaluated.

In the expense-scaling experiment, execution time generally increases as more expenses are added while the budget remains fixed at $500. Tabulation was faster than Memoization in the measured runs, although performance can vary depending on the input data and execution environment.

In the budget-scaling experiment, Tabulation evaluates more states as the budget increases because it systematically fills the DP table. Memoization may evaluate fewer states because it computes only the subproblems reached during recursion.

These observations are consistent with the theoretical O(n × B) worst-case time complexity of both approaches. However, the measured runtime and state counts are influenced by input characteristics, implementation overhead, and hardware.

Benchmark results are saved as CSV files, and comparison graphs are generated using Matplotlib.


## Project Structure

```text
SmartBudget---CSCE-4110/
│
├── app.py
├── Memoization.py
├── Tabulation.py
├── expense_catalog.py
├── roshan_app.py
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
│   ├── index.html
│   ├── roshan_dashboard.html
│   └── roshan_results.html
│
├── static/
│   ├── css/
│   │   └── roshan_style.css
│   ├── Javascript/
│   │   └── roshan_script.js
│   └── style.css
│
├── requirements.txt
├── .gitignore
└── README.md
```

### File Descriptions


- `app.py` - Main Flask application, API routes, input validation, optimization integration, results, and CSV export.
- `Memoization.py` - Top-down dynamic programming implementation.
- `Tabulation.py` - Bottom-up dynamic programming implementation and DP table generation.
- `expense_catalog.py` - Expense catalog data used by the application.
- `roshan_app.py` - Additional Flask application module retained in the repository.
- `benchmark.py` - Performance comparisons with increasing expense counts.
- `benchmark_budget.py` - Performance comparisons with increasing budgets.
- `test_algorithms.py` - Five algorithm correctness tests.
- `test_app.py` - Nine Flask application tests, including DP table visualization tests.
- `templates/index.html` - Earlier dashboard interface retained in the repository.
- `templates/roshan_dashboard.html` - Active dashboard for managing expenses and selecting an optimization method.
- `templates/roshan_results.html` - Active results page showing optimized expenses, budget allocation, algorithm details, and the Tabulation DP table for small inputs.
- `static/css/roshan_style.css` - Styling for the active dashboard.
- `static/Javascript/roshan_script.js` - Expense management, browser storage, user interactions, and optimization requests.
- `static/style.css` - Styling associated with the earlier dashboard.
- `requirements.txt` - Python dependencies.
- `README.md` - Project documentation.

The CSV files contain benchmark results, while the PNG files contain generated performance comparison graphs.


## Team Contributions


| Team Member | Implementation and Technical Contributions |
|---|---|
| Pragyan Gaire | Set up the Flask application, implemented budget and expense validation, added multi-expense support, integrated Tabulation and Memoization into Flask, developed DP table visualization, updated Flask tests, improved dashboard usability, contributed to performance analysis and README documentation, and supported GitHub integration and conflict resolution. |
| Bicky Roka | Implemented the Tabulation algorithm and selected-expense reconstruction, developed the original premium dashboard, financial summary cards, budget charts, expense visualizations, expense catalog, monthly budget tracker, CSV export, Save/Load Budget functionality, and Flask application tests. Contributed to documentation and integration. |
| Roshan Dahal | Implemented the Memoization algorithm and algorithm unit tests, developed the initial performance benchmark and comparison graph, built the redesigned frontend and results page, integrated the frontend with Flask, implemented browser localStorage persistence, expense editing and removal, Clear All functionality, custom Edit Expense modal, and toast notifications. |

The team collaborated through GitHub feature branches, pull requests, code reviews, testing, debugging, and integration. Some features were developed for an earlier version of the dashboard and later replaced or revised during frontend integration.


## Technologies Used

### Backend
- Python 3
- Flask
- Python unittest framework

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js (used in the earlier dashboard retained in templates/index.html)

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