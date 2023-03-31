import unittest
import requests

class TestLoansAPI(unittest.TestCase):
    API_URL = "http://localhost:8000"

    def test_default_flow(self):
        # Setup
        # Create a new user
        data = {'name': 'Jane Doe'}
        resp = requests.post(f"{self.API_URL}/user", json=data)

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("id", payload)

        user_id = payload["id"]

        # Ensure we have no loans under that user
        resp = requests.get(f"{self.API_URL}/user/{user_id}/loans")

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("loans", payload)
        self.assertEqual(payload["loans"], [])

        # Create a new loan
        loan = {
            "loan_term": 3,
            "amount": 1000000.01,
            "annual_ir": 3.14,
        }

        resp = requests.post(f"{self.API_URL}/loan/{user_id}", json=loan)
        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("id", payload)

        loan_id = payload["id"]
        self.assertTrue(loan_id > 0)

        # Check that loan is created
        resp = requests.get(f"{self.API_URL}/user/{user_id}/loans")

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        loan["id"] = loan_id
        self.assertEqual(payload, {"loans": [loan]})


if __name__ == "__main__":
    unittest.main()