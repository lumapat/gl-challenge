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
        def validate_loans_under_user(user_id, expected_loans):
            resp = requests.get(f"{self.API_URL}/user/{user_id}/loans")

            self.assertEqual(resp.status_code, 200)

            payload = resp.json()
            self.assertIn("loans", payload)
            self.assertEqual(payload["loans"], expected_loans)

        validate_loans_under_user(user_id, [])

        # Create a new loan
        loan = {
            "loan_term": 3,
            "amount": 1000000.01,
            "annual_ir": 3.14,
        }

        resp = requests.post(f"{self.API_URL}/loan", json=loan)
        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("id", payload)

        loan_id = payload["id"]
        self.assertTrue(loan_id > 0)

        validate_loans_under_user(user_id, [])

        # Associate loan with user
        resp = requests.put(f"{self.API_URL}/loan/{loan_id}/users", json={
            "user_ids": [user_id]
        })

        self.assertEqual(resp.status_code, 200)

        # Check we now have a loan under our user
        loan["id"] = loan_id
        validate_loans_under_user(user_id, [loan])


if __name__ == "__main__":
    unittest.main()