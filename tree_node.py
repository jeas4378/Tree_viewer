import parser as p

class Node:

    def __init__(self, parent=None):
        self.left_child = None
        self.right_child = None
        self.id = "Null"
        self.distance = -1.00
        self.host_leaf = "No host leaf"
        self.leaf_name = "Not leaf"
        self.ac = []
        self.name = "No name"
        self.parent = parent

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

    def set_distance(self, flt_level):
        self.distance = flt_level

    def set_id(self, str_id):
        if str_id is not None:
            self.id = str_id

    def get_distance(self):
        return self.distance

    def get_id(self):
        return self.id

    def get_parent(self):
        return self.parent

    def set_host_leaf(self, val):
        if val is not None:
            self.host_leaf = val

    def get_host_leaf(self):
        return self.host_leaf

    def set_leaf_name(self, val):
        if val is not None:
            self.leaf_name = val

    def get_leaf_name(self):
        return self.leaf_name

    def set_ac(self, val):
        if val is not None:
            self.ac = val

    def get_ac(self):
        return self.ac

    def set_name(self, val):
        if val is not None:
            self.name = val

    def get_name(self):
        return self.name



class Tree:

    def __init__(self, tree_data):
        self.root = Node()
        self.data = p.parser(tree_data)

    def get_root(self):
        return self.root

    def get_data(self):
        return self.data

    def create_tree(self):
        parser_data = self.get_data()
        root = self.get_root()
        index = 0

        if parser_data[index] == '(':
            left_child = Node(root)
            left_child, index = self.__rec_tree(left_child, parser_data, index+1)
            root.set_left_child(left_child)

        if parser_data[index] == ",":
            right_child = Node(root)
            right_child, index = self.__rec_tree(right_child, parser_data, index+1)
            root.set_right_child(right_child)

        if parser_data[index][0] == '&':
            id, host_leaf, ac, name = p.primetag_extractor(parser_data[index])
            root.set_id(id)
            root.set_host_leaf(host_leaf)
            root.set_ac(ac)
            root.set_name(name)


    def __rec_tree(self, node, parser_data, index):

        if parser_data[index] == ')':
            return node, index + 1

        if not p.is_numerical(parser_data[index]) and parser_data[index][0] != '&':
            node.set_leaf_name(parser_data[index])
            index += 1

        if p.is_numerical(parser_data[index]):
            val = parser_data[index][1:]
            node.set_distance(val)
            index += 1

        if parser_data[index][0] == '&':
            id, host_leaf, ac, name = p.primetag_extractor(parser_data[index])
            node.set_id(id)
            node.set_host_leaf(host_leaf)
            node.set_ac(ac)
            node.set_name(name)
            index += 1

        if parser_data[index] == '(':
            left_child = Node(node)
            left_child, index = self.__rec_tree(left_child, parser_data, index + 1)
            node.set_left_child(left_child)

        if parser_data[index] == ',':
            right_child = Node(node)
            right_child, index = self.__rec_tree(right_child, parser_data, index + 1)
            node.set_right_child(right_child)

