# Create your models here.
from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)
    node_path = models.TextField(db_index=True)
    parent = models.ForeignKey('Branch', default=None, null=True, on_delete=models.CASCADE, related_name="children")
    root = models.ForeignKey('Branch', default=None, null=True, on_delete=models.CASCADE, related_name="all_nodes")
    height = models.IntegerField(default=0)

    @property
    def full_path(self):
        return self.node_path + self.name

    def __repr__(self):
        return self.name + "=" + self.node_path + " (" + str(self.height) + ")"

    def add_child(self, child_name):
        child = Branch(name=child_name, parent=self, root=self.root if self.root is not None else self,
                       height=self.height + 1, node_path=self.node_path + self.name + "/")
        child.save()
        return child

