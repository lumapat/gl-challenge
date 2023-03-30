import unittest
import json
from urllib import request

class TestAPI(unittest.TestCase):
    API_URL = "http://localhost:8000"

    def test_get_all_users(self):
        with request.urlopen(f"{self.API_URL}/users") as response:
            data = json.loads(response.read().decode())
            self.assertTrue(len(data) > 0)

if __name__ == "__main__":
    unittest.main()