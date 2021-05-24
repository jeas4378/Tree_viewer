import vtk
import interactor

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


colors = vtk.vtkNamedColors()


def graphics(host_tree, gene_tree, ortographical_degree, custom_interactor):

    renderer = vtk.vtkRenderer()

    create_graphic_nodes(host_tree, renderer, CONE, GREEN)
    create_graphic_nodes(gene_tree, renderer, CUBE, RED)

    host_line_actor = graphics_line_placement(host_tree, LIME_GREEN)
    gene_line_actor = graphics_line_placement(gene_tree, LIGHT_SALMON)

    renderer.AddActor(host_line_actor)
    renderer.AddActor(gene_line_actor)

    renderer.SetBackground(colors.GetColor3d("CornflowerBlue"))

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetSize(1280, 720)
    renWin.SetWindowName("Tree viewer")

    camera = renderer.GetActiveCamera()
    x, z = calculate_focal_point(host_tree, gene_tree)
    #x /= 4
    camera.SetFocalPoint(-x, 0.5, z)

    #print(host_tree.get_x_offset(), host_tree.get_z_offset())
    #print(gene_tree.get_x_offset(), gene_tree.get_z_offset())

    max_width = max(abs(host_tree.get_tree_width()), abs(gene_tree.get_tree_width()))
    if max_width > 1:
        node_distance = max_width * 1.7
    else:
        node_distance = 2
    #node_distance = (gene_tree.get_node_size() * 30)
    offset_z = z + node_distance
    offset_x = x + node_distance
    camera.SetPosition(-offset_x, 0.5, offset_z)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    inter = vtk.vtkInteractorStyleTrackballCamera()
    if custom_interactor:
        inter = interactor.Interactor(YELLOW, ortographical_degree)
        inter.set_iren(iren)
        inter.set_camera(renderer.GetActiveCamera())
        inter.set_renWin(renWin)
        inter.set_renderer(renderer)

    iren.SetInteractorStyle(inter)

    iren.Initialize()
    iren.Start()

    #for i in range(0, 3600):  # render the image
        # render the image
     #   renWin.Render()
        # rotate the active camera by one degree
      #  renderer.GetActiveCamera().Azimuth(0.1)


def create_graphic_nodes(tree, renderer, shape, color):

    root = tree.get_root()

    graphic_obj = None

    for node in root:
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

        actor = vtk.vtkActor()
        actor.SetMapper(graphic_mapper)
        actor.SetProperty(graphic_property)
        actor.SetPosition(node.get_x(), node.get_y(), node.get_z())
        renderer.AddActor(actor)

def graphics_node_placement(host_tree, graphics_mapper, graphics_property):

    root = host_tree.get_root()
    graphic_actors = []
    for node in root:
        #print(node.get_id(), node.get_x(), node.get_y(), node.get_z())
        actor = vtk.vtkActor()
        actor.SetMapper(graphics_mapper)
        actor.SetProperty(graphics_property)
        actor.SetPosition(node.get_x(), node.get_y(), node.get_z())
        graphic_actors.append(actor)

    #print("\n")
    return graphic_actors


def graphics_line_placement(tree, line_color=GRAY):

    root = tree.get_root()
    linesPolyData = vtk.vtkPolyData()
    lines = vtk.vtkCellArray()
    pts = vtk.vtkPoints()
    i = 0

    for node in root:
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


def graphics_add_to_renderer(renderer, actors):

    for actor in actors:
        renderer.AddActor(actor)

    return renderer


def calculate_focal_point(host_tree, gene_tree):

    host_tree_min = host_tree.get_min()
    host_tree_max = host_tree.get_max()
    gene_tree_min = gene_tree.get_min()
    gene_tree_max = gene_tree.get_max()

    #Must include the position of the host tree in the x-axis.
    host_tree_x = host_tree.get_root().get_x()

    z = abs((host_tree_max + host_tree_min) / 2)
    x = abs((gene_tree_max + host_tree_x) / 2)

    return x, z
