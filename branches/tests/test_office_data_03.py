from django.test import TestCase

from branches.models import Office


class TestOfficeData(TestCase):
    fixtures = ["offices_test_3.json"]

    def setUp(self) -> None:
        self.root = Office.objects.get(node_pos=0)

    def test_has_child_00(self):
        current = Office.objects.get(name="BAA")
        destination = Office.objects.get(name="AA")
        self.assertFalse(current.has_child(destination))
