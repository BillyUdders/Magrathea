import unittest
from fastapi.testclient import TestClient
from api import app

class TestMapAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_and_get_map(self):
        # 1. Create a map
        response = self.client.post("/maps", json={"size": 64, "octaves": 2})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("url", data)
        
        map_url = data["url"]
        
        # 2. Retrieve the map
        response = self.client.get(map_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "image/png")
        self.assertGreater(len(response.content), 0)

    def test_get_nonexistent_map(self):
        response = self.client.get("/maps/nonexistent-id")
        self.assertEqual(response.status_code, 404)
