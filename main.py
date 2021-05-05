import tree_node as tn

if __name__ == '__main__':
    tree_host = tn.Tree('cyano.stree')
    tree_gene = tn.Tree('cyano1.rtree')

    tree_host.create_tree()
    tree_gene.create_tree()

    offset = tree_gene.get_tree_width()
    offset /= 2
    tree_host.set_x_offset(offset + 10)

    tree_host.node_placement()
    tree_gene.node_placement(tree_host)

    pass