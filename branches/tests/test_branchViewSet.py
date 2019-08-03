from django.test import TestCase
from rest_framework.test import APIClient


class TestBranchViewSet(TestCase):
    fixtures = ["branches.json"]

    def setUp(self) -> None:
        self.client = APIClient()

    def test_add_child_01(self):
        response = self.client.post("/branches/v1/branches/8/add_child/", {"name": "bac"}, format="json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, response.data["height"])
        self.assertEqual(8, response.data["parent"])

    def test_add_child_02(self):
        response = self.client.post("/branches/v1/branches/8/add_child/", {}, format="json")
        self.assertEqual(400, response.status_code)

    def test_change_parent_01(self):
        response = self.client.put("/branches/v1/branches/8/change_parent/", {"parent": 1}, format="json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data["height"])
        self.assertEqual("/1", response.data["up_path"])

    def test_change_parent_02(self):
        response = self.client.put("/branches/v1/branches/8/change_parent/", {"parent": 0}, format="json")
        self.assertEqual(404, response.status_code)

    def test_change_parent_03(self):
        response = self.client.put("/branches/v1/branches/0/change_parent/", {"parent": 0}, format="json")
        self.assertEqual(404, response.status_code)

    def test_get_children_01(self):
        response = self.client.get("/branches/v1/branches/7/get_children/", {}, format="json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_get_children_02(self):
        response = self.client.get("/branches/v1/branches/2/get_children/", {}, format="json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertEqual("aa", response.data[0]["name"])

