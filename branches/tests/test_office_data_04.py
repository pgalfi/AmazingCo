from django.test import TestCase

from branches.fixtures.offices_data_04 import load_sequence
from branches.fixtures.sequence_load import load
from branches.models import Office


class TestOfficeData(TestCase):
    fixtures = ["offices.json"]

    def setUp(self) -> None:
        self.root = Office.objects.get(node_pos=0)
        load(self.root, load_sequence)

    def test_get_children(self):
        office = Office.objects.get(name="B-1")
        self.assertEqual(1, office.get_children().count())

    def test_mode_children(self):
        office_C = Office.objects.get(name="C")
        office_B2 = Office.objects.get(name="B-2")
        office_C.move_to_parent(office_B2)
        office_B2.refresh_from_db()
        self.assertEqual(3, office_B2.get_children().count())
