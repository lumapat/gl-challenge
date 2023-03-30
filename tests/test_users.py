import unittest
import json
import requests
from urllib import request, parse

class TestAPI(unittest.TestCase):
    API_URL = "http://localhost:8000"

    def test_get_all_users(self):
        with request.urlopen(f"{self.API_URL}/users") as response:
            data = json.loads(response.read().decode())
            self.assertTrue(len(data) > 0)

    def test_create_user(self):
        data = {'name': 'woo'}
        resp = requests.post(f"{self.API_URL}/user", json=data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json()) > 0)

if __name__ == "__main__":
    unittest.main()