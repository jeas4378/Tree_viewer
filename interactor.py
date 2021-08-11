import math

import vtk

class Interactor(vtk.vtkInteractorStyleUser):

    """
    A custom Interactor-class which limits interaction to rotation only.
    """

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
        self.AddObserver("KeyPressEvent", self.keypress)
        self.camera = None
        self.within_parallell = within_parallel
        self.last_picked_actor = None
        self.last_picked_property = vtk.vtkProperty()
        self.renderer = None
        self.colors = vtk.vtkNamedColors()
        self.color = color
        self.limit_rotation = True
        self.current_pitch = 0
        self.pitch_min = 0
        self.pitch_max = 90
        self.rotation_speed = 59

    def left_button_press(self, obj, event):
        """
        A method that runs when you click your left mouse button.

        :param obj: An object.
        :param event: An event.
        :return: Nothing.
        """

        # When clicking on the left mouse button this value is set to one which impacts under the method
        # 'mouse_event'.
        self.boolRotate = 1

        # Get the position in the window where the user clicked.
        clickPos = self.iren.GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.get_renderer())

        # Gets the new actor that might have been clicked.
        self.NewPickedActor = picker.GetActor()

        # If the user clicked on an actor.
        if self.NewPickedActor:
            # If there is a previous clicked object we restore it's property.
            if self.last_picked_actor:
                self.last_picked_actor.GetProperty().DeepCopy(self.last_picked_property)

            # Save away the current property so we can restore it later.
            self.last_picked_property.DeepCopy(self.NewPickedActor.GetProperty())
            # The clicked actor gets it's property changed.
            self.NewPickedActor.GetProperty().SetColor(self.colors.GetColor3d(self.color))
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
            self.NewPickedActor.GetProperty().EdgeVisibilityOn()

            # Save away the current actor being clicked.
            self.last_picked_actor = self.NewPickedActor
        self.get_renWin().Render()
        return

    def left_button_release(self, obj, event):
        """
        Dictates what should happen when the left mouse button is released.

        Changes the boolean value so that nothing happens when you move the mouse over the screen.

        :param obj: An object.
        :param event: An event.
        :return: Nothing.
        """
        self.boolRotate = 0
        return

    def mouse_event(self, obj, event):
        """
        The method that dictates what happens when the mouse moves over the Render Window.

        If the left mouse button is pressed the graphical representation will rotate if the parameters are met.

        :param obj: An object.
        :param event: An event.
        :return: Nothing.
        """

        # Get the previous position of the mouse cursor.
        last_xy_pos = self.iren.GetLastEventPosition()
        last_x = last_xy_pos[0]
        last_y = last_xy_pos[1]

        # Get the current position of the mouse cursor.
        xy_pos = self.iren.GetEventPosition()
        x = xy_pos[0]
        y = xy_pos[1]

        # If the left mouse button is clicked.
        if self.get_boolRotate():
            #self.camera_pitch(y, last_y)
            # If there is a limit on how much the tree can be rotated.
            if self.is_in_valid_range(x, last_x) and self.get_limit_rotation():
                self.rotate(x, last_x)
            else:
                self.rotate(x, last_x)

    def rotate(self, x, last_x):
        """
        The method that actually rotates the Camera.

        :param x: A numerical value containing the current x-position of the mouse cursor.
        :param last_x: A numerical value containing the previous x-position of the mouse cursor.
        :return: Nothing.
        """

        # Calculates if there should be a positive or negative rotation.
        rotate_diff = last_x - x
        current = self.get_current_rotate()
        max_rotate = self.get_max_rotate()
        min_rotate = self.get_min_rotate()

        # If there is a rotation limit then we calculate how much the graphical representation is allowed to rotate.
        if self.get_limit_rotation():
            if (current + rotate_diff) > max_rotate:
                clamp = (current + rotate_diff) - max_rotate
                rotate_diff -= clamp
            elif (current + rotate_diff) < min_rotate:
                clamp = (current + rotate_diff) - min_rotate
                rotate_diff -= clamp

        rotate_diff /= self.rotation_speed
        # The actual rotation process.
        if abs(rotate_diff) > 0:
            position = self.get_camera().GetPosition()
            camera_position = []
            for pos in position:
                camera_position.append(pos)
            new_position = self.matrix_rotation(camera_position, [0, rotate_diff, 0])
            self.get_camera().SetPosition(new_position[0], new_position[1], new_position[2])
            #self.get_camera().Azimuth(rotate_diff)
            self.set_current_rotate(rotate_diff)
            self.get_camera().OrthogonalizeViewUp()

            # Re-render the viewport.
            self.get_renWin().Render()

    def camera_pitch(self, y, last_y):
        rotate_diff = last_y - y
        current = self.get_current_pitch()
        max_pitch = self.get_pitch_max()
        min_pitch = self.get_pitch_min()

        # If there is a rotation limit then we calculate how much the graphical representation is allowed to rotate.
        if (current + rotate_diff) > max_pitch:
            clamp = (current + rotate_diff) - max_pitch
            rotate_diff -= clamp
        elif (current + rotate_diff) < min_pitch:
            clamp = (current + rotate_diff) - min_pitch
            rotate_diff -= clamp

        # The actual rotation process.
        self.get_camera().Elevation(rotate_diff)
        self.set_current_pitch(rotate_diff)
        # self.get_camera().OrthogonalizeViewUp()

    def matrix_rotation(self, point, rotation):

        rot_x = rotation[0]
        rot_y = rotation[1]
        rot_z = rotation[2]

        transformed_point = [0, 0, 0]

        rotation_matrix = [[], [], []]
        theta = 0

        if rot_x == 0 and rot_y == 0:
            theta = rot_z
            # Rotation matrix represented with each row representing each matrix row.
            rotation_matrix = [[math.cos(theta), -math.sin(theta), 0],
                               [math.sin(theta), math.cos(theta), 0],
                               0, 0, 1]
        elif rot_x == 0 and rot_z == 0:
            theta = rot_y
            rotation_matrix = [[math.cos(theta), 0 , math.sin(theta)],
                               [0, 1, 0],
                               [-math.sin(theta), 0, math.cos(theta)]]
        elif rot_y == 0 and rot_z == 0:
            theta = rot_x
            rotation_matrix = [[1, 0 , 0],
                               [0, math.cos(theta), -math.sin(theta)],
                               [0, math.sin(theta), math.cos(theta)]]
        else:
            return [0, 0, 0]

        # The transformation of the point where the point is a column vector.

        for i in range(len(rotation_matrix)):
            transformed_point[i] = (rotation_matrix[i][0]*point[0] + rotation_matrix[i][1]*point[1] + rotation_matrix[i][2]*point[2])

        return transformed_point


    def get_current_rotate(self):
        """
        Get the current rotation of the camera in reference from the starting position which has the value 0.

        :return: A numerical value.
        """
        return self.current_rotate

    def get_min_rotate(self):
        """
        Get the minimum rotational value allowed. A value of -45 means that you can at most rotate a -45 degrees from
        the starting position which has the value 0.

        :return: A numerical value.
        """
        return self.min_rotate

    def get_max_rotate(self):
        """
        Get the maximal rotational value allowed. A value of 45 means that you can at most rotate 45 degrees from the
        starting position which has the value of 0.

        :return: A numerical value.
        """
        return self.max_rotate

    def set_current_rotate(self, x):
        """
        Adds the rotation to the current value.

        :param x: A numerical value.
        :return: Nothing.
        """
        self.current_rotate += (x * self.rotation_speed)

    def get_camera(self):
        """
        Gets the vtkCamera-object associated with this instance of this class.

        :return: A vtkCamera-object.
        """
        return self.camera

    def get_renWin(self):
        """
        Gets the vtkRenderWindow-object associated with the instance of this class.

        :return: A vtkRenderWindow-object.
        """
        return self.renWin

    def set_renWin(self, renWin):
        """
        Sets a vtkRenderWindow-object to an instance of this class.

        :param renWin: A vtkRenderWindow-object.
        :return: Nothing.
        """
        self.renWin = renWin

    def set_camera(self, camera):
        """
        Sets a vtkCamera-object to an instance of this class.

        :param camera: a vtkCamera-object.
        :return: Nothing.
        """
        self.camera = camera

    def set_iren(self, iren):
        """
        Sets a vtkRenderWindowInteractor-object to an instance of this class.

        :param iren: A vtkRenderWindowInteractor-object.
        :return: Nothing.
        """
        self.iren = iren

    def get_boolRotate(self):
        """
        Gets the value of the variable 'boolRotate'.

        :return: An integer of either 0 or 1.
        """
        return self.boolRotate

    def get_within_parallell(self):
        """
        Gets the value of the variable 'within_parallell'.

        :return: A numerical value.
        """
        return self.within_parallell

    def set_renderer(self, renderer):
        """
        Sets a vtkRender-object to be associcated with this instance of the class.

        :param renderer: A vtkRenderer-object.
        :return: Nothing.
        """
        self.renderer = renderer

    def get_renderer(self):
        """
        Returns the vktRenderer-object associated with the instance of this class.

        :return: A vtkRenderer-object.
        """
        return self.renderer

    def set_limit_rotation(self, val):
        """
        Sets if the rotation should be limited or not.

        :param val: A boolean value of 'True' or 'False'.
        :return: Nothing.
        """
        self.limit_rotation = val

    def get_limit_rotation(self):
        """
        Returns if rotation is limited or not.

        :return: A boolean value of 'True' or 'False'.
        """
        return self.limit_rotation

    def get_current_pitch(self):
        """
        Returns the current pitch-angle of the camera object.

        :return: A numerical value.
        """
        return self.current_pitch

    def set_current_pitch(self, y):
        """
        Adjust the current pitch of the camera.

        :param y: A numerical value.
        :return: Nothing.
        """
        self.current_pitch += y

    def get_pitch_min(self):
        """
        Returns the minimum allowed angle for the pitch of the camera.

        :return: A numerical value.
        """
        return self.pitch_min

    def get_pitch_max(self):
        """
        Returns the maximum allowed angle for the pitch of the camera.

        :return: A numerical value.
        """
        return self.pitch_max

    def set_ortographic(self):
        """
        A method that turns on or off orthographical camera projection.

        :return: Nothing.
        """
        if self.get_camera().GetParallelProjection():
            self.get_camera().SetParallelProjection(0)
        else:
            self.get_camera().SetParallelProjection(1)

    def is_in_valid_range(self, x, last_x):
        """
        A method that check if the current rotation is within the designated threshold for allowed rotation.

        :param x: The current x-position of the mouse cursor.
        :param last_x: The previous position of the mouse cursor.
        :return: A boolean value of 'True' or 'False'.
        """
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
        """
        A method that checks if the rotation has passed the point of which orthographical projection should be
        turned on.

        :return: A boolean value of 'True' or 'False'.
        """
        if abs(self.get_current_rotate()) >= self.get_within_parallell():
            return True
        else:
            return False

    def keypress(self, obj, event):
        """
        A method that listens after keypresses.

        When specific keys are pressed different operations will be performed.

        :param obj: An object.
        :param event: An event.
        :return: Nothing.
        """
        key = obj.GetKeySym()

        if key == "i":
            val = False if self.get_limit_rotation() else True
            self.set_limit_rotation(val)

        if key == "o":
            self.set_ortographic()

        self.get_renWin().Render()
