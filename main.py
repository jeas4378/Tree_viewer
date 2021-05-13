import tree_node as tn
import graphics as g

if __name__ == '__main__':
    tree_host = tn.Tree('ex_host.txt')
    tree_gene = tn.Tree('ex_gene.txt')

    tree_host.create_tree()
    tree_gene.create_tree()

    # offset = tree_gene.get_tree_width()
    # offset /= 2
    # tree_host.set_x_offset(offset + (tree_gene.get_node_size()*5))
    #
    # offset = tree_host.get_tree_width()
    # offset /= 2
    # tree_gene.set_z_offset(offset + (tree_host.get_node_size()*5))

    tree_host.initial_node_placement()
    tree_gene.initial_node_placement()
    tree_gene.place_nodes()
    tree_host.place_nodes()

    offset_host = tree_gene.get_tree_width()
    #offset_host /= 2
    tree_host.offset_tree(-offset_host/2)

    offset_gene = tree_host.get_tree_width()
    #offset_gene /= 2
    tree_gene.offset_tree(-offset_gene/2)
    tree_gene.match_against_host(tree_host)
    tree_gene.height_adjustment()
   # tree_gene.node_placement(tree_host)

    g.graphics(tree_host, tree_gene)

    pass