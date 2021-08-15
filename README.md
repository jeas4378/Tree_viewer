# Instructions

This is a simple tool made with Python and VTK to view reconciled trees in 3D with the host tree represented as green cones and the reconciled gene tree represented as red cubes. The tool is a simple representation where you can choose between a simple azimuth rotation or a free moving trackballcamera.

In order to use the tool you will have to make sure that Python is installed and that VTK is installed. VTK can be installed using the command

	pip install --upgrade --user vtk
	
on Ubuntu.

After that you run the tool by typing

	python3 tree_viewer.py [host tree] [reconciled gene tree] [OPTIONAL: An integer]
	
If you want a more limited rotation then put in an Integer (for example 45). Using the number 45 will give you a limited rotation of +45 degrees and -45 degrees from the camera starting point. Not inputing a third argument will give you a trackballcamera which provides more rotational options as well as zoom and pans.

If you have inputed a third argument then you can press the key 'i' on the keyboard to get free 360 degree horizontal rotation. Pressing the key 'o' will switch on/off orthographical view.
