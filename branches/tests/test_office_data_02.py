from django.test import TestCase

from branches.fixtures.offices_data_02 import load_sequence
from branches.fixtures.sequence_load import load
from branches.models import Office


class TestOfficeData(TestCase):
    fixtures = ["offices.json"]

    def setUp(self) -> None:
        self.root = Office.objects.get(node_pos=0)
        load(self.root, load_sequence)

    def test_move_01(self):
        office_aa = Office.objects.get(name="AA")
        office_a = Office.objects.get(name="A")

        office_aa.move_to_parent(self.root)
        self.assertEqual(1, office_aa.height)

        office_a.refresh_from_db()
        office_a.move_to_parent(office_aa)
        self.assertEqual(3, Office.objects.get(name="AB").height)

        office_a.move_to_parent(self.root)
        self.assertEqual(1, Office.objects.get(name="AA").height)

        office_aa.move_to_parent(office_a)
        self.assertEqual(2, Office.objects.get(name="AB").height)
