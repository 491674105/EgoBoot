class Node:
    def __init__(self, node, parent_is_dict=True, parent_id=None, parent=None):
        self.parent_is_dict = parent_is_dict
        self.node = node
        if parent_id is not None:
            self.parent_id = parent_id
        if parent is not None:
            self.parent = parent

    def get_node(self):
        return self.node

    def get_parent_id(self):
        return self.parent_id

    def get_parent(self):
        return self.parent