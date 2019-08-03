from rest_framework.serializers import ModelSerializer

from branches.models import Branch


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "up_path", "full_path", "parent", "root", "height"]


