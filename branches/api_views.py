from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from branches.api_serializers import OfficeSerializer
from branches.models import Office


class OfficeViewSet(ModelViewSet):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all().order_by("node_pos")

    def create(self, request, *args, **kwargs):
        if "parentId" not in request.data:
            return Response({"parentId": "parent ID must be specified"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data["parentId"] is None and Office.objects.filter(node_pos=0):
            return Response({"node_pos": "root element already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data["parentId"] is None:
            root = Office(name = request.data["name"])
            root.save()
            return Response(OfficeSerializer(root, context={"request": request}).data)

        office = get_object_or_404(Office, pk=request.data["parentId"])
        if "name" in request.data:
            child = office.add_child(request.data["name"])
            return Response(OfficeSerializer(child, context={"request": request}).data)
        else:
            return Response({"name": "name for child node not provided"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        office = self.get_object()
        if "parentId" in request.data and office.parent_id != request.data["parentId"]:
            new_parent = get_object_or_404(Office, pk=request.data["parentId"])
            if not office.has_child(new_parent):
                office.move_to_parent(new_parent)
                return Response(OfficeSerializer(office, context={"request": request}).data)
            else:
                return Response({"parentId": "new parent is a child of current node, invalid move"},
                                status=status.HTTP_400_BAD_REQUEST)
        super().update(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def get_children(self, request, pk, **kwargs):
        office = get_object_or_404(Office, pk=pk)
        children = office.get_children()
        return Response(OfficeSerializer(children, many=True, context={"request": request}).data)
