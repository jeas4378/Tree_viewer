import math

import vtk
import interactor

# Static shapes and colors used throughout.

CUBE = "cube"
CONE = "cone"
GREEN = "Green"
BLUE = "Blue"
WHITE = "White"
RED = "Red"
YELLOW = "Yellow"
GRAY = "Gray"
LIGHT_SALMON = "light_salmon"
LIME_GREEN = "lime_green"

# Initiate a color-object from the VTK-package in order to assign colors to different objects.
colors = vtk.vtkNamedColors()


def graphics(host_tree, gene_tree, ortographical_degree, custom_interactor):
    """
    The function that sets up all the graphical representation of the trees and renders them.

    :param host_tree: A Tree-object representing the host-tree.
    :param gene_tree: A Tree-object representing the guest-tree.
    :param ortographical_degree: A numerical value determening at which angle the ortographical view should kick in
                                if 'custom_interactor' is set to 'False'.
    :param custom_interactor: A boolean. If set to 'True' the user will have a more restricted control of the camera.
    :return: Nothing.
    """

    # Creates the renderer which is the Viewport of the pipeline.
    renderer = vtk.vtkRenderer()

    # Creates and add the visual representation of all the nodes in trees.
    create_graphic_nodes(host_tree, renderer, CONE, GREEN)
    create_graphic_nodes(gene_tree, renderer, CUBE, RED)

    # Creates and add the lines connecting all the nodes in respective tree.
    host_line_actor = graphics_line_placement(host_tree, LIME_GREEN)
    gene_line_actor = graphics_line_placement(gene_tree, LIGHT_SALMON)

    # Adds the lines to the Renderer.
    renderer.AddActor(host_line_actor)
    renderer.AddActor(gene_line_actor)

    # Set the background-color used in the Viewport.
    renderer.SetBackground(colors.GetColor3d("CornflowerBlue"))

    # Create the render-window which will show up on the screen and add our renderar to it.
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetSize(1280, 720)
    renWin.SetWindowName("Tree viewer")

    # Get the camera from the renderer and calculates where the focal point should be situated.
    camera = renderer.GetActiveCamera()
    x, z = calculate_focal_point(host_tree, gene_tree)
    #x /= 4
    camera.SetFocalPoint(-x, 0.5, z)

    #print(host_tree.get_x_offset(), host_tree.get_z_offset())
    #print(gene_tree.get_x_offset(), gene_tree.get_z_offset())

    # Determines where the camera itself should be placed in the XYZ-space.
    max_width = max(abs(host_tree.get_tree_width()), abs(gene_tree.get_tree_width()))
    if max_width > 1:
        node_distance = max_width * 1.7
    else:
        # If both trees are small enough then we use a standard value for placing the trees.
        node_distance = 2
    #node_distance = (gene_tree.get_node_size() * 30)
    offset_z = z + node_distance
    offset_x = x + node_distance
    camera.SetPosition(-offset_x, 0.5, offset_z)

    angle = math.atan(offset_z/-offset_x)
    angle = math.degrees(angle)
    angle = abs(angle) - 45

    # Creates an Interactor-object so the user can interact with the RenderWindow.
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Creates an object that dictate how the use can interact with the render windows.
    inter = vtk.vtkInteractorStyleTrackballCamera()
    if custom_interactor:
        inter = interactor.Interactor(YELLOW, ortographical_degree)
        inter.set_iren(iren)
        inter.set_camera(renderer.GetActiveCamera())
        inter.set_renWin(renWin)
        inter.set_renderer(renderer)
        #inter.set_current_rotate(angle)

    # Assigns the object dictating how to interact with the render window to the interactor-object.
    iren.SetInteractorStyle(inter)

    # Initializes the interactor and runs the graphical representation.
    iren.Initialize()
    iren.Start()

    #for i in range(0, 3600):  # render the image
        # render the image
     #   renWin.Render()
        # rotate the active camera by one degree
      #  renderer.GetActiveCamera().Azimuth(0.1)


