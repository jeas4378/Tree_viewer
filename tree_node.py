class Node:

    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.name = ""

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

    def set_name(self, str_name):
        self.name = str_name


class Tree:

    def __init__(self):
        self.root = Node()

    def get_root(self):
        return self.root
