import math
import time
from graph import Graph
from graph import Node
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

ESCAPE = '\033'

class TestGraph(Graph):
	
	print "4723947234"

	def __init__ ( self ):
		Graph.__init__(self)
		node1 = Node()
		node2 = Node()
		node3 = Node()
		node4 = Node()
		node5 = Node()
		node6 = Node()
		node7 = Node()
		node1.add_child(node2)
		node2.add_child(node3)
		node3.add_child(node1)
		node2.add_child(node7)
		node7.add_child(node6)
		node7.add_child(node5)
		node2.add_child(node4)
		node4.add_child(node6)
		node5.add_child(node2)
		node6.add_child(node5)
		self.nodes.append(node1)
		self.nodes.append(node2)
		self.nodes.append(node3)
		self.nodes.append(node4)
		self.nodes.append(node5)
		self.nodes.append(node6)
		self.nodes.append(node7)
		
		print "nu8f8rf30"
		
		for node in self.nodes:
			print "nodes"
			for edge in node.children:
				far_node = edge.get_far(node)
				print "edge in node"
				

	# def __render( self ):
	# 	self.__cr.rectangle(0,0,self.__width, self.__height)
	# 	self.__cr.set_source_rgb(1,1,1)
	# 	self.__cr.fill()
	# 
	# 	self.__cr.save()
	# 	self.__cr.set_source_rgb(0,0,0)
	# 	for node in self.nodes:
	# 		for edge in node.children:
	# 			far_node = edge.get_far(node)
	# 			self.__cr.move_to(node.x, node.y)
	# 			self.__cr.line_to(far_node.x, far_node.y)
	# 			self.__cr.stroke()
	# 	self.__cr.restore()
	# 
	# 	self.__cr.save()
	# 	for node in self.nodes:
	# 		self.__cr.arc(node.x, node.y, 5, 0, math.pi*2)
	# 		self.__cr.set_source_rgb(0xcc/255.0, 0, 0)
	# 		self.__cr.fill_preserve()
	# 		self.__cr.set_source_rgb(0xa4/255.0, 0, 0)
	# 		self.__cr.stroke()
	# 	self.__cr.restore()

def update_layout( widget, testgraph ):
	testgraph.update_layout()

def keyPressed(*args):
	# If escape is pressed, kill everything.
    if args[0] == ESCAPE:
	    sys.exit()

def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

def DrawGLScene():
	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()					# Reset The View 

	# Move Left 1.5 units and into the screen 6.0 units.
	glTranslatef(-1.5, 0.0, -6.0)

	# def __render( self ):
	# 	self.__cr.rectangle(0,0,self.__width, self.__height)
	# 	self.__cr.set_source_rgb(1,1,1)
	# 	self.__cr.fill()
	# 
	# 	self.__cr.save()
	# 	self.__cr.set_source_rgb(0,0,0)
	# 	for node in self.nodes:
	# 		for edge in node.children:
	# 			far_node = edge.get_far(node)
	# 			self.__cr.move_to(node.x, node.y)
	# 			self.__cr.line_to(far_node.x, far_node.y)
	# 			self.__cr.stroke()
	# 	self.__cr.restore()
	# 
	# 	self.__cr.save()
	# 	for node in self.nodes:
	# 		self.__cr.arc(node.x, node.y, 5, 0, math.pi*2)
	# 		self.__cr.set_source_rgb(0xcc/255.0, 0, 0)
	# 		self.__cr.fill_preserve()
	# 		self.__cr.set_source_rgb(0xa4/255.0, 0, 0)
	# 		self.__cr.stroke()
	# 	self.__cr.restore()

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

if __name__ == "__main__":

	testgraph = TestGraph()
	
	testgraph.update_layout()
	
	print "ksdlkasdlkasd"
	
	
	global window
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(1024, 768)
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("Graphs")
	glutDisplayFunc(DrawGLScene)
	glutIdleFunc(DrawGLScene)
	glutKeyboardFunc(keyPressed)
	# glutReshapeFunc(ReSizeGLScene)
	# glutKeyboardFunc(keyPressed)
	# InitGL(1024, 768)
	glutMainLoop()

	print "fmoiersmfsmr"