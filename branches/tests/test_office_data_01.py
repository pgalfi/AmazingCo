from django.test import TestCase

from branches.fixtures.offices_data_01 import load_sequence
from branches.fixtures.sequence_load import load
from branches.models import Office


class TestOfficeData(TestCase):
    fixtures = ["offices.json"]

    def setUp(self) -> None:
        self.root = Office.objects.get(node_pos=0)
        load(self.root, load_sequence)

    def test_data_load_00(self):
        self.assertEqual(0, Office.objects.get(pk=1).height)
        self.assertEqual(2, Office.objects.get(name="BA").height)
        self.assertEqual(Office.objects.get(name="AA").parent, Office.objects.get(name="A"))
        self.assertEqual(Office.objects.get(name="BA").parent, Office.objects.get(name="B"))

    def test_get_children_00(self):
        base_obj = Office.objects.get(name="BB")
        children = base_obj.get_children()
        self.assertEqual(2, children.count())

    def test_get_children_01(self):
        base_obj = Office.objects.get(name="AC")
        children = base_obj.get_children()
        self.assertEqual(0, children.count())

    def test_has_child_00(self):
        office_b = Office.objects.get(name="B")
        office_bbaa = Office.objects.get(name="BBAA")
        self.assertTrue(office_b.has_child(office_bbaa))

    def test_has_child_01(self):
        office_ab = Office.objects.get(name="AB")
        office_bb = Office.objects.get(name="BB")
        self.assertFalse(office_bb.has_child(office_ab))

    def test_move_00(self):
        base_obj = Office.objects.get(name="BBAA")
        self.assertEqual(4, base_obj.height)
        base_obj.move_to_parent(self.root)
        base_obj.refresh_from_db()
        self.assertEqual(1, base_obj.node_pos)
        self.assertEqual(2, Office.objects.get(name="B").node_pos)
        self.assertEqual(Office.objects.get(name="BA").parent, Office.objects.get(name="B"))

    def test_move_01(self):
        base_obj = Office.objects.get(name="BB")
        self.assertEqual(2, base_obj.height)
        base_obj.move_to_parent(Office.objects.get(name="A"))
        base_obj.refresh_from_db()
        self.assertEqual(7, base_obj.node_pos)
        self.assertEqual(1, Office.objects.get(name="B").node_pos)
        self.assertEqual(Office.objects.get(name="BA").parent, Office.objects.get(name="B"))
        self.assertEqual(Office.objects.get(name="BBA").parent, Office.objects.get(name="BB"))
