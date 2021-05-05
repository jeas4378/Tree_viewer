import vtk
from vtkmodules.util import colors


def graphics(host_tree, gene_tree):

    color_host = vtk.NamedColors()
    color_gene = vtk.NamedColors()

    host_graphic_obj = vtk.vtkConeSource()
    gene_graphic_obj = vtk.vtkCubeSource()

    host_graphic_mapper = vtk.vtkPolyDataMatter()
    gene_graphic_mapper = vtk.vtkPolyDataMatter()

    host_graphic_mapper.setInputConnection(host_graphic_obj.getOutputPort)
    gene_graphic_mapper.setInputConnection(gene_graphic_obj.getOutputPort)

    host_graphic_property = vtk.vtkProperty()
    host_graphic_property.SetColor(colors.GetColor3d("Green"))
    host_graphic_property.SetDiffuse(0.7)
    host_graphic_property.SetSpecular(0.4)
    host_graphic_property.SetSpecularPower(20)

    host_actors = graphics_node_placement(host_tree, host_graphic_mapper, host_graphic_property)

    gene_graphic_property = vtk.vtkProperty()
    gene_graphic_property.SetColor(colors.GetColor3d("Red"))
    gene_graphic_property.SetDiffuse(0.7)
    gene_graphic_property.SetSpecular(0.4)
    gene_graphic_property.SetSpecularPower(20)

    gene_actors = graphics_node_placement(gene_tree, gene_graphic_mapper, gene_graphic_property)

    renderer = vtk.vtkRenderer()

    renderer = graphics_add_to_renderer(renderer, host_actors)
    renderer = graphics_add_to_renderer(renderer, gene_actors)

    renderer.SetBackground(colors.GetColor3d("CornflowerBlue"))

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetSize(1280, 720)
    renWin.SetWindowName("Tree viewer")

    for i in range(0, 360):  # render the image
        # render the image
        renWin.Render()
        # rotate the active camera by one degree
        renderer.GetActiveCamera().Azimuth(1)

def graphics_node_placement(host_tree, graphics_mapper, graphics_property):

    root = host_tree.get_root()
    graphic_actors = []
    for node in root:
        actor = vtk.vtkActor()
        actor.setMapper(graphics_mapper)
        actor.setProperty(graphics_property)
        actor.setPosition(node.get_x(), node.get_y(), node.get_z())
        graphic_actors.append(actor)

    return graphic_actors


def graphics_add_to_renderer(renderer, actors):

    for actor in actors:
        renderer.addActor(actor)

    return renderer