from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from branches.api_serializers import BranchSerializer, OfficeSerializer
from branches.models import Branch, Office


class BranchViewSet(ModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()

    @action(detail=True, methods=["post"])
    def add_child(self, request, pk, **kwargs):
        branch = get_object_or_404(Branch, pk=pk)
        if "name" in request.data:
            child = branch.add_child(request.data["name"])
            return Response(BranchSerializer(child, context={"request": request}).data)
        else:
            return Response("", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put"])
    def change_parent(self, request, pk, **kwargs):
        branch = get_object_or_404(Branch, pk=pk)
        if "parent" in request.data:
            parent = get_object_or_404(Branch, pk=request.data["parent"])
            branch.parent_id = parent.id
            branch.up_path = parent.up_path + "/" + str(parent.id)
            branch.height = parent.height + 1
            branch.save()
            return Response(BranchSerializer(branch, context={"request": request}).data)
        else:
            return Response("", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def get_children(self, request, pk, **kwargs):
        branch = get_object_or_404(Branch, pk=pk)
        branch_path = branch.full_path
        nodes = Branch.objects.filter(up_path__startswith=branch_path)
        return Response(BranchSerializer(nodes, many=True, context={"request": request}).data)


class OfficeViewSet(ModelViewSet):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all().order_by("node_pos")

    def create(self, request, *args, **kwargs):
        if Office.objects.filter(node_pos=0):
            return Response({"node_pos": "root element already exists"}, status=status.HTTP_400_BAD_REQUEST)

        super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def add_child(self, request, pk, **kwargs):
        office = get_object_or_404(Office, pk=pk)
        if "name" in request.data:
            child = office.add_child(request.data["name"])
            return Response(OfficeSerializer(child, context={"request": request}).data)
        else:
            return Response({"name": "name for child node not provided"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def get_children(self, request, pk, **kwargs):
        office = get_object_or_404(Office, pk=pk)
        children = office.get_children()
        return Response(OfficeSerializer(children, many=True, context={"request": request}).data)

    @action(detail=True, methods=["put"])
    def change_parent(self, request, pk, **kwargs):
        office = get_object_or_404(Office, pk=pk)
        if "destination" in request.data:
            new_parent = get_object_or_404(Office, pk=request.data["destination"])
            office.move_to_parent(new_parent)
            return Response(OfficeSerializer(office, context={"request": request}).data)
        return Response({"destination": "destination ID needs to be provided"}, status=status.HTTP_400_BAD_REQUEST)

