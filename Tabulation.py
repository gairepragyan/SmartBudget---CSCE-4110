
# CSCE 4110 - SmartBudget Project
# Bottom-Up Dynamic Programming (0/1 Knapsack)
# Tabulation + Result Reconstruction


# PART 1: Build the DP table
def knapsack_tabulation(costs, priorities, budget):

    n = len(costs)

    # Create DP table with n+1 rows and budget+1 columns
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Go through each item
    for i in range(1, n + 1):

        cost = costs[i - 1]
        priority = priorities[i - 1]

        # Go through each possible budget
        for b in range(1, budget + 1):

            if cost > b:
                # Item is too expensive, so skip it
                dp[i][b] = dp[i - 1][b]

            else:
                # Choice 1: Skip the current item
                skip = dp[i - 1][b]

                # Choice 2: Take the current item
                take = priority + dp[i - 1][b - cost]

                # Choose the maximum priority
                dp[i][b] = max(skip, take)

    return dp


# PART 2: Result Reconstruction (Backtracking)
def reconstruct_items(dp, costs, names, budget):

    selected_indices = []

    i = len(costs)
    b = budget

    # Start from the bottom-right corner of the DP table
    while i > 0 and b > 0:

        # Compare the current cell with the cell above
        if dp[i][b] == dp[i - 1][b]:

            # Current item was not selected
            i -= 1

        else:

            # Current item was selected
            selected_indices.append(i - 1)

            # Subtract the selected item's cost
            b -= costs[i - 1]

            # Move to the previous item
            i -= 1

    # Restore the original order
    selected_indices.reverse()

    selected_names = [
        names[index] for index in selected_indices
    ]

    return selected_names, selected_indices

def solve_budget(names, costs, priorities, budget):

    # Step 1: Create the DP table
    dp = knapsack_tabulation(costs, priorities, budget)

    # Step 2: Find selected expenses
    selected_names, selected_indices = reconstruct_items(
        dp, costs, names, budget
    )

    # Step 3: Calculate total cost
    total_cost = sum(costs[i] for i in selected_indices)

    # Step 4: Calculate remaining budget
    remaining_budget = budget - total_cost

    # Step 5: Find maximum priority
    max_priority = dp[len(costs)][budget]

    # Step 6: Return all results
    return {
        "maximum_priority": max_priority,
        "selected_expenses": selected_names,
        "total_cost": total_cost,
        "remaining_budget": remaining_budget
    }


# PART 4: Main Program
def main():

    print("           SMARTBUDGET PROJECT          ")

    # Step 1: Define expenses and budget
    names = ["Laptop Repair", "Course", "Books", "Gym"]
    costs = [300, 250, 150, 100]
    priorities = [10, 9, 8, 6]
    budget = 500

    # Step 2: Test the new reusable function
    result = solve_budget(names, costs, priorities, budget)

    print("\nTESTING solve_budget():", result)

    # Step 3: Build the DP table for display
    dp = knapsack_tabulation(costs, priorities, budget)

    # Step 4: Display available expenses
    print("\nAvailable Expenses:")

    for i in range(len(names)):
        print(
            f"{names[i]}: "
            f"Cost = ${costs[i]}, "
            f"Priority = {priorities[i]}"
        )

    print("\nTotal Budget: $", budget, sep="")

    # Step 5: Display DP table information
    if budget <= 20:
        print("\nDP Table:")
        for row in dp:
            print(row)
    else:
        print("\nDP Table created successfully.")
        print("Table Size:", len(dp), "rows x",
              len(dp[0]), "columns")

    # Step 6: Display final result
    print("\n              FINAL RESULT              ")

    print("Maximum Priority:", result["maximum_priority"])

    print("Selected Expenses:")

    if result["selected_expenses"]:
        for name in result["selected_expenses"]:
            print("-", name)
    else:
        print("No expenses selected.")

    print("\nTotal Cost: $", result["total_cost"], sep="")
    print("Remaining Budget: $",
          result["remaining_budget"], sep="")


# PART 5: Run the program
if __name__ == "__main__":
    main()
