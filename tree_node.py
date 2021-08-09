import parser as p


class Node:
    """
    A Node-class in order create Node-objects that will be used for the Tree-class.
    """

    def __init__(self, parent=None):
        """
        Constructs all the attributes for the Node-object.

        :param parent: If this Node is a child it's parent-node is stored in order to more easily
        traverse the Tree-object later.
        """
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
        self.level = 0
        self.placed = False

    def set_left_child(self, node):
        """
        Assigns a node as left child to this node.

        :param node: A Node-object to be assigned as left child.
        :return: None.
        """
        self.left_child = node

    def set_right_child(self, node):
        """
        Assigns a node as right child to this node.

        :param node: A Node-object to be assigned as right child.
        :return: None.
        """

        self.right_child = node

    def get_left_child(self):
        """
        Returns the left child of this object if it exists.

        :return: A Node-object that is the left child.
        """
        if self.left_child is not None:
            return self.left_child

    def get_right_child(self):
        """
        Returns the right child of this object if it exists.

        :return: A Node-object that is the right child.
        """
        if self.right_child is not None:
            return self.right_child

    def set_distance(self, flt_level):
        """
        Sets the distance attribute of the node object.

        :param flt_level: An integer or float to be assigned.
        :return: None.
        """
        self.distance = float(flt_level)

    def set_id(self, str_id):
        """
        Assigns the id-attribute with an id.

        :param str_id: A String to be assigned as the id of the node.
        :return: None.
        """
        if str_id is not None:
            self.id = str_id

    def get_distance(self):
        """
        Returns the distance value for the Node.

        :return: A float representing the distance.
        """
        return self.distance

    def get_id(self):
        """
        Returns the id of the Node.

        :return: A String containing the id.
        """
        return self.id

    def get_parent(self):
        """
        Returns the parent of this Node-object.

        :return: A Node-object representing the parent.
        """
        return self.parent

    def set_host_leaf(self, val):
        """
        If this Node is a leaf in a Host-tree it can be assigned a Host-Leaf name by using this method.

        :param val: A String to assign to the attribute.
        :return: None.
        """
        if val is not None:
            self.host_leaf = val

    def get_host_leaf(self):
        """
        Returns the Host-leaf name.

        :return: A String containing the Host-Leaf name.
        """
        return self.host_leaf

    def set_leaf_name(self, val):
        """
        If the Node-object is a leaf in a guest-tree a name can be assigned with this method.

        :param val: A String containing the name to be assigned.
        :return: None.
        """
        if val is not None:
            self.leaf_name = val

    def get_leaf_name(self):
        """
        Returns the leaf-name of this Node-object.

        :return: A String containing the leaf-name.
        """
        return self.leaf_name

    def set_ac(self, val):
        """
        Assigns node-ids to the ac-attribute.

        :param val: An array containing node id's as a string.
        :return: Nothing.
        """
        if val is not None:
            self.ac = val

    def get_ac(self):
        """
        Returns the AC-nodes for associated with this node.

        :return: An array with node-ids.
        """
        return self.ac

    def set_name(self, val):
        """
        Sets the name of the node.

        :param val: A String containing the name.
        :return: Nothing.
        """
        if val is not None:
            self.name = val

    def get_name(self):
        """
        Returns the name of the node.

        :return: A String with the name.
        """
        return self.name

    def set_x(self, val):
        """
        Sets the X-position of the node.

        :param val: A numerical value representing the x-position.
        :return: Nothing.
        """
        self.x = val

    def set_y(self, val):
        """
        Sets the Y-position of the node.

        :param val: A numerical value.
        :return: Nothing.
        """
        self.y = val

    def set_z(self, val):
        """
        Sets the Z-positon of the node.

        :param val: A numerical value.
        :return: Nothing.
        """
        self.z = val

    def get_x(self):
        """
        Returns the X-position of the node.

        :return: A numerical value.
        """
        return self.x

    def get_y(self):
        """
        Returns the Y-position of the node.

        :return: A numerical value.
        """
        return self.y

    def get_z(self):
        """
        Returns the Z-position of the node.

        :return: A numerical value.
        """
        return self.z

    def set_level(self, val):
        """
        Sets which level the node resides in. The root resides on level 0. You can think of 'level' as floors in a
        high rise building. Nodes with the same value on the level attribute resides on the same floor. This information
        is important in the method '__rec_initial_node_placement' in the Tree-class.

        :param val: An Integer.
        :return: Nothing.
        """
        self.level = val

    def get_level(self):
        """
        Returns the level of the node.

        :return: An integer.
        """
        return self.level

    def get_placed(self):
        """
        Returns if this node has been placed or not.

        :return: A Boolean.
        """
        return self.placed

    def set_placed(self, val):
        """
        Sets the placed attribute. Indicates if the node has had it's position set in space.

        :param val: A boolean.
        :return: Nothing.
        """
        self.placed = val

    def __iter__(self):
        """
        The iteration of the nodes. The iteration occurs in a preorder fashion.

        :return: A Node-object.
        """
        yield self
        if self.left_child:
            yield from self.left_child
        if self.right_child:
            yield from self.right_child

    def __str__(self):
        """
        The implementation of the string-conversion. When trying to print a Node-object you will get the
        x-, y- and z-position of the Node-object on the form 'x, y, z".

        :return: A String.
        """
        m_string = str(self.get_x()) + ", " + str(self.get_y()) + ", " + str(self.get_z())
        return m_string


