from django.test import TestCase

from branches.models import Branch


class TestBranch(TestCase):

    def test_setup_branches(self):
        root = Branch(parent=None, root=None, height=0, node_path="")
        root.save()
        abranch = root.add_child("a")
        achildren = abranch.add_child("c"), abranch.add_child("d"), abranch.add_child("e")
        bbranch = root.add_child("b")

        self.assertEqual(6, Branch.objects.all().count())
        self.assertEqual(2, Branch.objects.get(name="d").height)
        self.assertEqual("/a/", Branch.objects.get(name="d").node_path)

