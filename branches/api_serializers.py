from rest_framework.fields import ReadOnlyField
from rest_framework.relations import HyperlinkedIdentityField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from branches.models import Branch, Office


class BranchSerializer(ModelSerializer):

    branch_detail = HyperlinkedIdentityField(view_name='branch-detail')

    class Meta:
        model = Branch
        fields = ["id", "name", "up_path", "full_path", "parent", "root", "height", "branch_detail"]


class OfficeSerializer(ModelSerializer):

    instance = HyperlinkedIdentityField(view_name="office-detail")
    node_pos = ReadOnlyField()
    parent = PrimaryKeyRelatedField(many=False, read_only=True)
    root = PrimaryKeyRelatedField(many=False, read_only=True)
    height = ReadOnlyField()

    class Meta:
        model = Office
        fields = ["id", "node_pos", "name", "parent", "root", "height", "instance"]

