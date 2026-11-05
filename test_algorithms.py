
# CSCE 4110 - SmartBudget
# Testing Memoization and Tabulation Algorithms

import unittest

from Memoization import knapsack_memoization
from Tabulation import solve_budget


class TestSmartBudget(unittest.TestCase):

    def compare_algorithms(self, expenses, budget):
        names = [item["name"] for item in expenses]
        costs = [item["cost"] for item in expenses]
        priorities = [item["priority"] for item in expenses]

        memo = knapsack_memoization(expenses, budget)
        tab = solve_budget(names, costs, priorities, budget)

        # Both algorithms must find the same optimal priority
        self.assertEqual(
            memo["maximum_priority"],
            tab["maximum_priority"]
        )

        # Neither algorithm should exceed the budget
        self.assertLessEqual(memo["total_spent"], budget)
        self.assertLessEqual(tab["total_cost"], budget)

        # Verify selected expenses and their priorities
        memo_names = [item["name"] for item in memo["selected_expenses"]]

        for selected_names, total_cost in [
            (memo_names, memo["total_spent"]),
            (tab["selected_expenses"], tab["total_cost"])
        ]:
            self.assertEqual(len(selected_names), len(set(selected_names)))

            selected = [
                item for item in expenses
                if item["name"] in selected_names
            ]

            self.assertEqual(
                sum(item["cost"] for item in selected),
                total_cost
            )

            self.assertEqual(
                sum(item["priority"] for item in selected),
                memo["maximum_priority"]
            )

        return memo, tab

    def test_original_example(self):
        expenses = [
            {"name": "Laptop Repair", "cost": 300, "priority": 10},
            {"name": "Course", "cost": 250, "priority": 9},
            {"name": "Books", "cost": 150, "priority": 8},
            {"name": "Gym", "cost": 100, "priority": 6}
        ]

        memo, tab = self.compare_algorithms(expenses, 500)

        self.assertEqual(memo["maximum_priority"], 23)
        self.assertEqual(tab["maximum_priority"], 23)

    def test_small_budget(self):
        expenses = [
            {"name": "Books", "cost": 100, "priority": 8},
            {"name": "Gym", "cost": 50, "priority": 6}
        ]

        memo, tab = self.compare_algorithms(expenses, 30)

        self.assertEqual(memo["maximum_priority"], 0)

    def test_exact_budget(self):
        expenses = [
            {"name": "Books", "cost": 100, "priority": 8},
            {"name": "Course", "cost": 200, "priority": 9}
        ]

        memo, tab = self.compare_algorithms(expenses, 300)

        self.assertEqual(memo["maximum_priority"], 17)

    def test_single_expense(self):
        expenses = [
            {"name": "Laptop", "cost": 200, "priority": 10}
        ]

        memo, tab = self.compare_algorithms(expenses, 300)

        self.assertEqual(memo["maximum_priority"], 10)

    def test_zero_priority(self):
        expenses = [
            {"name": "Optional Item", "cost": 50, "priority": 0},
            {"name": "Books", "cost": 100, "priority": 8}
        ]

        memo, tab = self.compare_algorithms(expenses, 150)

        self.assertEqual(memo["maximum_priority"], 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
