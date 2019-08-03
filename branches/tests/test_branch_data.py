from django.test import TestCase

from branches.models import Branch


class TestBranchData(TestCase):

    fixtures = ["branches.json"]

    def test_data_01(self):
        self.assertEqual("a", Branch.objects.get(pk=2).name)

    def test_data_02(self):
        self.assertEqual(3, Branch.objects.filter(up_path__startswith="/1/2").count())

