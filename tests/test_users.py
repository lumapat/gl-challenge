import unittest
import json
import requests

class TestAPI(unittest.TestCase):
    API_URL = "http://localhost:8000"

    def test_default_flow(self):
        # Get all users which should not exist
        resp = requests.get(f"{self.API_URL}/users")

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("users", payload)
        self.assertEqual(payload["users"], [])

        # Create a single user and check that we have a valid ID
        data = {'name': 'Test User 1'}
        resp = requests.post(f"{self.API_URL}/user", json=data)

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("id", payload)
        self.assertTrue(payload["id"] > 0)

        user_id = payload["id"]

        # Validate that the user is persisted with that same returned ID
        resp = requests.get(f"{self.API_URL}/users")

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("users", payload)
        self.assertEqual(payload["users"], [{"name": "Test User 1", "id": user_id}])


if __name__ == "__main__":
    unittest.main()