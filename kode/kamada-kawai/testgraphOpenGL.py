import math
import time
from graph import Graph
from graph import Node
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

ESCAPE = '\033'

class TestGraph(Graph):
	
	print "Press ESC to exit"

	def __init__ ( self ):
		Graph.__init__(self)
		# node1 = Node()
		# node2 = Node()
		# node1.add_child(node2)
		# self.nodes.append(node1)
		# self.nodes.append(node2)
		node1 = Node()
		node2 = Node()
		node3 = Node()
		node4 = Node()
		node5 = Node()
		node6 = Node()
		node7 = Node()
		node8 = Node()
		node9 = Node()
		node1.add_child(node2)
		node2.add_child(node3)
		node3.add_child(node1)
		node2.add_child(node7)
		node7.add_child(node6)
		node7.add_child(node5)
		node7.add_child(node8)
		node7.add_child(node9)
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
		self.nodes.append(node8)
		self.nodes.append(node9)

		print "nu8f8rf30"

	# def __render( self ):
	# 	
	# 	# glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	# 	# glLoadIdentity()					# Reset The View 
    #     # 
	# 	# # Move Left 1.5 units and into the screen 6.0 units.
	# 	# glTranslatef(-1.5, 0.0, -6.0)
	# 	
	# 	for node in self.nodes:
	# 		for edge in node.children:
	# 			far_node = edge.get_far(node)
	# 			glLineWidth(5.0)
	# 			glBegin(GL_LINES)
	# 			glVertex2f(node.x, node.y)
	# 			glColor3f(1.0, 0.0, 0.0)
	# 			glVertex2f(far_node.x, far_node.y)
	# 			glEnd()
    # 
	# 	for node in self.nodes:
	# 		print "Node x: "
	# 		print node.x
	# 		print "Node y: "
	# 		print node.y
	# 		glPointSize(20.0);
	# 		glColor3f(0.3, 0.5, 1.0)
	# 		glEnable(GL_POINT_SMOOTH)
	# 		glBegin(GL_POINTS)
	# 		glVertex2f(node.x, node.y)
	# 		glEnd()
		
			# self.__cr.rectangle(0,0,self.__width, self.__height)
			# self.__cr.set_source_rgb(1,1,1)
			# self.__cr.fill()
			# 
			# self.__cr.save()
			# self.__cr.set_source_rgb(0,0,0)
			# for node in self.nodes:
			# 	for edge in node.children:
			# 		far_node = edge.get_far(node)
			# 		self.__cr.move_to(node.x, node.y)
			# 		self.__cr.line_to(far_node.x, far_node.y)
			# 		self.__cr.stroke()
			# self.__cr.restore()
			# 
			# self.__cr.save()
			# for node in self.nodes:
			# 	self.__cr.arc(node.x, node.y, 5, 0, math.pi*2)
			# 	self.__cr.set_source_rgb(0xcc/255.0, 0, 0)
			# 	self.__cr.fill_preserve()
			# 	self.__cr.set_source_rgb(0xa4/255.0, 0, 0)
			# 	self.__cr.stroke()
			# self.__cr.restore()

def update_layout( widget, testgraph ):
	testgraph.update_layout()

def keyPressed(*args):
	# If escape is pressed, kill everything.
    if args[0] == ESCAPE:
	    sys.exit()

def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    glClearColor(1.0, 1.0, 1.0, 0.0)	# This Will Clear The Background Color To Black
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
	
	# glPointSize(20.0);
	# glColor3f(0.3, 0.5, 1.0)
	# glEnable(GL_POINT_SMOOTH)
	# glBegin(GL_POINTS)
	# # glEnable(GL_POINT_SMOOTH)
	# # glPointSize(2.0);
	# glVertex2f(2.2, 1.8)
	# glEnd()
	
	testgraph = TestGraph()
	testgraph.update_layout()
	DrawGraph(testgraph)

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

