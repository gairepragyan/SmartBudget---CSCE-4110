
import unittest
from app import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # Test 1: Check whether the homepage opens
    def test_homepage(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

        self.assertIn(b"Dashboard Overview", response.data)

    # Test 2: Check budget optimization
    def test_budget_optimization(self):

        response = self.client.post("/", data={
            "budget": "250",
            "expense_name": ["Books", "Course", "Headphones"],
            "expense_cost": ["100", "150", "80"],
            "expense_priority": ["10", "8", "6"]
        })

        self.assertEqual(response.status_code, 200)

        self.assertIn(b"Optimization Results", response.data)

        self.assertIn(b"Maximum Priority", response.data)

        self.assertIn(b"18", response.data)

    # Test 3: Check CSV report download
    def test_csv_export(self):

        response = self.client.post("/download-csv", data={
            "budget": "250",
            "expense_name": ["Books", "Course", "Headphones"],
            "expense_cost": ["100", "150", "80"],
            "expense_priority": ["10", "8", "6"]
        })

        self.assertEqual(response.status_code, 200)

        self.assertIn("text/csv", response.content_type)

        self.assertIn(b"Books", response.data)

        self.assertIn(b"Course", response.data)

        self.assertIn(b"Headphones", response.data)

        self.assertIn(b"Maximum Priority,18", response.data)

    # Test 4: Reject a negative budget
    def test_negative_budget(self):

        response = self.client.post("/", data={
            "budget": "-100",
            "expense_name": ["Books"],
            "expense_cost": ["50"],
            "expense_priority": ["10"]
        })

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b"Budget must be greater than 0.",
            response.data
        )

    # Test 5: Reject a negative expense cost
    def test_negative_expense_cost(self):

        response = self.client.post("/", data={
            "budget": "300",
            "expense_name": ["Books"],
            "expense_cost": ["-50"],
            "expense_priority": ["10"]
        })

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b"Expense cost must be greater than 0.",
            response.data
        )

    # Test 6: Reject a negative priority
    def test_negative_priority(self):

        response = self.client.post("/", data={
            "budget": "300",
            "expense_name": ["Books"],
            "expense_cost": ["50"],
            "expense_priority": ["-10"]
        })

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b"Priority score cannot be negative.",
            response.data
        )


if __name__ == "__main__":
    unittest.main()
