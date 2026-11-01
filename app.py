from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    success = None

    budget = ""
    expense_name = ""
    expense_cost = ""
    expense_priority = ""

    if request.method == "POST":
        budget = request.form.get("budget", "").strip()
        expense_name = request.form.get("expense_name", "").strip()
        expense_cost = request.form.get("expense_cost", "").strip()
        expense_priority = request.form.get("expense_priority", "").strip()

        if not expense_name:
            error = "Expense name cannot be empty."

        else:
            try:
                budget_value = int(budget)
                cost_value = int(expense_cost)
                priority_value = int(expense_priority)

                if budget_value <= 0:
                    error = "Budget must be greater than 0."

                elif cost_value <= 0:
                    error = "Expense cost must be greater than 0."

                elif priority_value < 0:
                    error = "Priority score cannot be negative."

                else:
                    success = "Input accepted. The expense is ready for optimization."

            except ValueError:
                error = "Budget, cost, and priority must be whole numbers."

    return render_template(
        "index.html",
        error=error,
        success=success,
        budget=budget,
        expense_name=expense_name,
        expense_cost=expense_cost,
        expense_priority=expense_priority,
    )


if __name__ == "__main__":
    app.run(debug=True)