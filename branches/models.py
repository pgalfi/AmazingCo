# Create your models here.
from django.db import models
from django.db.models import F, Case, When


class Branch(models.Model):
    name = models.CharField(max_length=100)
    up_path = models.TextField(db_index=True)
    parent = models.ForeignKey('Branch', default=None, null=True, on_delete=models.CASCADE, related_name="children")
    root = models.ForeignKey('Branch', default=None, null=True, on_delete=models.CASCADE, related_name="all_nodes")
    height = models.IntegerField(default=0)

    @property
    def full_path(self):
        return self.up_path + "/" + str(self.id)

    def __repr__(self):
        return self.name + "=" + self.up_path + " (" + str(self.height) + ")"

    def add_child(self, child_name):
        child = Branch(name=child_name, parent=self, root=self.root if self.root is not None else self,
                       height=self.height + 1, up_path=self.up_path + "/" + str(self.id))
        child.save()
        return child


class Office(models.Model):
    node_id = models.BigIntegerField()
    height = models.BigIntegerField(default=0)
    parent = models.BigIntegerField(default=None, null=True)  # node id of parent
    root = models.BigIntegerField(default=None, null=True)  # node id of root - always 0, except on root element

    name = models.CharField(max_length=100, default=None, null=True)  # optional field, only used for testing

    class Meta:
        indexes = [
            models.Index(fields=["node_id"]),
            models.Index(fields=['node_id', 'height'])
        ]

    def __repr__(self):
        return self.name + "(" + str(self.node_id) + ")"

    def get_next_sibling(self):
        next_sibling = Office.objects.filter(node_id__gt=self.node_id, height=self.height)
        if next_sibling:
            return next_sibling[0]
        return None

    def get_children(self):
        next_office = self.get_next_sibling()
        if next_office is None:
            return Office.objects.filter(node_id__gt=self.node_id, height__gt=self.height)
        else:
            return Office.objects.filter(node_id__gt=self.node_id, node_id__lt=next_office.node_id,
                                         height__gt=self.height)

    def add_child(self, new_name):
        # self may need to be refreshed before adding children to get most up to date node_id in the model
        Office.objects.filter(node_id__gt=self.node_id).update(node_id=F('node_id') + 1,
                                                               parent=Case(
                                                                   When(parent__gt=self.node_id, then=F('parent') + 1),
                                                                   default=F('parent')
                                                               ))
        child_office = Office(name=new_name, node_id=self.node_id + 1, height=self.height + 1, parent=self.node_id,
                              root=0)
        child_office.save()
        return child_office

    def move_to_parent(self, new_parent_office):
        children = self.get_children()
        children_count = children.count()
        # make space in the node_id mapping for the move
        Office.objects.filter(node_id__gt=new_parent_office.node_id).update(node_id=F('node_id') + children_count + 1,
                                                                            parent=Case(
                                                                                When(parent__gt=new_parent_office.node_id,
                                                                                     then=F('parent') + children_count + 1),
                                                                                default=F('parent')
                                                                            ))
        self.parent = new_parent_office.node_id
        # update children's node_id as per new mapping, and update their height and parent pointers
        children.update(node_id=F('node_id') - self.node_id + new_parent_office.node_id + 1,
                        height=F('height') - self.height + new_parent_office.height + 1,
                        parent=Case(
                            When(parent=self.node_id, then=new_parent_office.node_id + 1),
                            default=F('parent')
                        ))
        self.node_id = new_parent_office.node_id + 1
        self.height = new_parent_office.height + 1
        self.save()

