import vtk

class Interactor(vtk.vtkInteractorStyleUser):

    def __init__(self, color="Blue", within_parallel=45, parent=None):
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
        self.within_parallell = within_parallel
        self.last_picked_actor = None
        self.last_picked_property = vtk.vtkProperty()
        self.renderer = None
        self.colors = vtk.vtkNamedColors()
        self.color = color

    def left_button_press(self, obj, event):
        self.boolRotate = 1

        clickPos = self.iren.GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.get_renderer())

        # get the new
        self.NewPickedActor = picker.GetActor()

        # If something was selected
        if self.NewPickedActor:
            # If we picked something before, reset its property
            if self.last_picked_actor:
                self.last_picked_actor.GetProperty().DeepCopy(self.last_picked_property)

            # Save the property of the picked actor so that we can
            # restore it next time
            self.last_picked_property.DeepCopy(self.NewPickedActor.GetProperty())
            # Highlight the picked actor by changing its properties
            self.NewPickedActor.GetProperty().SetColor(self.colors.GetColor3d(self.color))
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
            self.NewPickedActor.GetProperty().EdgeVisibilityOn()

            # save the last picked actor
            self.last_picked_actor = self.NewPickedActor
        self.get_renWin().Render()
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
        current = self.get_current_rotate()
        max = self.get_max_rotate()
        min = self.get_min_rotate()

        if (current + rotate_diff) > max:
            clamp = (current + rotate_diff) - max
            rotate_diff -= clamp
        elif (current + rotate_diff) < min:
            clamp = (current + rotate_diff) - min
            rotate_diff -= clamp

        self.get_camera().Azimuth(rotate_diff)
        self.set_current_rotate(rotate_diff)
        self.get_camera().OrthogonalizeViewUp()
        if self.is_within_parallell():
            self.get_camera().SetParallelProjection(1)
        else:
            self.get_camera().SetParallelProjection(0)
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

    def get_within_parallell(self):
        return self.within_parallell

    def set_renderer(self, renderer):
        self.renderer = renderer

    def get_renderer(self):
        return self.renderer

    def is_in_valid_range(self, x, last_x):
        diff = last_x - x
        if self.get_max_rotate() >= self.get_current_rotate() >= self.get_min_rotate():
            return True
        else:
            if self.get_current_rotate() >= self.get_max_rotate() and diff < 0:
                return True
            elif self.get_current_rotate() <= self.get_min_rotate() and diff > 0:
                return True
            else:
                return False

    def is_within_parallell(self):
        if abs(self.get_current_rotate()) >= self.get_within_parallell():
            return True
        else:
            return False