import math
import time
import computegraph.operations as operations
from computegraph.kkgraph import KKGraph
from computegraph.reductiongraph import *
# from computegraph.lambda_dag import *
# import computegraph.lambda_dag as lambda_dag
import lambdaparser as parser
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import randomgraph
import graphicsutils

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
	
	kkGraph = KKGraph(g, 300, 300)
	print "Drawing: "
	print g
	return kkGraph

def keyPressed(*args):
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
	    sys.exit()
	elif args[0] == 'u':
		DrawGLScene()

def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	glClearColor(1.0, 1.0, 1.0, 0.0)	# This Will Clear The Background Color To White
	glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	# glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
	glDisable(GL_DEPTH_TEST)			# Disables Depth Testing
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
	glTranslatef(-1.5, -1.0, -6.0)
	# glTranslatef(0.0, 0.0, 0.0)
	
	testgraph = graphify()
	testgraph.update_layout()
	DrawGraph(testgraph)

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

def DrawGraph(graph):
	# glEnable(GL_LINE_SMOOTH)
	glEnable(GL_POINT_SMOOTH)
	glLineWidth(1.1)
	glPointSize(10.0);
	
	# Draw directed arcs.
	glColor3f(0.0, 0.2, 0.6)
	for node in graph.nodes:
		for edge in node.children:			
			far_node = edge.get_far(node)
			
			x1 = float(node.x)/100
			y1 = float(node.y)/100
			x2 = float(far_node.x)/100
			y2 = float(far_node.y)/100
			
			glBegin(GL_LINES)
			glVertex2f(x1, y1)
			glVertex2f(x2, y2)
			glEnd()
			
			graphicsutils.arrowhead(x1, y1, x2, y2, 0.15, 10)
	
	# Draw nodes.
	for node in graph.nodes:
		x = float(node.x)/100
		y = float(node.y)/100
		
		print "("+str(x)+", "+str(y)+")"
		
		glBegin(GL_POINTS)
		glVertex2f(x, y)
		glEnd()
		
		glColor3f(0.0, 0.0, 0.0)
		graphicsutils.write(x-0.05, y-0.1, node.name)


def draw(termstr = '', gr = None):
	global graph
	global term
	graph = None
	term = ''
	if not termstr == '':
		term = parser.parse(termstr)
	elif not gr == None:
		graph = gr
	else:
		graph = randomgraph.generatereductiongraph()
		while len(graph.nodes) == 0 or len(graph.nodes) > 50: # For now, draw only smaller graphs.
			graph = randomgraph.generatereductiongraph()
	
	print term
	
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
	# glutFullScreen()
	glutKeyboardFunc(keyPressed)
	InitGL(1024, 768)
	glutMainLoop()

def d():
	draw('#B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))')

#if __name__ == "__main__":
#	d()