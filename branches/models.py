from django.db import models
from django.db.models import F


class Office(models.Model):
    # storage position of node in a queue-like storage of the office tree
    node_pos = models.BigIntegerField(default=0, db_index=True)
    # count of descendant nodes under this node (alocation in storage queue)
    desc_count = models.BigIntegerField(default=0)

    height = models.BigIntegerField(default=0)
    parent = models.ForeignKey('Office', default=None, null=True, on_delete=models.CASCADE,
                               related_name="direct_children")
    root = models.ForeignKey('Office', default=None, null=True, on_delete=models.CASCADE, related_name="all_nodes")

    name = models.CharField(max_length=100, default=None, null=True)  # optional field, only used for testing, display

    def __repr__(self):
        return self.name + "(" + str(self.node_pos) + "-" + str(self.height) + "-" + str(self.desc_count) + ")"

    def add_child(self, new_name):
        # increase count of descendants as new child node is about to be added, up until root element
        Office.objects.filter(node_pos__lte=self.node_pos,
                              desc_count__gte=self.node_pos - F('node_pos')).update(
            desc_count=F('desc_count') + 1
        )

        # increase queue positions for anything after this node
        Office.objects.filter(node_pos__gt=self.node_pos).update(node_pos=F('node_pos') + 1)

        child_office = Office(name=new_name, height=self.height + 1, parent=self, node_pos=self.node_pos + 1,
                              desc_count=0, root=self.root if self.root is not None else self)
        child_office.save()
        return child_office

    def get_children(self):
        return Office.objects.filter(node_pos__gt=self.node_pos, node_pos__lte=self.node_pos + self.desc_count)

    def has_child(self, office):
        return self.node_pos < office.node_pos < self.node_pos + self.desc_count

    def move_to_parent(self, new_parent_office):
        # make space in the node_pos mapping for the move
        Office.objects.filter(node_pos__gt=new_parent_office.node_pos).update(node_pos=F('node_pos') + self.desc_count + 1)
        self.refresh_from_db()
        self.parent = new_parent_office

        # update children's node_pos and next_pos as per new mapping and update their height
        self.get_children().update(
            height=F('height') - self.height + new_parent_office.height + 1,
            node_pos=F('node_pos') - self.node_pos + new_parent_office.node_pos + 1,
        )
        self.node_pos = new_parent_office.node_pos + 1
        self.height = new_parent_office.height + 1
        self.save()

