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
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.height = 0

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
        self.distance = float(flt_level)

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

    def set_x(self, val):
        self.x = val

    def set_y(self, val):
        self.y = val

    def set_z(self, val):
        self.z = val

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def set_height(self, val):
        self.height = val

    def get_height(self):
        return self.height

    def __iter__(self):
        yield self
        if self.left_child:
            yield from self.left_child
        if self.right_child:
            yield from self.right_child


class Tree:

    def __init__(self, tree_data):
        self.root = Node()
        self.data = p.parser(tree_data)
        self.tree_info = {}
        self.height = 0
        self.x_offset = 0
        self.z_offset = 0
        self.tree_width = 0
        self.node_size = 0.1

    def get_root(self):
        return self.root

    def get_data(self):
        return self.data

    def get_height(self):
        return self.height

    def set_height(self, val):
        if val > self.get_height():
            self.height = val

    def create_update_tree_info(self, key, value):
        self.tree_info[key] = value

    def get_tree_info(self, key):
        return self.tree_info[key]

    def set_x_offset(self, val):
        self.x_offset = val

    def set_z_offset(self, val):
        self.z_offset = val

    def get_x_offset(self):
        return self.x_offset

    def get_z_offset(self):
        return self.z_offset

    def set_node_size(self, val):
        if val > 0:
            self.node_size = val

    def get_node_size(self):
        return self.node_size

    def create_tree_width(self):
        height = self.get_height()
        if height > 0:
            self.tree_width = (2**height)*self.get_node_size()

    def get_tree_width(self):
        if self.tree_width == 0:
            self.create_tree_width()
        return self.tree_width

    def create_tree(self):
        parser_data = self.get_data()
        root = self.get_root()

        self.__rec_tree(root, parser_data, 0)

    def __rec_tree(self, node, parser_data, height):

        if parser_data[0] == '(':
            left_child = Node(node)
            parser_data.pop(0)
            left_child, parser_data = self.__rec_tree(left_child, parser_data, height + 1)
            node.set_left_child(left_child)

        if parser_data[0] == ',':
            right_child = Node(node)
            parser_data.pop(0)
            right_child, parser_data = self.__rec_tree(right_child, parser_data, height + 1)
            node.set_right_child(right_child)

        if not p.is_numerical(parser_data[0]) and parser_data[0][0] != '&' and not p.is_valid_symbols(parser_data[0]):
            node.set_leaf_name(parser_data[0])
            parser_data.pop(0)

        if p.is_numerical(parser_data[0]):
            val = parser_data[0][1:]
            node.set_distance(val)
            parser_data.pop(0)

        if parser_data[0][0] == '&':
            p.primetag_extractor(node, parser_data[0])
            self.create_update_tree_info(node.get_id(), node)
            parser_data.pop(0)
            node.set_height(height)
            self.set_height(height)
            if parser_data != [] and parser_data[0] == ')':
                parser_data.pop(0)
            return node, parser_data

        if parser_data[0] == ')':
            parser_data.pop(0)
            return node, parser_data

        return node, parser_data

    def node_placement(self, host_tree=None):
        root = self.get_root()
        if host_tree is None:
            root.set_x(self.get_x_offset())
            root.set_y(1)
            width = self.get_tree_width()
            width /= 4
            self.__rec_node_placement(root.get_left_child(), self.get_x_offset(), root.get_y(), -width, None)
            self.__rec_node_placement(root.get_right_child(), self.get_x_offset(), root.get_y(), width, None)
        else:
            ac = root.get_ac()
            if ac:
                host_key = ac[0]
                host_node = host_tree.get_tree_info(host_key)
                z = host_node.get_z()
                y = host_node.get_y()
                root.set_z(z)
                root.set_y(y)
            else:
                root.set_y(1)
            width = self.get_tree_width()
            width /= 4
            self.__rec_node_placement(root.get_left_child(), -width, root.get_y() - 0.1, self.get_z_offset(), host_tree)
            self.__rec_node_placement(root.get_right_child(), width, root.get_y() - 0.1, self.get_z_offset(), host_tree)

    def __rec_node_placement(self, node, x, y, z, host_tree):

        if host_tree is None:
            node.set_x(x)
            node.set_z(z)
            y = y - node.get_distance()
            node.set_y(y)
            width = abs(z) / 2
            if node.get_left_child() is not None:
                self.__rec_node_placement(node.get_left_child(), x, node.get_y(), z - width, host_tree)
            if node.get_right_child() is not None:
                self.__rec_node_placement(node.get_right_child(), x, node.get_y(), z + width, host_tree)
        else:
            ac = node.get_ac()
            if ac:
                host_key = ac[0]
                host_node = host_tree.get_tree_info(host_key)
                z = host_node.get_z()
                y = host_node.get_y()
            node.set_z(z)
            node.set_y(y)
            node.set_x(x)

            width = abs(x) / 2
            if node.get_left_child() is not None:
                self.__rec_node_placement(node.get_left_child(), x - width, node.get_y() - 0.1, self.get_z_offset(),
                                          host_tree)
            if node.get_right_child() is not None:
                self.__rec_node_placement(node.get_right_child(), x + width, node.get_y() - 0.1, self.get_z_offset(),
                                          host_tree)

