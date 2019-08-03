from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from branches.api_serializers import BranchSerializer
from branches.models import Branch


class BranchViewSet(ModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()

    @action(detail=True, methods=["post"])
    def add_child(self, request, pk, **kwargs):
        branch = get_object_or_404(Branch, pk=pk)
        if "name" in request.data:
            child = branch.add_child(request.data["name"])
            return Response(BranchSerializer(child).data)
        else:
            return Response("", status=status.HTTP_400_BAD_REQUEST)

