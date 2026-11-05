
# SmartBudget - 0/1 Knapsack using Memoization
# CSCE 4110 - Algorithms

def knapsack_memoization(expenses, budget):
    """
    Solve 0/1 Knapsack using Top-Down Dynamic Programming.

    Returns:
        Maximum priority
        Selected expenses
        Total spent
        Remaining budget
        Number of DP states evaluated
    """

    # Validate inputs
    if type(budget) is not int or budget <= 0:
        raise ValueError("Budget must be a positive whole number.")

    if not isinstance(expenses, list) or not expenses:
        raise ValueError("Please provide at least one expense.")

    for expense in expenses:
        if not isinstance(expense, dict):
            raise ValueError("Each expense must be a dictionary.")

        name = expense.get("name")
        cost = expense.get("cost")
        priority = expense.get("priority")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Expense name cannot be empty.")

        if type(cost) is not int or cost <= 0:
            raise ValueError("Expense cost must be a positive integer.")

        if type(priority) is not int or priority < 0:
            raise ValueError("Priority must be a nonnegative integer.")

    n = len(expenses)
    memo = {}
    states_evaluated = 0

    # Recursive function
    def solve(i, remaining_budget):
        nonlocal states_evaluated

        # Base case
        if i == 0 or remaining_budget == 0:
            return 0

        # Reuse previously calculated result
        if (i, remaining_budget) in memo:
            return memo[(i, remaining_budget)]

        states_evaluated += 1

        expense = expenses[i - 1]
        cost = expense["cost"]
        priority = expense["priority"]

        # Option 1: Skip current expense
        skip = solve(i - 1, remaining_budget)

        # Option 2: Take current expense
        if cost <= remaining_budget:
            take = priority + solve(
                i - 1, remaining_budget - cost
            )
            best = max(skip, take)
        else:
            best = skip

        # Store result
        memo[(i, remaining_budget)] = best
        return best

    # Calculate maximum priority
    maximum_priority = solve(n, budget)

    # Reconstruct selected expenses
    selected_expenses = []
    remaining = budget

    for i in range(n, 0, -1):
        if remaining == 0:
            break

        expense = expenses[i - 1]
        cost = expense["cost"]
        priority = expense["priority"]

        current = solve(i, remaining)
        skip = solve(i - 1, remaining)

        if cost <= remaining:
            take = priority + solve(i - 1, remaining - cost)

            if take > skip and current == take:
                selected_expenses.append(expense)
                remaining -= cost

    # Restore original expense order
    selected_expenses.reverse()

    total_spent = sum(item["cost"] for item in selected_expenses)

    return {
        "maximum_priority": maximum_priority,
        "selected_expenses": selected_expenses,
        "total_spent": total_spent,
        "remaining_budget": budget - total_spent,
        "states_evaluated": states_evaluated
    }


# Test the algorithm
if __name__ == "__main__":

    expenses = [
        {"name": "Laptop Repair", "cost": 300, "priority": 10},
        {"name": "Course", "cost": 250, "priority": 9},
        {"name": "Books", "cost": 150, "priority": 8},
        {"name": "Gym", "cost": 100, "priority": 6}
    ]

    budget = 500

    result = knapsack_memoization(expenses, budget)

    print("SmartBudget - Memoization")
    print("-------------------------")
    print(f"Available Budget: ${budget}")

    print("\nSelected Expenses:")
    for item in result["selected_expenses"]:
        print(f"- {item['name']}: ${item['cost']}")

    print(f"\nTotal Spent: ${result['total_spent']}")
    print(f"Remaining Budget: ${result['remaining_budget']}")
    print(f"Maximum Priority: {result['maximum_priority']}")
    print(f"DP States Evaluated: {result['states_evaluated']}")
