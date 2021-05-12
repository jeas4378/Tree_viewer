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
        self.placed = False

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

    def get_placed(self):
        return self.placed

    def set_placed(self, val):
        self.placed = val

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
        self.leaves = []
        self.host = False
        self.max = 0.0
        self.min = 0.0

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

    def add_leaf(self, node):
        self.leaves.append(node)

    def get_leaves(self):
        return self.leaves

    def get_host(self):
        return self.host

    def set_host(self, val):
        self.host = val

    def get_max(self):
        return self.max

    def set_max(self, val):
        self.max = val

    def get_min(self):
        return self.min

    def set_min(self, val):
        self.min = val

    def set_min_max(self, val):
        if val > self.get_max():
            self.set_max(val)
        elif val < self.get_min():
            self.set_min(val)

    def create_tree_width(self):
        if self.get_min() != 0 and self.get_max() != 0:
            max = self.get_max()
            min = self.get_min()
            self.tree_width = max - min

    def get_tree_width(self):
        if self.tree_width == 0:
            self.create_tree_width()
        return self.tree_width

    def create_tree(self):
        parser_data = self.get_data()
        root = self.get_root()

        self.__rec_tree(root, parser_data, 0)

    def offset_tree(self, val):
        root = self.get_root()
        for node in root:
            if self.get_host():
                node.set_x(val)
            else:
                node.set_z(val)
    # def node_placement(self, host_tree):
    #     self.initial_node_placement()

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
            self.add_leaf(node)
            node.set_leaf_name(parser_data[0])
            parser_data.pop(0)

        if p.is_numerical(parser_data[0]):
            val = parser_data[0][1:]
            node.set_distance(val)
            if not self.get_host():
                self.set_host(True)
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

    def initial_node_placement(self):

        root = self.get_root()

        if self.get_host():
            root.set_x(self.get_x_offset())
        else:
            root.set_z(self.get_z_offset())
        root.set_y(1)
        width = (2 ** self.get_height()) * self.get_node_size() + (self.get_node_size())
        width /= 4
        if self.get_host():
            if root.get_left_child():
                self.__rec_initial_node_placement(root.get_left_child(),
                                                  0,
                                                  root.get_y(),
                                                  -width)
            if root.get_right_child():
                self.__rec_initial_node_placement(root.get_right_child(),
                                                  0,
                                                  root.get_y(),
                                                  width)
        else:
            if root.get_left_child():
                self.__rec_initial_node_placement(root.get_left_child(),
                                                  -width,
                                                  root.get_y() - 0.1,
                                                  0)
            if root.get_right_child():
                self.__rec_initial_node_placement(root.get_right_child(),
                                                  width,
                                                  root.get_y() - 0.1,
                                                  0)

    def __rec_initial_node_placement(self, node, x, y, z):

        width = self.get_tree_width() / 2
        node_height = node.get_height()
        width = (width / (2 ** (node_height + 1)))

        if self.get_host():
            y = y - node.get_distance()
        node.set_y(y)
        node.set_x(x)
        node.set_z(z)

        if self.get_host():
            if node.get_left_child():
                self.__rec_initial_node_placement(node.get_left_child(),
                                                  x,
                                                  y,
                                                  z - width)

            if node.get_right_child():
                self.__rec_initial_node_placement(node.get_right_child(),
                                                  x,
                                                  y,
                                                  z + width)
        else:
            if node.get_left_child():
                self.__rec_initial_node_placement(node.get_left_child(),
                                                  x - width,
                                                  y - 0.1,
                                                  z)

            if node.get_right_child():
                self.__rec_initial_node_placement(node.get_right_child(),
                                                  x + width,
                                                  y - 0.1,
                                                  z)

    def place_nodes(self):
        leaves = self.get_leaves()
        nodes = self.merge_sort(leaves)
        self.adjust_nodes(nodes)

    def merge_sort(self, nodes):
        length = len(nodes)
        nodes1 = []
        nodes2 = []
        if length > 1:
            if (length % 2) == 0:
                cut = length // 2
                nodes1 = self.merge_sort(nodes[:cut])
                nodes2 = self.merge_sort(nodes[cut:])
            else:
                cut = (length + 1) // 2
                nodes1 = self.merge_sort(nodes[:cut])
                nodes2 = self.merge_sort(nodes[cut:])

            nodes = self.merge(nodes1, nodes2)

        return nodes

    def merge(self, nodes1, nodes2):
        nodes = []
        while(nodes1 and nodes2):
            elem1 = nodes1[0]
            elem2 = nodes2[0]
            if self.get_host():
                if abs(elem1.get_z()) < abs(elem2.get_z()):
                    nodes.append(elem1)
                    nodes1.pop(0)
                else:
                    nodes.append(elem2)
                    nodes2.pop(0)
            else:
                if abs(elem1.get_x()) < abs(elem2.get_x()):
                    nodes.append(elem1)
                    nodes1.pop(0)
                else:
                    nodes.append(elem2)
                    nodes2.pop(0)

        if nodes1:
            for elem in nodes1:
                nodes.append(elem)
        else:
            for elem in nodes2:
                nodes.append(elem)

        return nodes

    def adjust_nodes(self, nodes):
        pos_axis = []
        neg_axis = []
        node_size = self.get_node_size()
        offset = node_size
        for node in nodes:
            #If the tree is a host-tree.
            if self.get_host():
                if node.get_z() > 0:
                    if pos_axis:
                        prev_node = pos_axis[-1]
                        node.set_z(prev_node.get_z() + offset)
                        pos_axis.append(node)
                    else:
                        node.set_z(offset/2)
                        pos_axis.append(node)
                else:
                    if neg_axis:
                        prev_node = neg_axis[-1]
                        node.set_z(prev_node.get_z() - offset)
                        neg_axis.append(node)
                    else:
                        node.set_z(-offset/2)
                        neg_axis.append(node)
                self.set_min_max(node.get_z())
            #If the tree is a reconciled gene-tree.
            else:
                if node.get_x() > 0:
                    if pos_axis:
                        prev_node = pos_axis[-1]
                        node.set_x(prev_node.get_x() + offset)
                        pos_axis.append(node)
                    else:
                        node.set_x(offset/2)
                        pos_axis.append(node)
                else:
                    if neg_axis:
                        prev_node = neg_axis[-1]
                        node.set_x(prev_node.get_x() - offset)
                        neg_axis.append(node)
                    else:
                        node.set_x(-offset/2)
                        neg_axis.append(node)
                self.set_min_max(node.get_x())

        while nodes:
            nodes = self.__adjust_nodes_parents(nodes)

    def __adjust_nodes_parents(self, nodes):
        parents = []

        for node in nodes:
            parent = node.get_parent()
            if parent:
                if parent not in parents:
                    self.__parent_placement(parent)
                    parents.append(parent)
            else:
                self.__parent_placement(node)

        return parents

    def __parent_placement(self, parent):
        child_left = parent.get_left_child()
        child_right = parent.get_right_child()
        if self.get_host():
            sort = sorted([child_left.get_z(), child_right.get_z()])
            min_val, max_val = sort[0], sort[-1]
            offset = (max_val + min_val) / 2
            pos = offset
            parent.set_z(pos)
        else:
            sort = sorted([child_left.get_x(), child_right.get_x()])
            min_val, max_val = sort[0], sort[-1]
            offset = (max_val + min_val) / 2
            pos = offset
            parent.set_x(pos)

    def match_against_host(self, tree):
        if not self.get_host():
            root = self.get_root()

            for node in root:
                ac = node.get_ac()
                if ac:
                    host_key = ac[0]
                    host_node = tree.get_tree_info(host_key)
                    y = host_node.get_y()
                    z = host_node.get_z()
                    node.set_y(y)
                    node.set_z(z)
