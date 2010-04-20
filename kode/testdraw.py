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

ESCAPE = '\033'
global term
global graph
def drawtest():
	term = Abstraction()
	term.varname = 'B1'
	t1 = Application()
	term.add(t1)
	t2 = Abstraction()
	t2.varname = 'B2'
	t1.add(t2)
	v1 = Variable('B1')
	# v2 = Variable('B2')
	v2 = Application()
	v2.add(Variable('B2'))
	v2.add(Variable('B2'))
	t1.add(v1)
	t2.add(v2)
	t3 = Application()
	t3.add(term)
	v3 = Variable('B3')
	t3.add(v3)
	operations.assignvariables(t3)
	g = operations.reductiongraph(t3)
	# g er en normal reductiongraph nu.
	print g
	kkGraph = KKGraph(g)
	return kkGraph

def graphify():
	global term
	global graph
	if not graph:
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
	
	# glPointSize(20.0);
	# glColor3f(0.3, 0.5, 1.0)
	# glEnable(GL_POINT_SMOOTH)
	# glBegin(GL_POINTS)
	# # glEnable(GL_POINT_SMOOTH)
	# # glPointSize(2.0);
	# glVertex2f(2.2, 1.8)
	# glEnd()
	
	# testgraph = TestGraph()
	
	testgraph = graphify()
	testgraph.update_layout()
	DrawGraph(testgraph)

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

def DrawGraph(graph):
	for node in graph.nodes:
		glPointSize(5.0);
		glColor3f(0.3, 0.5, 1.0)
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		glVertex2f(float(node.x)/100, float(node.y)/100)
		glEnd()
		
	for node in graph.nodes:
		for edge in node.children:
			far_node = edge.get_far(node)
			glLineWidth(1.0)
			# glEnable(GL_LINE_SMOOTH)
			glBegin(GL_LINES)
			glColor3f(1.0, 0.0, 0.0)
			glVertex2f(float(node.x)/100, float(node.y)/100)
			glVertex2f(float(far_node.x)/100, float(far_node.y)/100)
			glEnd()

# if __name__ == "__main__":
def draw(termstr = '', gr = None):
	global graph
	global term
	
	if termstr == '' and gr == None:
		return
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