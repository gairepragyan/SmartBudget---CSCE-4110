
import csv
import io
from pathlib import Path

from flask import Flask, render_template, request, Response
from Tabulation import solve_budget, knapsack_tabulation
from Memoization import knapsack_memoization
from expense_catalog import EXPENSE_CATALOG


app = Flask(__name__)


def load_benchmark_data(filename):
    file_path = Path(__file__).resolve().parent / filename

    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    return data


@app.route("/", methods=["GET", "POST"])
def home():
    expense_benchmarks = load_benchmark_data("benchmark_results.csv")
    budget_benchmarks = load_benchmark_data("budget_benchmark_results.csv")

    error = None
    success = None
    result = None
    memo_result = None
    priority_chart_data = []
    dp_table = None
    tabulation_states = None

    budget = ""
    expenses = [
        {"name": "", "cost": "", "priority": ""}
    ]

    if request.method == "POST":
        budget = request.form.get("budget", "").strip()

        names = request.form.getlist("expense_name")
        costs = request.form.getlist("expense_cost")
        priorities = request.form.getlist("expense_priority")

        expenses = []

        for name, cost, priority in zip(names, costs, priorities):
            expenses.append(
                {
                    "name": name.strip(),
                    "cost": cost.strip(),
                    "priority": priority.strip(),
                }
            )

        try:
            budget_value = int(budget)

            if budget_value <= 0:
                error = "Budget must be greater than 0."

            else:
                valid_expenses = []

                for expense in expenses:
                    name = expense["name"]
                    cost = expense["cost"]
                    priority = expense["priority"]

                    if not name and not cost and not priority:
                        continue

                    if not name or not cost or not priority:
                        error = "Each expense must include a name, cost, and priority."
                        break

                    cost_value = int(cost)
                    priority_value = int(priority)

                    if cost_value <= 0:
                        error = "Expense cost must be greater than 0."
                        break

                    if priority_value < 0:
                        error = "Priority score cannot be negative."
                        break

                    valid_expenses.append(
                        {
                            "name": name,
                            "cost": cost_value,
                            "priority": priority_value,
                        }
                    )

                if not error:
                    if len(valid_expenses) == 0:
                        error = "Please enter at least one expense."

                    else:
                        names = [
                            expense["name"]
                            for expense in valid_expenses
                        ]

                        costs = [
                            expense["cost"]
                            for expense in valid_expenses
                        ]

                        priorities = [
                            expense["priority"]
                            for expense in valid_expenses
                        ]

                        result = solve_budget(
                            names, costs, priorities, budget_value
                        )

                        memo_result = knapsack_memoization(
                            valid_expenses, budget_value
                        )

                        selected_ids = {
                            id(expense)
                            for expense in memo_result["selected_expenses"]
                        }

                        priority_chart_data = [
                            {
                                "name": expense["name"],
                                "cost": expense["cost"],
                                "priority": expense["priority"],
                                "selected": id(expense) in selected_ids
                            }
                            for expense in valid_expenses
                        ]

                        if budget_value <= 20:
                            dp_table, tabulation_states = knapsack_tabulation(
                                costs,
                                priorities,
                                budget_value,
                                return_count=True
                            )

                        success = "Budget optimization completed successfully."

        except ValueError:
            error = "Budget, cost, and priority must be whole numbers."
    print("CATALOG DEBUG:", len(EXPENSE_CATALOG), EXPENSE_CATALOG)
    return render_template(
        "index.html",
        expense_catalog=EXPENSE_CATALOG,
        error=error,
        success=success,
        budget=budget,
        expenses=expenses,
        result=result,
        memo_result=memo_result,
        priority_chart_data=priority_chart_data,
        dp_table=dp_table,
        tabulation_states=tabulation_states,
        expense_benchmarks=expense_benchmarks,
        budget_benchmarks=budget_benchmarks,
    )


@app.route("/download-csv", methods=["POST"])
def download_csv():
    budget = request.form.get("budget", "").strip()

    names = request.form.getlist("expense_name")
    costs = request.form.getlist("expense_cost")
    priorities = request.form.getlist("expense_priority")

    try:
        budget_value = int(budget)

        if budget_value <= 0:
            return "Budget must be greater than 0.", 400

        if not (len(names) == len(costs) == len(priorities)):
            return "Expense information is incomplete.", 400

        valid_expenses = []

        for name, cost, priority in zip(names, costs, priorities):
            name = name.strip()

            # Ignore completely empty expense rows
            if not name and not cost.strip() and not priority.strip():
                continue

            if not name or not cost.strip() or not priority.strip():
                return "Each expense must include a name, cost, and priority.", 400

            cost_value = int(cost)
            priority_value = int(priority)

            if cost_value <= 0:
                return "Expense cost must be greater than 0.", 400

            if priority_value < 0:
                return "Priority cannot be negative.", 400

            valid_expenses.append(
                {
                    "name": name,
                    "cost": cost_value,
                    "priority": priority_value
                }
            )

        if not valid_expenses:
            return "Please enter at least one expense.", 400

    except ValueError:
        return "Budget, cost, and priority must be whole numbers.", 400

    memo_result = knapsack_memoization(
        valid_expenses, budget_value
    )

    selected_ids = {
        id(expense)
        for expense in memo_result["selected_expenses"]
    }

    
    output = io.StringIO()
    writer = csv.writer(output)

  
    writer.writerow([
        "Expense",
        "Cost",
        "Priority",
        "Status"
    ])

    for expense in valid_expenses:
        status = (
            "Selected"
            if id(expense) in selected_ids
            else "Not Selected"
        )

        writer.writerow([
            expense["name"],
            expense["cost"],
            expense["priority"],
            status
        ])

    writer.writerow([])
    writer.writerow(["Budget Summary"])
    writer.writerow(["Total Budget", budget_value])
    writer.writerow(["Maximum Priority", memo_result["maximum_priority"]])
    writer.writerow(["Total Spent", memo_result["total_spent"]])
    writer.writerow(["Remaining Budget", memo_result["remaining_budget"]])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=budget_report.csv"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
