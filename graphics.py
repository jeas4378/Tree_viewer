import vtk
import tree_node
from vtkmodules.util import colors

class Interactor(vtk.vtkInteractorStyleUser):

    def __init__(self, parent=None):
        self.iren = None
        self.renWin = None
        self.max_rotate = 45
        self.min_rotate = -45
        self.current_rotate = 0
        self.boolRotate = 0
        self.AddObserver("LeftButtonPressEvent", self.left_button_press)
        self.AddObserver("LeftButtonReleaseEvent", self.left_button_release)
        self.AddObserver("MouseMoveEvent", self.mouse_event)
        self.camera = None

    def left_button_press(self, obj, event):
        self.boolRotate = 1
        return

    def left_button_release(self, obj, event):
        self.boolRotate = 0
        return

    def mouse_event(self, obj, event):
        last_xy_pos = self.iren.GetLastEventPosition()
        last_x = last_xy_pos[0]

        xy_pos = self.iren.GetEventPosition()
        x = xy_pos[0]

        if self.get_boolRotate() and self.is_in_valid_range(x, last_x):
            self.rotate(x, last_x)

    def rotate(self, x, last_x):
        rotate_diff = last_x - x

        self.get_camera().Azimuth(rotate_diff)
        self.set_current_rotate(rotate_diff)
        self.get_camera().OrthogonalizeViewUp()
        self.get_renWin().Render()


    def get_current_rotate(self):
        return self.current_rotate

    def get_min_rotate(self):
        return self.min_rotate

    def get_max_rotate(self):
        return self.max_rotate

    def set_current_rotate(self, x):
        self.current_rotate += x

    def get_camera(self):
        return self.camera

    def get_renWin(self):
        return self.renWin

    def set_renWin(self, renWin):
        self.renWin = renWin

    def set_camera(self, camera):
        self.camera = camera

    def set_iren(self, iren):
        self.iren = iren

    def get_boolRotate(self):
        return self.boolRotate

    def is_in_valid_range(self, x, last_x):
        diff = last_x - x
        if self.get_max_rotate() > self.get_current_rotate() > self.get_min_rotate():
            return True
        else:
            if self.get_current_rotate() >= self.get_max_rotate() and diff < 0:
                return True
            elif self.get_current_rotate() <= self.get_min_rotate() and diff > 0:
                return True
            else:
                return False



def graphics(host_tree, gene_tree):

    colors = vtk.vtkNamedColors()

    host_graphic_obj = vtk.vtkConeSource()
    host_graphic_obj.SetHeight(host_tree.get_node_size())
    host_graphic_obj.SetRadius(host_tree.get_node_size() / 3)
    host_graphic_obj.SetResolution(10)
    host_graphic_obj.SetDirection(0, 1, 0)

    gene_graphic_obj = vtk.vtkCubeSource()
    gene_node_size = gene_tree.get_node_size() / 2
    gene_graphic_obj.SetXLength(gene_node_size)
    gene_graphic_obj.SetYLength(gene_node_size)
    gene_graphic_obj.SetZLength(gene_node_size)

    host_graphic_mapper = vtk.vtkPolyDataMapper()
    gene_graphic_mapper = vtk.vtkPolyDataMapper()

    host_graphic_mapper.SetInputConnection(host_graphic_obj.GetOutputPort())
    gene_graphic_mapper.SetInputConnection(gene_graphic_obj.GetOutputPort())

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

    host_line_actor = graphics_line_placement(host_tree)
    gene_line_actor = graphics_line_placement(gene_tree)

    renderer = vtk.vtkRenderer()

    renderer = graphics_add_to_renderer(renderer, host_actors)
    renderer = graphics_add_to_renderer(renderer, gene_actors)

    renderer.AddActor(host_line_actor)
    renderer.AddActor(gene_line_actor)

    renderer.SetBackground(colors.GetColor3d("CornflowerBlue"))

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetSize(1280, 720)
    renWin.SetWindowName("Tree viewer")

    camera = renderer.GetActiveCamera()
    camera.SetFocalPoint(0, 0.5, 0)

    #print(host_tree.get_x_offset(), host_tree.get_z_offset())
    #print(gene_tree.get_x_offset(), gene_tree.get_z_offset())

    if abs(host_tree.get_x_offset()) > abs(gene_tree.get_z_offset()):
        offset = host_tree.get_x_offset() + (host_tree.get_node_size() * 20)
        camera.SetPosition(offset, 0.5, offset)
    else:
        offset = gene_tree.get_z_offset() + (gene_tree.get_node_size() * 20)
        camera.SetPosition(offset, 0.5, offset)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    inter = Interactor()
    inter.set_iren(iren)
    inter.set_camera(renderer.GetActiveCamera())
    inter.set_renWin(renWin)
    iren.SetInteractorStyle(inter)

    iren.Initialize()
    iren.Start()

    #for i in range(0, 3600):  # render the image
        # render the image
     #   renWin.Render()
        # rotate the active camera by one degree
      #  renderer.GetActiveCamera().Azimuth(0.1)


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


def graphics_line_placement(tree):

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
    lines_graphic_property.SetColor(color.GetColor3d("Gray"))
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