import tree_node as tn
import graphics as g
import sys

# The main file for this application.

def run(tree1, tree2, ortographical_degree=45, custom_interactor=False):
    """
    This function creates the initial trees and place all the nodes before calling the graphics package.

    :param tree1: A file representing the host-tree in PrIME-format.
    :param tree2: A file representing the guest-tree in PrIME-format.
    :param ortographical_degree: A numerical value indicating at which angle the ortographic view will kick in.
    :param custom_interactor: A boolean. If 'True' the user will have a more restricted control of the camera.
    :return: Nothing.
    """

    # Initiates the tree-objects.
    tree_host = tn.Tree(tree1)
    tree_gene = tn.Tree(tree2)

    # Creates the trees.
    tree_host.create_tree()
    tree_gene.create_tree()

    # Make the initial node placement of all the trees in XYZ-space.
    tree_host.initial_node_placement()
    tree_gene.initial_node_placement()

    # Tightens all the nodes together.
    tree_gene.place_nodes()
    tree_host.place_nodes()

    # Calculate the minimum and maximum placement of nodes in the X- or Z-axis depending on if the tree is a host-tree
    # or not.
    tree_gene.calculate_min_max()
    tree_host.calculate_min_max()

    # Center the trees above the origin.
    tree_gene.center()
    tree_host.center()

    # Shifts the trees in the X- and Z-axis respectively so they dont encroach on each others space.
    gene_max = tree_gene.get_max()
    offset_host = gene_max + tree_gene.get_node_size()*2
    tree_host.offset_tree(-offset_host)

    offset_gene = tree_host.get_max
    tree_gene.offset_tree(0)

    # Matches the each node in the guest-tree against the respective node in the host-tree.
    tree_gene.match_against_host(tree_host)
    tree_gene.height_adjustment()

    # Initializes the graphical representation of the trees.
    g.graphics(tree_host, tree_gene, ortographical_degree, custom_interactor)

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Not enough arguments")
        exit(1)
    else:
        tree1 = sys.argv[1]
        tree2 = sys.argv[2]
        try:
            ortographical_degree = int(sys.argv[3])
            run(tree1, tree2, ortographical_degree, True)
        except IndexError:
            run(tree1, tree2, 45, False)
