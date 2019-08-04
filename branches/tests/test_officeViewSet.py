from django.test import TestCase
from rest_framework.test import APIClient

from branches.models import Office


class TestOfficeViewSet(TestCase):

    def setUp(self) -> None:
        self.root = Office(name="root", node_pos=0)
        self.root.save()
        self.client = APIClient()

    def test_create(self):
        response = self.client.post("/branches/v1/offices/", {"name": "special root"}, format="json")
        self.assertEqual(400, response.status_code)

    def test_add_child(self):
        response = self.client.post("/branches/v1/offices/" + str(self.root.id) + "/add_child/",
                                    {"name": "A"}, format="json")
        self.assertEqual(200, response.status_code)
        office_a = Office.objects.get(name="A")
        self.assertEqual(self.root.id, office_a.parent_id)
        response = self.client.post("/branches/v1/offices/" + str(self.root.id) + "/add_child/",
                                    {"name": "B"}, format="json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.root.id, Office.objects.get(name="B").parent_id)
        office_a.refresh_from_db()
        response = self.client.post("/branches/v1/offices/" + str(office_a.id) + "/add_child/",
                                    {"name": "AA"}, format="json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, Office.objects.get(name="AA").height)

    def test_get_children(self):
        response = self.client.post("/branches/v1/offices/" + str(self.root.id) + "/add_child/",
                                    {"name": "A"}, format="json")
        self.assertEqual(200, response.status_code)
        response = self.client.post("/branches/v1/offices/" + str(self.root.id) + "/add_child/",
                                    {"name": "B"}, format="json")
        self.assertEqual(200, response.status_code)
        response = self.client.post("/branches/v1/offices/" + str(self.root.id) + "/add_child/",
                                    {"name": "C"}, format="json")
        self.assertEqual(200, response.status_code)
        response = self.client.get("/branches/v1/offices/", format="json")
        self.assertEqual(4, len(response.data))

    def test_change_parent(self):
        response = self.client.post("/branches/v1/offices/" + str(self.root.id) + "/add_child/",
                                    {"name": "A"}, format="json")
        self.assertEqual(200, response.status_code)

        response = self.client.post("/branches/v1/offices/" + str(Office.objects.get(name="A").id) + "/add_child/",
                                    {"name": "B"}, format="json")
        self.assertEqual(200, response.status_code)
        response = self.client.post("/branches/v1/offices/" + str(Office.objects.get(name="B").id) + "/add_child/",
                                    {"name": "C"}, format="json")
        self.assertEqual(200, response.status_code)
        response = self.client.put("/branches/v1/offices/" + str(Office.objects.get(name="C").id) + "/change_parent/",
                                   {"destination": "1"}, format="json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.root.id, Office.objects.get(name="C").parent_id)

