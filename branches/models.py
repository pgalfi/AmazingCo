# Create your models here.
from django.db import models
from django.db.models import F


class Office(models.Model):
    node_pos = models.BigIntegerField(default=0)
    height = models.BigIntegerField(default=0)
    parent = models.ForeignKey('Office', default=None, null=True, on_delete=models.CASCADE, related_name="first_children")
    root = models.ForeignKey('Office', default=None, null=True, on_delete=models.CASCADE, related_name="all_nodes")

    name = models.CharField(max_length=100, default=None, null=True)  # optional field, only used for testing

    class Meta:
        indexes = [
            models.Index(fields=["node_pos"]),
            models.Index(fields=['node_pos', 'height'])
        ]

    def __repr__(self):
        return self.name + "(" + str(self.node_pos) + ")"

    def get_next_sibling(self):
        next_sibling = Office.objects.filter(node_pos__gt=self.node_pos, height=self.height)
        if next_sibling:
            return next_sibling[0]
        return None

    def get_children(self):
        next_office = self.get_next_sibling()
        if next_office is None:
            return Office.objects.filter(node_pos__gt=self.node_pos, height__gt=self.height)
        else:
            return Office.objects.filter(node_pos__gt=self.node_pos, node_pos__lt=next_office.node_pos,
                                         height__gt=self.height)

    def add_child(self, new_name):
        Office.objects.filter(node_pos__gt=self.node_pos).update(node_pos=F('node_pos') + 1)
        child_office = Office(name=new_name, node_pos=self.node_pos + 1, height=self.height + 1, parent=self,
                              root=self.root if self.root is not None else self)
        child_office.save()
        return child_office

    def move_to_parent(self, new_parent_office):
        children = self.get_children()
        children_count = children.count()
        # make space in the node_pos mapping for the move
        Office.objects.filter(node_pos__gt=new_parent_office.node_pos).update(node_pos=F('node_pos') + children_count + 1)
        self.parent = new_parent_office
        # update children's node_pos as per new mapping and update their height
        children.update(node_pos=F('node_pos') - self.node_pos + new_parent_office.node_pos + 1,
                        height=F('height') - self.height + new_parent_office.height + 1)
        self.node_pos = new_parent_office.node_pos + 1
        self.height = new_parent_office.height + 1
        self.save()

