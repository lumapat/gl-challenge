import json
import unittest
import requests


class TestLoansAPI(unittest.TestCase):
    API_URL = "http://localhost:8000"

    def create_user(self, name: str) -> int:
        data = {'name': name}
        resp = requests.post(f"{self.API_URL}/user", json=data)

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("id", payload)

        return payload["id"]

    def test_default_flow(self):
        # Setup
        # Create a new user
        user_id = self.create_user("Jane Doe")

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
            "loan_term": 6,
            "amount": 3600,
            "annual_ir": 2,
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

        # Generate the loan schedule
        resp = requests.get(f"{self.API_URL}/loan/{loan_id}/schedule")

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("schedule", payload)

        # The actual logic for this is tested in the unit test
        # This is just light validation on the output of the API call
        schedule = payload["schedule"]
        self.assertEqual(loan["loan_term"], len(schedule))
        self.assertAlmostEqual(schedule[-1]["remaining_balance"], 0, 3)

        # Generate the loan summary at month 4
        resp = requests.get(f"{self.API_URL}/loan/{loan_id}/summary/month/4")

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("summary", payload)

        summary = payload["summary"]
        self.assertEqual(4, summary["month"])
        self.assertGreater(summary["current_principal_balance"], 0)
        self.assertGreater(summary["aggregate_interest_paid"], 0)
        self.assertGreater(summary["aggregate_principal_paid"], 0)


    def test_get_loans_from_invalid_user(self):
        # GIVEN
        bad_user_id=9876543210

        # WHEN
        resp = requests.get(f"{self.API_URL}/user/{bad_user_id}/loans")

        # THEN
        self.assertEqual(resp.status_code, 404)

        error_msg = json.loads(resp.content)["detail"]
        self.assertEqual(f"Could not find user with id={bad_user_id}", error_msg)


    def test_get_invalid_loan(self):
        # GIVEN
        bad_loan_id=9876543210

        # WHEN
        resp = requests.get(f"{self.API_URL}/loan/{bad_loan_id}")

        # THEN
        self.assertEqual(resp.status_code, 404)

        error_msg = json.loads(resp.content)["detail"]
        self.assertEqual(f"Could not find loan with id={bad_loan_id}", error_msg)


    def test_add_user_to_bad_loan(self):
        # GIVEN
        bad_loan_id=9876543210

        # WHEN
        resp = requests.put(f"{self.API_URL}/loan/{bad_loan_id}/users", json={
            "user_ids": [123456]
        })

        # THEN
        self.assertEqual(resp.status_code, 404)

        error_msg = json.loads(resp.content)["detail"]
        self.assertEqual(f"Could not find loan with id={bad_loan_id}", error_msg)


    def test_get_schedule_for_invalid_loan(self):
        # GIVEN
        bad_loan_id=9876543210

        # WHEN
        resp = requests.get(f"{self.API_URL}/loan/{bad_loan_id}/schedule")

        # THEN
        self.assertEqual(resp.status_code, 404)

        error_msg = json.loads(resp.content)["detail"]
        self.assertEqual(f"Could not find loan with id={bad_loan_id}", error_msg)


    def test_get_summary_for_invalid_loan(self):
        # GIVEN
        bad_loan_id=9876543210

        # WHEN
        resp = requests.get(f"{self.API_URL}/loan/{bad_loan_id}/summary/month/1")

        # THEN
        self.assertEqual(resp.status_code, 404)

        error_msg = json.loads(resp.content)["detail"]
        self.assertEqual(f"Could not find loan with id={bad_loan_id}", error_msg)


if __name__ == "__main__":
    unittest.main()