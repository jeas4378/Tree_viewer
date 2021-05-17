# Instructions

This is a simple tool made with Python and VTK to view reconciled trees in 3D with the host tree represented as green cones and the reconciled gene tree represented as red cubes. The tool is a simple representation with limited camera movement. The only camera movement allowed is a 90 degree rotation around the tree.

In order to use the tool you will have to make sure that Python is installed and that VTK is installed. VTK can be installed using the command

	pip install --upgrade --user vtk

After that you run the tool by typing

	python3 [host tree] [reconciled gene tree] [OPTIONAL: An integer]
	
The optional argument determines at what angle the view will become ortographical. '45' will mean that the ortograhical view only activate at the maximum positive or negative rotation. A value >45 means that the ortographical view is disabled and a value of <=0 means that the ortographical view is always activated.