class Tree:

    """
    A Tree-class suited for binary trees and represents the binary tree from the input.
    """

    def __init__(self, tree_data):
        """
        Constucts all the attributes for the Tree-class.

        :param tree_data: The information required to build the tree represented as one of the input arguments
        when launching 'tree_viewer.py'. 'tree_data' points to a file which is in the PrIME-format.
        """
        self.root = Node()
        self.data = p.parser(tree_data)
        self.tree_info = {}
        self.depth = 0
        self.x_offset = 0
        self.z_offset = 0
        self.tree_width = 0
        self.node_size = 0.1
        self.leaves = []
        self.host = False
        self.max = 0.0
        self.min = 0.0

    def get_root(self):
        """
        Gets the root-node of the Tree.

        :return: A Node-object.
        """
        return self.root

    def get_data(self):
        """
        Returns the data for the structure of the tree.
        :return: An array.
        """
        return self.data

    def get_depth(self):
        """
        Returns the Depth for the tree.

        :return: An integer.
        """
        return self.depth

    def set_depth(self, val):
        """
        Sets the depth of the tree. Will only update if the new value is larger than the old value.

        :param val: An integer representing the depth.
        :return: Nothing.
        """
        if val > self.get_depth():
            self.depth = val

    def create_update_tree_info(self, key, value):
        """
        Update the 'tree_info' attribute.

        'tree_info' is a dictionary where the key is the ID of a node and the value is the node-object itself.
        This is used so that you can get a node-object by just providing the ID of the node.

        :param key: A String with the ID of a node.
        :param value: The node-object corresponding to the ID.
        :return: Nothing.
        """
        self.tree_info[key] = value

    def get_tree_info(self, key):
        """
        Get the Node-object corresponding to an node ID.

        :param key: A String with the node ID that is sought after.
        :return: The Node-object corresponding to the key.
        """
        return self.tree_info[key]

    def set_x_offset(self, val):
        """
        Offset the tree in the X-axis.

        :param val: A float.
        :return: Nothing.
        """
        self.x_offset = val

    def set_z_offset(self, val):
        """
        Offset the tree in the Z-axis.

        :param val: A float.
        :return: Nothing.
        """
        self.z_offset = val

    def get_x_offset(self):
        """
        Get the offset of the tree in the X-axis.

        :return: A float.
        """
        return self.x_offset

    def get_z_offset(self):
        """
        Get the offset of the tree in the Z-axis.
        :return: A float.
        """
        return self.z_offset

    def set_node_size(self, val):
        """
        Sets the node-size used for this tree.

        This value is used to calculate the distance between nodes as well as their graphical representation.

        :param val: A numerical value.
        :return: Nothing.
        """
        if val > 0:
            self.node_size = val

    def get_node_size(self):
        """
        Returns the node-size used for this tree.

        :return: A numerical value.
        """
        return self.node_size

    def add_leaf(self, node):
        """
        Adds a Node-object to the 'leaves'-attribute.

        This attribute is used to quickly get the nodes that are leaves in the tree.

        :param node: A Node-object.
        :return: Nothing.
        """
        self.leaves.append(node)

    def get_leaves(self):
        """
        Get all the leaves of the tree.

        :return: An array with Node-objects.
        """
        return self.leaves

    def get_host(self):
        """
        Returns the value of the 'host' attribute.

        This attribute indicates if the tree is a host-tree or not. If it's a host-tree it will be set to 'True'.

        :return: A boolean.
        """
        return self.host

    def set_host(self, val):
        """
        Sets the attribute 'host'.

        :param val: A boolean.
        :return: Nothing.
        """
        self.host = val

    def get_max(self):
        """
        Returns the value of the 'max'-attribute of the tree.

        The 'max' attribute refers to the maximum position of a node in either the X- or Z-axis depending on if
        the tree is a Host-tree or not. This value is used to shift the tree later in order to center it.

        :return: A float.
        """
        return self.max

    def set_max(self, val):
        """
        Sets the 'max'-attribute.

        :param val: A float.
        :return: Nothing.
        """
        self.max = val

    def get_min(self):
        """
        Returns the value of the 'min'-attribute of the tree.

        Like with the 'max'-attribute the 'min'-attribute holds the minimum value that a node in the tree has
        in either the X- or Z-axis depending on if the tree is a Host-tree or not.

        :return: A float.
        """
        return self.min

    def set_min(self, val):
        """
        Sets the 'min'-attribute.

        :param val: A float.
        :return: Nothing.
        """
        self.min = val

    def print_leaves(self):
        """
        A method to print out the information for all the leaves in the tree.

        :return: Nothing.
        """
        leaves = self.get_leaves()
        for leaf in leaves:
            print(leaf)

    def __str__(self):
        """
        Prints out the whole tree.

        :return: A String with the information of the tree.
        """
        root = self.get_root()
        m_string = ""
        for node in root:
            m_string += str(node) + "\n"
        return m_string

    def calculate_min_max(self):
        """
        Checks all the nodes in the tree stores the values of the nodes with the maximum and minimum value
        in either the X- or Z-axis depending on if the tree is a Host-tree or not.

        :return: Nothing.
        """
        root = self.get_root()
        for node in root:
            if self.get_host():
                self.set_min_max(node.get_z())
            else:
                self.set_min_max(node.get_x())

    def set_min_max(self, val):
        """
        Sets the 'max'- and 'min'-attribute of the tree if the incoming value is greater or smaller than the existing
        max- and min-value respectively.

        :param val: A float.
        :return: Nothing.
        """
        if val > self.get_max():
            self.set_max(val)
        elif val < self.get_min():
            self.set_min(val)

    def reset_min_max(self):
        """
        Sets the values of the 'max' -and 'min'-attribute to 0 for the tree.

        :return: Nothing.
        """
        self.set_max(0)
        self.set_min(0)

    def create_tree_width(self):
        """
        Calculates the width of the tree.

        :return: Nothing.
        """
        if self.get_min() != 0 and self.get_max() != 0:
            max_pos = self.get_max()
            min_pos = self.get_min()
            self.tree_width = max_pos - min_pos

    def get_tree_width(self):
        """
        Returns the width of the tree.

        :return: A float.
        """
        if self.tree_width == 0:
            self.create_tree_width()
        return self.tree_width

    def create_tree(self):
        """
        The method that creates the tree by calling the recursive-function '__rec_tree'.

        :return: Nothing.
        """
        parser_data = self.get_data()
        root = self.get_root()

        self.__rec_tree(root, parser_data, 0)

    def offset_tree(self, val):
        """
        Offsets all the nodes in tree in the X- or Z-axis depending on if the tree is a host tree or not.

        :param val: A numerical value to offset the nodes by.
        :return: Nothing.
        """
        root = self.get_root()
        for node in root:
            if self.get_host():
                node.set_x(val)
            else:
                node.set_z(val)

    def center(self):
        """
        Centers the tree over the origin.

        :return: Nothing.
        """
        min_val = self.get_min()
        max_val = self.get_max()
        width = max_val - min_val
        rel_midpoint = width / 2
        desired_midpoint = max_val - rel_midpoint

        # If the tree is more on the positive side than the negative side of the axis it has to be shifted
        # in the negative direction and vice versa.
        if abs(max_val) > abs(min_val):
            self.shift(-abs(desired_midpoint))
        else:
            self.shift(abs(desired_midpoint))

    def shift(self, val):
        """
        A method that shifts the whole tree in the X- or Z-axis depending on if the tree is a Host-tree or not.

        :param val: A numerical value.
        :return: Nothing.
        """
        root = self.get_root()
        self.reset_min_max()
        for node in root:
            if self.get_host():
                z_pos = node.get_z()
                new_pos = z_pos + val
                node.set_z(new_pos)
                self.set_min_max(node.get_z())
            else:
                x_pos = node.get_x()
                new_pos = x_pos + val
                node.set_x(new_pos)
                self.set_min_max(node.get_x())

    # def node_placement(self, host_tree):
    #     self.initial_node_placement()

    def __rec_tree(self, node, parser_data, height):
        """
        A recursive method that builds the tree based on the 'parser_data'.

        :param node: A Node-object.
        :param parser_data: An array with the data for the whole tree.
        :param height: A numerical value.
        :return: Nothing.
        """

        # If a '(' is the first element in 'parser_data' it means that should make a left child-node.
        if parser_data[0] == '(':
            left_child = Node(node)
            # To get the next datapoint for the recursive method to act on we pop the first element from 'parser_data'.
            parser_data.pop(0)
            left_child, parser_data = self.__rec_tree(left_child, parser_data, height + 1)
            node.set_left_child(left_child)
            if not p.is_numerical(parser_data[0]) and parser_data[0][0] != '&' and not p.is_valid_symbols(
                    parser_data[0]):
                node.set_name(parser_data[0])
                parser_data.pop(0)

        # If a ',' is encountered next we have a right child that needs to be created.
        if parser_data[0] == ',':
            right_child = Node(node)
            parser_data.pop(0)
            right_child, parser_data = self.__rec_tree(right_child, parser_data, height + 1)
            node.set_right_child(right_child)
            if not p.is_numerical(parser_data[0]) and parser_data[0][0] != '&' and not p.is_valid_symbols(
                    parser_data[0]):
                node.set_name(parser_data[0])
                parser_data.pop(0)

        # If there is no information to indicate that we have to "move down" in the tree we assign the node as a leaf.
        if not p.is_numerical(parser_data[0]) and parser_data[0][0] != '&' and not p.is_valid_symbols(parser_data[0]):
            self.add_leaf(node)
            node.set_leaf_name(parser_data[0])
            parser_data.pop(0)

        # If we have a value on the form ':x.xxx' where 'x' are digits then we know that this tells the distance from
        # this node to the root-node. We store this value.
        if p.is_numerical(parser_data[0]):
            val = parser_data[0][1:]
            node.set_distance(val)
            if not self.get_host():
                self.set_host(True)
            parser_data.pop(0)

        # If we have a PrIME-tag we take the following steps to extract the information from it and store it with
        # this node.
        if parser_data[0][0] == '&':
            p.primetag_extractor(node, parser_data[0])
            self.create_update_tree_info(node.get_id(), node)
            parser_data.pop(0)
            node.set_level(height)
            self.set_depth(height)
            if parser_data != [] and parser_data[0] == ')':
                parser_data.pop(0)
            return node, parser_data

        # A ')' tells us to move one step up in the hierarchy.
        if parser_data[0] == ')':
            parser_data.pop(0)
            return node, parser_data

        return node, parser_data

    def initial_node_placement(self):
        """
        Makes the initial "worst case"-placement of all the nodes to make sure that two nodes on the same level don't
        encroach on each other.

        :return: Nothing.
        """

        root = self.get_root()

        if self.get_host():
            root.set_x(self.get_x_offset())
        else:
            root.set_z(self.get_z_offset())
        root.set_y(1)
        # We calculate the maximum theoretical width of the tree with respect to the node-size.
        width = (2 ** self.get_depth()) * self.get_node_size() + (self.get_node_size())
        # Since the root-node will be placed in the middle of the width the roots children should be placed half of half
        # to each side, or 1/4 of the total width.
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
            # Due to guest-trees not having a distance-attribute most of the time we use the current nodes y-value minus
            # the node-size for it's child nodes.
            if root.get_left_child():
                self.__rec_initial_node_placement(root.get_left_child(),
                                                  -width,
                                                  root.get_y() - self.get_node_size(),
                                                  0)
            if root.get_right_child():
                self.__rec_initial_node_placement(root.get_right_child(),
                                                  width,
                                                  root.get_y() - self.get_node_size(),
                                                  0)

    def __rec_initial_node_placement(self, node, x, y, z):
        """
        The recursive method that places all the nodes.

        :param node: A Node-object.
        :param x: A numerical value.
        :param y: A numerical value.
        :param z: A numerical value.
        :return: Nothing.
        """

        # Calculate the maximum theoretical width of the tree with respect to the  node-size.
        width = (2 ** self.get_depth()) * self.get_node_size() + (self.get_node_size())
        node_height = node.get_level()
        # Since the roots position is 1/2 of the maximum width and the root is on level 0 we have +1 to the value
        # for the calculation to make sense. As in "Width / 2⁰ = Width" which doesn't make sense.
        # However "Width / 2¹ = 1/2*width". The reason for +2 is because we want to calculate the width for this nodes
        # children.
        width = (width / (2 ** (node_height + 2)))

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
                                                  y - self.get_node_size(),
                                                  z)

            if node.get_right_child():
                self.__rec_initial_node_placement(node.get_right_child(),
                                                  x + width,
                                                  y - self.get_node_size(),
                                                  z)

    def place_nodes(self):
        """
        Makes the final placement of the nodes.

        :return: Nothing.
        """
        leaves = self.get_leaves()
        nodes = self.merge_sort(leaves)
        self.adjust_nodes(nodes)

    def merge_sort(self, nodes):
        """
        Standard implementaion of the Merge-Sort algorithm.

        The purpose of the method is to sort the nodes from the smallest value to the largest value on the
        X- or Z-axis depending on if they are part of a Host-tree or not.

        :param nodes: An array with Node-objects to be sorted.
        :return: An array with sorted nodes.
        """
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
        """
        Merges two arrays with Node-objects with respect to their X- or Z-axis depending on if they are part of a
        Host tree or not.

        :param nodes1: An array with Node-objects.
        :param nodes2: An array with Node-objects.
        :return: An array with sorted Node-objects.
        """
        nodes = []
        while (nodes1 and nodes2):
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

        # If there are Node-objects left they are added to the array named 'nodes'.
        if nodes1:
            for elem in nodes1:
                nodes.append(elem)
        else:
            for elem in nodes2:
                nodes.append(elem)

        return nodes

    def adjust_nodes(self, nodes):
        """
        This function first packs the leaves of the tree as tightly together as possible extending in the positive and
        negative direction. After that it goes thorugh the leaves parents and places them right in between it's children.

        :param nodes: An array with sorted Node-objects.
        :return: Nothing.
        """
        pos_axis = []
        neg_axis = []
        node_size = self.get_node_size()
        offset = node_size * 1.2
        for node in nodes:
            # If the tree is a host-tree.
            if self.get_host():
                if node.get_z() > 0:
                    if pos_axis:
                        # In order to know what value the current node should be set to we need to know the value
                        # of the previous node.
                        prev_node = pos_axis[-1]
                        node.set_z(prev_node.get_z() + offset)
                        pos_axis.append(node)
                    else:
                        node.set_z(offset / 2)
                        pos_axis.append(node)
                else:
                    if neg_axis:
                        prev_node = neg_axis[-1]
                        node.set_z(prev_node.get_z() - offset)
                        neg_axis.append(node)
                    else:
                        node.set_z(-offset / 2)
                        neg_axis.append(node)

            # If the tree is a guest-tree.
            else:
                if node.get_x() > 0:
                    if pos_axis:
                        prev_node = pos_axis[-1]
                        node.set_x(prev_node.get_x() + offset)
                        pos_axis.append(node)
                    else:
                        node.set_x(offset / 2)
                        pos_axis.append(node)
                else:
                    if neg_axis:
                        prev_node = neg_axis[-1]
                        node.set_x(prev_node.get_x() - offset)
                        neg_axis.append(node)
                    else:
                        node.set_x(-offset / 2)
                        neg_axis.append(node)

        #Adjust the parents of the leave nodes. This loop is essentially recursive.
        while nodes:
            nodes = self.__adjust_nodes_parents(nodes)

    def __adjust_nodes_parents(self, nodes):
        """
        This method adjust the position of the parent-nodes.

        :param nodes: An array with Node-objects that are the leaves in the tree.
        :return: An array with Node-objects consisting of the parents.
        """
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
        """
        This method takes a Node-object that is a parent and places it right in between it's children.

        :param parent: A Node-object.
        :return: Nothing.
        """
        child_left = parent.get_left_child()
        child_right = parent.get_right_child()
        if self.get_host():
            sort = sorted([child_left.get_z(), child_right.get_z()])
            min_val, max_val = sort[0], sort[-1]
            offset = (max_val - min_val) / 2
            pos = offset + min_val
            parent.set_z(pos)
        else:
            sort = sorted([child_left.get_x(), child_right.get_x()])
            min_val, max_val = sort[0], sort[-1]
            offset = (max_val - min_val) / 2
            pos = offset + min_val
            parent.set_x(pos)

    def match_against_host(self, tree):
        """
        If the tree is a guest-tree this method will try and match the nodes in the Y- and Z-axis to the first host-node
        listed in the AC-attribute.
        :param tree:
        :return:
        """
        if not self.get_host():
            root = self.get_root()
            root_host = tree.get_root()

            root.set_y(root_host.get_y())
            root.set_z(root_host.get_z())

            for node in root:
                ac = node.get_ac()
                if ac:
                    host_key = ac[0]
                    host_node = tree.get_tree_info(host_key)
                    y = host_node.get_y()
                    z = host_node.get_z()
                    node.set_y(y)
                    node.set_z(z)

    def height_adjustment(self):
        """
        This method adjusts the nodes of the tree in the Y-axis with respects to their children.

        After the guest-tree has had it's node matched against potential nodes in the host-tree there can arise a
        situation where the parent of a node is lower than the node itself in the Y-axis. This node method adjusts
        so that a parent-node is always above its children.

        :return: Nothing.
        """
        root = self.get_root()
        for node in root:
            parent = node.get_parent()
            if parent:
                current_height = node.get_y()
                if parent.get_y() <= current_height:
                    max_height = max(node.get_left_child().get_y(),
                                     node.get_right_child().get_y())
                    height = (parent.get_y() + max_height) / 2
                    node.set_y(height)
