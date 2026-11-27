
import csv
import io
import os

from flask import Flask, render_template, request, redirect, url_for, session, Response
from Tabulation import knapsack_tabulation
from Memoization import knapsack_memoization
from expense_catalog import EXPENSE_CATALOG


app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "smartbudget-local-development-key"
)


@app.route("/")
def dashboard():
    return render_template(
        "roshan_dashboard.html",
        expense_catalog=EXPENSE_CATALOG
    )


def run_tabulation(expenses, budget):
    costs = [expense["cost"] for expense in expenses]
    priorities = [expense["priority"] for expense in expenses]

    dp, states = knapsack_tabulation(
        costs, priorities, budget, return_count=True
    )

    n = len(expenses)
    max_priority = dp[n][budget]
    selected = []
    remaining_capacity = budget

    # Find which expenses were included in the optimal solution.
    for i in range(n, 0, -1):
        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:
            selected.append(expenses[i - 1])
            remaining_capacity -= costs[i - 1]

    selected.reverse()


    return {
        "maximum_priority": max_priority,
        "selected_expenses": selected,
        "states_evaluated": states,
        "dp_table": dp if len(expenses) <= 10 and budget <= 50 else None
    }

def run_memoization(expenses, budget):
    result = knapsack_memoization(expenses, budget)

    return {
        "maximum_priority": result["maximum_priority"],
        "selected_expenses": result["selected_expenses"],
        "states_evaluated": result.get(
            "states_evaluated", "Not available"
        )
    }


@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Invalid request information."}, 400

    try:
        def parse_integer(value, field_name):
            if isinstance(value, bool):
                raise ValueError(f"{field_name} must be a whole number.")

            if isinstance(value, int):
                return value

            if isinstance(value, str):
                value = value.strip()

                if value and value.lstrip("-").isdigit():
                    return int(value)

            raise ValueError(f"{field_name} must be a whole number.")

        budget = parse_integer(data["budget"], "Budget")
        algorithm = data.get("algorithm", "tabulation")
        expenses = data["expenses"]

        if budget < 1 or budget > 10000:
            raise ValueError("Budget must be between $1 and $10,000.")

        if algorithm not in ("tabulation", "memoization"):
            raise ValueError("Invalid optimization algorithm.")

        if not isinstance(expenses, list):
            raise ValueError("Expenses must be provided as a list.")

        if not 1 <= len(expenses) <= 50:
            raise ValueError("Enter between 1 and 50 expenses.")

        clean_expenses = []

        for expense in expenses:
            if not isinstance(expense, dict):
                raise ValueError("Invalid expense information.")

            
            raw_name = expense["name"]

            if not isinstance(raw_name, str):
                raise ValueError("Please enter a valid expense name.")

            name = raw_name.strip()
            cost = parse_integer(expense["cost"], "Expense cost")
            priority = parse_integer(expense["priority"], "Priority")

            if not name or len(name) > 60:
                raise ValueError("Please enter a valid expense name.")

            if cost < 1:
                raise ValueError("Expense cost must be greater than zero.")

            if priority < 0:
                raise ValueError("Priority cannot be negative.")

            clean_expenses.append({
                "name": name,
                "cost": cost,
                "priority": priority
            })

    except (KeyError, ValueError, TypeError, OverflowError) as error:
        return {"error": str(error)}, 400

    # Run the algorithm selected by the user.
    if algorithm == "memoization":
        result = run_memoization(clean_expenses, budget)
    else:
        result = run_tabulation(clean_expenses, budget)

    max_priority = result["maximum_priority"]
    selected_expenses = result["selected_expenses"]

    total_spent = sum(
        expense["cost"] for expense in selected_expenses
    )

    remaining = budget - total_spent
    allocation_percent = round((total_spent / budget) * 100, 1)

    # Store results so the second page can display them.
    session["results"] = {
        "budget": budget,
        "total_spent": total_spent,
        "remaining": remaining,
        "max_priority": max_priority,
        "selected_expenses": selected_expenses,
        "all_expenses": clean_expenses,
        "allocation_percent": allocation_percent,
        "algorithm": algorithm.title(),
        "expense_count": len(clean_expenses),
        "states_evaluated": result["states_evaluated"],
        "dp_table": result.get("dp_table")
    }

    return {"redirect": url_for("results")}


@app.route("/results")
def results():
    data = session.get("results")

    if data is None:
        return redirect(url_for("dashboard"))

    return render_template("roshan_results.html", **data)


@app.route("/download-csv", methods=["GET"])
def download_csv():
    data = session.get("results")

    if data is None:
        return redirect(url_for("dashboard"))

    all_expenses = data["all_expenses"]
    selected_expenses = data["selected_expenses"]

    remaining_selected = list(selected_expenses)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Expense", "Cost", "Priority", "Status"])

    # Include selected and unselected expenses in the report.
    for expense in all_expenses:
        if expense in remaining_selected:
            status = "Selected"
            remaining_selected.remove(expense)
        else:
            status = "Not Selected"

        writer.writerow([
            expense["name"],
            expense["cost"],
            expense["priority"],
            status
        ])

    writer.writerow([])
    writer.writerow(["BUDGET SUMMARY"])
    writer.writerow(["Total Budget", data["budget"]])
    writer.writerow(["Total Spent", data["total_spent"]])
    writer.writerow(["Remaining Budget", data["remaining"]])
    writer.writerow(["Maximum Priority", data["max_priority"]])
    writer.writerow(["Algorithm", data["algorithm"]])
    writer.writerow([
        "Budget Allocation",
        str(data["allocation_percent"]) + "%"
    ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=SmartBudget_Report.csv"
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
