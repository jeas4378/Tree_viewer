class Node:

    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.id = "Null"
        self.level = -1.00

    def set_left_child(self, node):
        self.left_child = node

    def set_right_child(self, node):
        self.right_child = node

    def get_left_child(self):
        if self.left_child is not None:
            return self.left_child

    def get_right_child(self):
        if self.right_child is not None:
            return self.right_child

    def set_level(self, flt_level):
        self.level = flt_level

    def set_id(self, str_id):
        self.id = str_id

    def get_level(self):
        return self.level

    def get_id(self):
        return self.id


class Tree:

    def __init__(self):
        self.root = Node()

    def get_root(self):
        return self.root
