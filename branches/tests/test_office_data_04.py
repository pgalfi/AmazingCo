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
