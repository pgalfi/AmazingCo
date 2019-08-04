from django.test import TestCase

from branches.fixtures.offices_data import load_sequence
from branches.models import Office


class TestOfficeData(TestCase):
    fixtures = ["offices.json"]

    def setUp(self) -> None:
        self.root = Office.objects.get(node_id=0)
        for entry in load_sequence:
            parent_name = entry["parent"]
            parent_object = self.root
            if parent_name != "":
                parent_object = Office.objects.get(name=parent_name)
            parent_object.add_child(entry["name"])

    def test_data_load_00(self):
        self.assertEqual(0, Office.objects.get(pk=1).height)
        self.assertEqual(2, Office.objects.get(name="BA").height)
        self.assertEqual(Office.objects.get(name="AA").parent, Office.objects.get(name="A").node_id)
        self.assertEqual(Office.objects.get(name="BA").parent, Office.objects.get(name="B").node_id)

    def test_get_children_00(self):
        base_obj = Office.objects.get(name="BB")
        children = base_obj.get_children()
        self.assertEqual(2, children.count())

    def test_get_children_01(self):
        base_obj = Office.objects.get(name="AC")
        children = base_obj.get_children()
        self.assertEqual(0, children.count())

    def test_move_00(self):
        base_obj = Office.objects.get(name="BBAA")
        self.assertEqual(4, base_obj.height)
        base_obj.move_to_parent(self.root)
        base_obj.refresh_from_db()
        self.assertEqual(1, base_obj.node_id)
        self.assertEqual(2, Office.objects.get(name="B").node_id)
        self.assertEqual(Office.objects.get(name="BA").parent, Office.objects.get(name="B").node_id)

    def test_move_01(self):
        base_obj = Office.objects.get(name="BB")
        self.assertEqual(2, base_obj.height)
        base_obj.move_to_parent(Office.objects.get(name="A"))
        base_obj.refresh_from_db()
        self.assertEqual(7, base_obj.node_id)
        self.assertEqual(1, Office.objects.get(name="B").node_id)
        self.assertEqual(Office.objects.get(name="BA").parent, Office.objects.get(name="B").node_id)
        self.assertEqual(Office.objects.get(name="BBA").parent, Office.objects.get(name="BB").node_id)
