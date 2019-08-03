from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from branches.models import Branch


class BranchSerializer(ModelSerializer):

    branch_detail = HyperlinkedIdentityField(view_name='branch-detail')

    class Meta:
        model = Branch
        fields = ["id", "name", "up_path", "full_path", "parent", "root", "height", "branch_detail"]


