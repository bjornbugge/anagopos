import math
import time
import computegraph.operations as operations
from computegraph.kkgraph import KKGraph
from computegraph.reductiongraph import *
from computegraph.lambda_dag import *
import lambdaparser as parser
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import randomgraph

ESCAPE = '\033'
global term
global graph

def graphify():
	global term
	global graph
	
	if graph is None:
		operations.assignvariables(term)
		g = operations.reductiongraph(term)
	else:
		g = graph
	kkGraph = KKGraph(g)
	print "Drawing: "
	print g
	return kkGraph

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
	
	testgraph = graphify()
	testgraph.update_layout()
	DrawGraph(testgraph)

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

def DrawGraph(graph):
	for node in graph.nodes:
		glPointSize(10.0);
		glColor3f(0.0, 0.0, 0.0)
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		glVertex2f(float(node.x)/100, float(node.y)/100)
		glEnd()
		
	for node in graph.nodes:
		for edge in node.children:
			far_node = edge.get_far(node)
			glLineWidth(2.0)
			# glEnable(GL_LINE_SMOOTH)
			glBegin(GL_LINES)
			glColor3f(0.0, 0.0, 1.0)
			glVertex2f(float(node.x)/100, float(node.y)/100)
			glColor3f(0.0, 1.0, 1.0)
			glVertex2f(float(far_node.x)/100, float(far_node.y)/100)
			glEnd()

def draw(termstr = '', gr = None):
	global graph
	global term
	graph = None
	
	if termstr == '' and gr == None:
		graph = randomgraph.generatereductiongraph()
		while len(graph.nodes) == 0 or len(graph.nodes) > 50: # For now, draw only smaller graphs.
			graph = randomgraph.generatereductiongraph()
	else:
		if gr:
			graph = gr
		else:
			term = parser.parse(termstr)
	
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
	glutKeyboardFunc(keyPressed)
	InitGL(1024, 768)
	glutMainLoop()

if __name__ == "__main__":
	draw()