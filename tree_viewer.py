import tree_node as tn
import graphics as g
import sys


def run(tree1, tree2, ortographical_degree=45):
    tree_host = tn.Tree(tree1)
    tree_gene = tn.Tree(tree2)

    tree_host.create_tree()
    tree_gene.create_tree()

    tree_host.initial_node_placement()
    tree_gene.initial_node_placement()
    tree_gene.place_nodes()
    tree_host.place_nodes()

    tree_gene.calculate_min_max()
    tree_host.calculate_min_max()

    tree_gene.center()
    tree_host.center()

    gene_max = tree_gene.get_max()
    offset_host = gene_max + tree_gene.get_node_size()*2
    tree_host.offset_tree(-offset_host)

    offset_gene = tree_host.get_max
    tree_gene.offset_tree(0)

    tree_gene.match_against_host(tree_host)
    tree_gene.height_adjustment()

    g.graphics(tree_host, tree_gene, ortographical_degree)

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Not enough arguments")
        exit(1)
    else:
        tree1 = sys.argv[1]
        tree2 = sys.argv[2]
        try:
            ortographical_degree = int(sys.argv[3])
            run(tree1, tree2, ortographical_degree)
        except IndexError:
            run(tree1, tree2)
