
import unittest
from app import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def sample_data(self):
        return {
            "budget": 250,
            "algorithm": "tabulation",
            "expenses": [
                {"name": "Books", "cost": 100, "priority": 10},
                {"name": "Course", "cost": 150, "priority": 8},
                {"name": "Headphones", "cost": 80, "priority": 6}
            ]
        }

    # Test 1: Homepage loads Roshan's dashboard
    def test_homepage(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Manage Expenses", response.data)
        self.assertIn(b"Budget Optimizer", response.data)

    # Test 2: Budget optimization
    def test_budget_optimization(self):
        response = self.client.post(
            "/optimize",
            json=self.sample_data()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["redirect"],
            "/results"
        )

        with self.client.session_transaction() as session:
            result = session["results"]

        self.assertEqual(result["max_priority"], 18)
        self.assertEqual(result["total_spent"], 250)
        self.assertEqual(result["remaining"], 0)
        self.assertEqual(
            [e["name"] for e in result["selected_expenses"]],
            ["Books", "Course"]
        )

    # Test 3: CSV export after optimization
    def test_csv_export(self):
        response = self.client.post(
            "/optimize",
            json=self.sample_data()
        )

        self.assertEqual(response.status_code, 200)

        csv_response = self.client.get("/download-csv")

        self.assertEqual(csv_response.status_code, 200)
        self.assertIn("text/csv", csv_response.content_type)
        self.assertIn(b"Books", csv_response.data)
        self.assertIn(b"Course", csv_response.data)
        self.assertIn(b"Headphones", csv_response.data)

    # Test 4: Negative budget rejected
    def test_negative_budget(self):
        data = self.sample_data()
        data["budget"] = -100

        response = self.client.post("/optimize", json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Budget must be between",
            response.get_json()["error"]
        )

    # Test 5: Negative expense cost rejected
    def test_negative_expense_cost(self):
        data = self.sample_data()
        data["expenses"][0]["cost"] = -50

        response = self.client.post("/optimize", json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Expense cost must be greater than zero",
            response.get_json()["error"]
        )

    # Test 6: Negative priority rejected
    def test_negative_priority(self):
        data = self.sample_data()
        data["expenses"][0]["priority"] = -10

        response = self.client.post("/optimize", json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Priority cannot be negative",
            response.get_json()["error"]
        )


if __name__ == "__main__":
    unittest.main()