def create_graphic_nodes(tree, renderer, shape, color):
    """
    A function that creates and adds a graphical representation of nodes to the Render-object.

    The reason for the loop is that each node in the graphical representation of the tree needs to be it's
    own object in order to be able to be distinguishable and clickable.

    :param tree: A Tree-object containing information of a Binary-tree.
    :param renderer: A Render-object that will be used to contain all the graphical objects.
    :param shape: The shape the graphical objects should have. Only 'CUBE' and 'CONE' is available.
    :param color: The color the nodes should have.
    :return: Nothing.
    """

    root = tree.get_root()

    graphic_obj = None

    for node in root:
        # Loops through all the nodes in the tree and creates a graphical representation for each one.
        if shape == CONE:
            graphic_obj = vtk.vtkConeSource()
            graphic_obj.SetHeight(tree.get_node_size())
            graphic_obj.SetRadius(tree.get_node_size() / 3)
            graphic_obj.SetResolution(10)
            graphic_obj.SetDirection(0, 1, 0)
        elif shape == CUBE:
            graphic_obj = vtk.vtkCubeSource()
            gene_node_size = tree.get_node_size() / 2
            graphic_obj.SetXLength(gene_node_size)
            graphic_obj.SetYLength(gene_node_size)
            graphic_obj.SetZLength(gene_node_size)

        graphic_mapper = vtk.vtkPolyDataMapper()
        graphic_mapper.SetInputConnection(graphic_obj.GetOutputPort())

        graphic_property = vtk.vtkProperty()
        graphic_property.SetColor(colors.GetColor3d(color))
        graphic_property.SetDiffuse(0.7)
        graphic_property.SetSpecular(0.4)
        graphic_property.SetSpecularPower(20)

        # In order for the the graphical representation of the node object to be placed in the XYZ-space it has to
        # have an 'Actor'-object assigned to it.
        actor = vtk.vtkActor()
        actor.SetMapper(graphic_mapper)
        actor.SetProperty(graphic_property)
        actor.SetPosition(node.get_x(), node.get_y(), node.get_z())
        renderer.AddActor(actor)


def graphics_line_placement(tree, line_color=GRAY):
    """
    A function that creates the lines between each node in the tree.

    Loops through all the nodes in the tree and constructs appropiate lines between each node to map out their
    relation to each other. With the current organization of the code if you click on one line in the tree
    you will select all lines.

    :param tree: A Tree-object containing information for a binary tree.
    :param line_color: The color the line should have. Default is 'GRAY'.
    :return: A VTK-Actor object containing all the lines for the tree.
    """

    root = tree.get_root()
    linesPolyData = vtk.vtkPolyData()
    lines = vtk.vtkCellArray()
    pts = vtk.vtkPoints()
    i = 0

    for node in root:
        # Lines are created with a start-point at the node itself and end-point at the parent-node.
        if node.get_parent():
            node_pos = [node.get_x(), node.get_y(), node.get_z()]
            node_parent = node.get_parent()
            parent_pos = [node_parent.get_x(), node_parent.get_y(), node_parent.get_z()]

            pts.InsertNextPoint(node_pos)
            pts.InsertNextPoint(parent_pos)

            linesPolyData.SetPoints(pts)

            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, i+1)
            i += 2

            lines.InsertNextCell(line)

    linesPolyData.SetLines(lines)
    color = vtk.vtkNamedColors()

    lines_graphic_property = vtk.vtkProperty()
    lines_graphic_property.SetColor(color.GetColor3d(line_color))
    lines_graphic_property.SetDiffuse(0.7)
    lines_graphic_property.SetSpecular(0)
    lines_graphic_property.SetSpecularPower(0)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(linesPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetProperty(lines_graphic_property)
    actor.GetProperty().SetLineWidth(0.01)

    return actor


def calculate_focal_point(host_tree, gene_tree):
    """
    A function that calculates the focal point based on the position of the two trees.

    :param host_tree: A Tree-object containing the host-tree.
    :param gene_tree: A Tree-object containing the guest-tree.
    :return: The numerical values for the X- and Z-coordinates for the focal point.
    """

    host_tree_min = host_tree.get_min()
    host_tree_max = host_tree.get_max()
    gene_tree_min = gene_tree.get_min()
    gene_tree_max = gene_tree.get_max()

    #Must include the position of the host tree in the x-axis.
    host_tree_x = host_tree.get_root().get_x()

    z = abs((host_tree_max + host_tree_min) / 2)
    x = abs((gene_tree_max + host_tree_x) / 2)

    return x, z
