 
# CSCE 4110 - SmartBudget
# Performance Analysis: Increasing Budget with Fixed Expense Count

import csv
import random
import time

import matplotlib.pyplot as plt

from Memoization import knapsack_memoization
from Tabulation import solve_budget


def generate_expenses(n, seed=42):
    rng = random.Random(seed)

    return [
        {
            "name": f"Expense {i + 1}",
            "cost": rng.randint(10, 100),
            "priority": rng.randint(1, 20),
        }
        for i in range(n)
    ]


def benchmark_budget():
    budgets = [100, 250, 500, 1000, 2000]
    n = 20
    repetitions = 10

    expenses = generate_expenses(n)

    names = [item["name"] for item in expenses]
    costs = [item["cost"] for item in expenses]
    priorities = [item["priority"] for item in expenses]

    results = []

    for budget in budgets:
        memo_total = 0
        tab_total = 0

        for repetition in range(repetitions):
            # Alternate the timing order to reduce order bias.
            if repetition % 2 == 0:
                start = time.perf_counter()
                memo_result = knapsack_memoization(expenses, budget)
                memo_total += time.perf_counter() - start

                start = time.perf_counter()
                tab_result = solve_budget(
                    names, costs, priorities, budget
                )
                tab_total += time.perf_counter() - start
            else:
                start = time.perf_counter()
                tab_result = solve_budget(
                    names, costs, priorities, budget
                )
                tab_total += time.perf_counter() - start

                start = time.perf_counter()
                memo_result = knapsack_memoization(expenses, budget)
                memo_total += time.perf_counter() - start

            if (
                memo_result["maximum_priority"]
                != tab_result["maximum_priority"]
            ):
                raise AssertionError(
                    f"Algorithms disagree at budget {budget}"
                )

        results.append({
            "budget": budget,
            "items": n,
            "memoization_ms": round(
                memo_total / repetitions * 1000, 6
            ),
            "tabulation_ms": round(
                tab_total / repetitions * 1000, 6
            ),
            "maximum_priority": memo_result["maximum_priority"],
            "memo_states": memo_result["states_evaluated"],
            "tab_states": n * budget,
        })

    print("\nSMARTBUDGET - BUDGET SCALING EXPERIMENT")
    print("-" * 70)

    for result in results:
        print(
            f"Budget: ${result['budget']:<5} "
            f"Memo: {result['memoization_ms']:.4f} ms  "
            f"Tab: {result['tabulation_ms']:.4f} ms  "
            f"Memo States: {result['memo_states']}  "
            f"Tab States: {result['tab_states']}"
        )

    with open(
        "budget_benchmark_results.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    budgets = [row["budget"] for row in results]

    plt.figure(figsize=(9, 5))
    plt.plot(
        budgets,
        [row["memoization_ms"] for row in results],
        marker="o",
        label="Memoization",
    )
    plt.plot(
        budgets,
        [row["tabulation_ms"] for row in results],
        marker="s",
        label="Tabulation",
    )
    plt.xlabel("Budget")
    plt.ylabel("Average Execution Time (ms)")
    plt.title("SmartBudget: Runtime vs Budget (20 Expenses)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("budget_runtime_comparison.png", dpi=300)

    plt.figure(figsize=(9, 5))
    plt.plot(
        budgets,
        [row["memo_states"] for row in results],
        marker="o",
        label="Memoization",
    )
    plt.plot(
        budgets,
        [row["tab_states"] for row in results],
        marker="s",
        label="Tabulation",
    )
    plt.xlabel("Budget")
    plt.ylabel("DP States Evaluated")
    plt.title("SmartBudget: DP States vs Budget (20 Expenses)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("budget_states_comparison.png", dpi=300)

    plt.show()

    print("\nBenchmark completed successfully.")
    print("Saved: budget_benchmark_results.csv")
    print("Saved: budget_runtime_comparison.png")
    print("Saved: budget_states_comparison.png")


if __name__ == "__main__":
    benchmark_budget()
