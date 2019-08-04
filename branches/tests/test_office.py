from django.test import TestCase

from branches.models import Office


class TestOffice(TestCase):

    def test_initial(self):
        root = Office(name="root", node_pos=0)
        root.save()

        office_a = root.add_child("A")  # A=1
        office_b = root.add_child("B")  # B=1, A=2

        # all_offices = list(Office.objects.all().order_by("node_pos"))
        self.assertEqual(2, Office.objects.get(pk=office_a.pk).node_pos)
        office_a.refresh_from_db()

        office_aa = office_a.add_child("AA")  # AA=3
        # all_offices = list(Office.objects.all().order_by("node_pos"))

        office_ab = office_a.add_child("AB")  # AB=3, AA=4
        # all_offices = list(Office.objects.all().order_by("node_pos"))

        office_b.refresh_from_db()
        office_ba = office_b.add_child("BA")  # BA=2, A=3, AB=4, AA=5
        # all_offices = list(Office.objects.all().order_by("node_pos"))

        office_bb = office_b.add_child("BB")  # BB=2, BA=3, A=4, AB=5, AA=6
        # all_offices = list(Office.objects.all().order_by("node_pos"))

        office_bb.refresh_from_db()
        office_bba = office_bb.add_child("BBA")  # BBA=3, BA=4, A=5, AB=6, AA=7

        self.assertEqual(3, office_bba.height)
        self.assertEqual(7, Office.objects.get(pk=office_aa.pk).node_pos)
