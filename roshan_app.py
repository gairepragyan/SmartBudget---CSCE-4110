
from flask import Flask, render_template, request, redirect, url_for, session
from functools import lru_cache

app = Flask(__name__)
app.secret_key = "smartbudget-development-key"


# PAGE 1 - HOME
@app.route("/")
def dashboard():
    return render_template("roshan_dashboard.html")


# 0/1 KNAPSACK - TABULATION
def knapsack_tabulation(expenses, budget):
    n = len(expenses)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = expenses[i - 1]["cost"]
        priority = expenses[i - 1]["priority"]

        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]

            if cost <= b:
                dp[i][b] = max(
                    dp[i][b],
                    priority + dp[i - 1][b - cost]
                )

    selected = []
    b = budget

    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            selected.append(expenses[i - 1])
            b -= expenses[i - 1]["cost"]

    selected.reverse()
    return dp[n][budget], selected


# 0/1 KNAPSACK - MEMOIZATION
def knapsack_memoization(expenses, budget):
    n = len(expenses)

    @lru_cache(None)
    def solve(i, remaining):
        if i == n:
            return 0

        best = solve(i + 1, remaining)
        cost = expenses[i]["cost"]
        priority = expenses[i]["priority"]

        if cost <= remaining:
            best = max(
                best,
                priority + solve(i + 1, remaining - cost)
            )

        return best

    max_priority = solve(0, budget)

    selected = []
    remaining = budget

    for i in range(n):
        cost = expenses[i]["cost"]
        priority = expenses[i]["priority"]

        if (
            cost <= remaining
            and priority + solve(i + 1, remaining - cost)
            > solve(i + 1, remaining)
        ):
            selected.append(expenses[i])
            remaining -= cost

    return max_priority, selected


# PROCESS USER EXPENSES
@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "Invalid request data."}, 400

    try:
        budget = int(data["budget"])
        algorithm = data.get("algorithm", "tabulation")
        expenses = data["expenses"]

        if budget < 1 or budget > 10000:
            raise ValueError("Budget must be between 1 and 10000.")

        if algorithm not in ("tabulation", "memoization"):
            raise ValueError("Invalid algorithm.")

        if not isinstance(expenses, list) or not 1 <= len(expenses) <= 50:
            raise ValueError("Enter between 1 and 50 expenses.")

        clean_expenses = []

        for expense in expenses:
            name = str(expense["name"]).strip()
            cost = int(expense["cost"])
            priority = int(expense["priority"])

            if not name or len(name) > 60 or cost < 1 or priority < 1:
                raise ValueError("Invalid expense information.")

            clean_expenses.append({
                "name": name,
                "cost": cost,
                "priority": priority
            })

    except (KeyError, ValueError, TypeError, OverflowError) as error:
        return {"error": str(error)}, 400

    if algorithm == "memoization":
        max_priority, selected = knapsack_memoization(
            clean_expenses, budget
        )
    else:
        max_priority, selected = knapsack_tabulation(
            clean_expenses, budget
        )

    total_spent = sum(item["cost"] for item in selected)
    remaining = budget - total_spent
    allocation_percent = round(total_spent / budget * 100, 1)

    session["results"] = {
        "budget": budget,
        "total_spent": total_spent,
        "remaining": remaining,
        "max_priority": max_priority,
        "selected_expenses": selected,
        "allocation_percent": allocation_percent,
        "algorithm": algorithm.title(),
        "expense_count": len(clean_expenses)
    }

    return {"redirect": url_for("results")}


# PAGE 2 - RESULTS
@app.route("/results")
def results():
    data = session.get("results")

    if data is None:
        return redirect(url_for("dashboard"))

    return render_template("roshan_results.html", **data)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
