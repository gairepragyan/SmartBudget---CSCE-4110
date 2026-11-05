
from flask import Flask, render_template, request
from Tabulation import solve_budget, knapsack_tabulation
from Memoization import knapsack_memoization

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    success = None
    result = None
    memo_result = None
    dp_table = None

    budget = ""
    expenses = [
        {"name": "", "cost": "", "priority": ""},
        {"name": "", "cost": "", "priority": ""},
        {"name": "", "cost": "", "priority": ""},
        {"name": "", "cost": "", "priority": ""},
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
                        names = [expense["name"] for expense in valid_expenses]
                        costs = [expense["cost"] for expense in valid_expenses]
                        priorities = [expense["priority"] for expense in valid_expenses]

                        result = solve_budget(
                            names, costs, priorities, budget_value
                        )
                        memo_result = knapsack_memoization(
                            valid_expenses, budget_value
                        )
                        if budget_value <= 20:
                            dp_table = knapsack_tabulation(
                                costs, priorities, budget_value
                            )
                        success = "Budget optimization completed successfully."


        except ValueError:
            error = "Budget, cost, and priority must be whole numbers."

    return render_template(
        "index.html",
        error=error,
        success=success,
        budget=budget,
        expenses=expenses,
        result=result,
        memo_result=memo_result,
        dp_table=dp_table,
    )


if __name__ == "__main__":
    app.run(debug=True)