def DrawGraph(graph):
	
	# glColor3f(1.0, 0.0, 0.0)
	# glBegin(GL_TRIANGLES);
	# glVertex2f(2.1, 3.1);
	# glVertex2f(1.2, 2.2);
	# glVertex2f(3.3, 1.3);
	# glEnd();
	
	for node in graph.nodes:
		print "Node x: "
		print node.x/100
		print node.x
		print "Node y: "
		print float(node.y)/100
		print float(node.y)
		glPointSize(10.0);
		glColor3f(0.0, 0.0, 0.0)
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		glVertex2f(float(node.x)/100, float(node.y)/100)
		glEnd()
		
	for node in graph.nodes:
		for edge in node.children:
			far_node = edge.get_far(node)
			# Arrow (triangle)
			# glColor3f(1.0, 0.0, 0.0)
			# glBegin(GL_TRIANGLES);
			# glVertex2f(float(far_node.x)/100, float(far_node.y)/100);
			# glVertex2f(((float(node.y)/100)), ((float(far_node.y)/100)));
			# glVertex2f(((float(far_node.x)/100)), ((float(node.x)/100)));
			# glEnd();
			# glPointSize(5.0);
			# glColor3f(0.3, 0.5, 0.1)
			# glEnable(GL_POINT_SMOOTH)
			# glBegin(GL_POINTS)
			# if node.x < far_node.x:
			# 	print "1"
			# 	px = (float(node.x)/100)+0.03
			# else:
			# 	print "2"
			# 	px = (float(node.x)/100)-0.03
			# if node.y > far_node.y:
			# 	print "3"
			# 	py = (float(node.y)/100)-0.03
			# else:
			# 	print "4"
			# 	py = (float(node.y)/100)+0.03
            # 
			# glVertex2f(px, py)

			# glEnd()
			# Line
			glLineWidth(2.0)
			# glEnable(GL_LINE_SMOOTH)
			# print "line vector is " + str(float(far_node.x)/100-float(node.x)/100) + "/" + str(float(far_node.y)/100-float(node.y)/100)
			
			X2 = float(far_node.x)/100
			Y2 = float(far_node.y)/100
			X1 = float(node.x)/100
			Y1 = float(node.y)/100
			
			hx = float(far_node.x)/100-float(node.x)/100
			hy = float(far_node.y)/100-float(node.y)/100
			print "Haeldning X: " + str(hx)
			print "Haeldning Y: " + str(hy)
			
			glBegin(GL_LINES)
			glColor3f(0.0, 0.0, 1.0)
			glVertex2f(X1, Y1)
			glColor3f(0.0, 0.0, 1.0)
			glVertex2f(X2, Y2)
			glEnd()
			
			Pi = math.pi
			ArrowHeadLength1 = 0.1
			ArrowHeadLength2 = 0.1
			
			LineAngle = math.atan((Y2-Y1)/(X2-X1))
			
			EndAngle1 = LineAngle + 10 * Pi/180
			EndAngle2 = LineAngle - 10 * Pi/180
			
			if X1 < X2:
				if Y1 < Y2:
					Y3 = Y2 - ArrowHeadLength1 * math.sin(EndAngle1)
					Y4 = Y2 - ArrowHeadLength1 * math.sin(EndAngle2)
					X3 = X2 - ArrowHeadLength1 * math.cos(EndAngle1)
					X4 = X2 - ArrowHeadLength1 * math.cos(EndAngle2)
				else:
					Y3 = Y2 - ArrowHeadLength1 * math.sin(EndAngle1)
					Y4 = Y2 - ArrowHeadLength1 * math.sin(EndAngle2)
					X3 = X2 - ArrowHeadLength1 * math.cos(EndAngle1)
					X4 = X2 - ArrowHeadLength1 * math.cos(EndAngle2)
			else:
				if Y1 < Y2:
					Y3 = Y2 + ArrowHeadLength1 * math.sin(EndAngle1)
					Y4 = Y2 + ArrowHeadLength1 * math.sin(EndAngle2)
					X3 = X2 + ArrowHeadLength1 * math.cos(EndAngle1)
					X4 = X2 + ArrowHeadLength1 * math.cos(EndAngle2)
				else:
					Y3 = Y2 + ArrowHeadLength1 * math.sin(EndAngle1)
					Y4 = Y2 + ArrowHeadLength1 * math.sin(EndAngle2)
					X3 = X2 + ArrowHeadLength1 * math.cos(EndAngle1)
					X4 = X2 + ArrowHeadLength1 * math.cos(EndAngle2)
			
			glBegin(GL_TRIANGLES);
			glVertex2f(X2,Y2);
			glVertex2f(X3,Y3);
			glVertex2f(X4,Y4);
			glEnd();
			
			# print "1"
			# glBegin(GL_LINES)
			# glColor3f(0.3, 0.3, 0.3)
			# glVertex2f(float(node.x)/100, float(far_node.y)/100)
			# glColor3f(0.1, 1.0, 0.8)
			# glVertex2f((float(node.x)/100)+hy, (float(far_node.y)/100)-hx)
			# glEnd()
			# print "2" 

if __name__ == "__main__":
	
	print "ksdlkasdlkasd"
	
	
	global window
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(1024, 768)
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("Graphs")
	glutDisplayFunc(DrawGLScene)
	# glutIdleFunc(DrawGLScene)
	glutKeyboardFunc(keyPressed)
	# glutReshapeFunc(ReSizeGLScene)
	# glutKeyboardFunc(keyPressed)
	InitGL(1024, 768)
	glutMainLoop()

	print "fmoiersmfsmr"