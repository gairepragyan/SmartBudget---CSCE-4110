
# CSCE 4110 - SmartBudget
# Memoization vs Tabulation Performance Comparison

import random
import time
import csv
import matplotlib.pyplot as plt

from Memoization import knapsack_memoization
from Tabulation import solve_budget


def generate_expenses(n, seed=42):
    random_generator = random.Random(seed)

    expenses = []

    for i in range(n):
        expenses.append({
            "name": f"Expense {i + 1}",
            "cost": random_generator.randint(10, 100),
            "priority": random_generator.randint(1, 20)
        })

    return expenses


def benchmark():
    # Number of expenses to test
    sizes = [5, 10, 20, 30, 50, 100]

    # Keep budget fixed to study effect of item count
    budget = 500
    repetitions = 10

    memo_times = []
    tab_times = []
    results = []

    print("SMARTBUDGET PERFORMANCE COMPARISON")
    print("-" * 65)
    print(
        f"{'Items':<8}"
        f"{'Memo (ms)':<15}"
        f"{'Tab (ms)':<15}"
        f"{'Priority':<12}"
        f"{'Memo States':<12}"
    )

    for n in sizes:
        expenses = generate_expenses(n)

        names = [item["name"] for item in expenses]
        costs = [item["cost"] for item in expenses]
        priorities = [item["priority"] for item in expenses]

        memo_total = 0
        tab_total = 0

        for _ in range(repetitions):

            start = time.perf_counter()
            memo_result = knapsack_memoization(expenses, budget)
            memo_total += time.perf_counter() - start

            start = time.perf_counter()
            tab_result = solve_budget(
                names, costs, priorities, budget
            )
            tab_total += time.perf_counter() - start

            if (
                memo_result["maximum_priority"]
                != tab_result["maximum_priority"]
            ):
                raise AssertionError(
                    f"Algorithms disagree for {n} items!"
                )

        memo_ms = (memo_total / repetitions) * 1000
        tab_ms = (tab_total / repetitions) * 1000

        memo_times.append(memo_ms)
        tab_times.append(tab_ms)

        results.append({
            "items": n,
            "budget": budget,
            "memoization_ms": round(memo_ms, 6),
            "tabulation_ms": round(tab_ms, 6),
            "maximum_priority": memo_result["maximum_priority"],
            "memo_states": memo_result["states_evaluated"],
            "tab_states": n * budget
        })

        print(
            f"{n:<8}"
            f"{memo_ms:<15.4f}"
            f"{tab_ms:<15.4f}"
            f"{memo_result['maximum_priority']:<12}"
            f"{memo_result['states_evaluated']:<12}"
        )

    # Save benchmark results to CSV
    with open(
        "benchmark_results.csv", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # Create runtime comparison graph
    plt.figure(figsize=(9, 5))

    plt.plot(
        sizes, memo_times, marker="o", label="Memoization"
    )

    plt.plot(
        sizes, tab_times, marker="s", label="Tabulation"
    )

    plt.xlabel("Number of Expenses")
    plt.ylabel("Average Execution Time (milliseconds)")
    plt.title("SmartBudget: Memoization vs Tabulation")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("runtime_comparison.png", dpi=300)
    plt.show()

    print("\nBenchmark completed successfully!")
    print("Saved: benchmark_results.csv")
    print("Saved: runtime_comparison.png")


if __name__ == "__main__":
    benchmark()
