import unittest
import requests

class TestUserAPI(unittest.TestCase):
    API_URL = "http://localhost:8000"

    def test_default_flow(self):
        # Get all users which should not exist
        resp = requests.get(f"{self.API_URL}/users")

        self.assertEqual(resp.status_code, 200)

        payload = resp.json()
        self.assertIn("users", payload)

        user = {'name': 'Test User 1'}
        self.assertNotIn(user, payload["users"])

        # Create a single user and check that we have a valid ID
        data = user
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
        self.assertIn({"name": "Test User 1", "id": user_id}, payload["users"])


if __name__ == "__main__":
    unittest.main()