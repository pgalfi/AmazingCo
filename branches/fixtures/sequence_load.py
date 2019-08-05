from branches.models import Office


def load(root, sequence):
    for entry in sequence:
        parent_name = entry["parent"]
        parent_object = root
        if parent_name != "":
            parent_object = Office.objects.get(name=parent_name)
        parent_object.add_child(entry["name"])
        # all_offices = list(Office.objects.all().order_by("node_pos"))