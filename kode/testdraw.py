import math
import time
import computegraph.operations as operations
import lambdaparser as parser
import randomgraph
import graphicsutils
from computegraph.kkgraph import KKGraph
from computegraph.reductiongraph import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

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

	glTranslatef(0.0, 0.0, -7.0)
	
	testgraph = graphify()
	testgraph.update_layout()
	DrawGraph(testgraph)

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

def DrawGraph(graph):
	# glEnable(GL_LINE_SMOOTH)
	# glEnable(GL_POINT_SMOOTH)
	glPointSize(10.0);
	
	# Draw directed arcs.
	glColor3f(0.2, 0.4, 0.8)
	for node in graph.nodes:
		for edge in node.children:
			far_node = edge.get_far(node)
			if node == far_node:
				print "Circular edge."
				continue
				
			width = 1.1
			if edge.weight > 1:
				width += edge.weight * 0.5
			glLineWidth(width)
			
			x1 = float(node.x)/100
			y1 = float(node.y)/100
			x2 = float(far_node.x)/100
			y2 = float(far_node.y)/100
			
			glBegin(GL_LINES)
			glVertex2f(x1, y1)
			glVertex2f(x2, y2)
			glEnd()
			
			graphicsutils.arrowhead(x1, y1, x2, y2, 0.15, 10)
			# graphicsutils.write((x1-x2)/2, (y1-y2)/2, str(weight), GLUT_BITMAP_HELVETICA_10)

	
	#glColor3f(0.0, 1.0, 0.0)
	#glBegin(GL_POINTS)
	#glVertex2f(0.0, 0.0)
	#glColor3f(0.0, 0.0, 1.0)
	#glVertex2f(1.0, 1.0)
	#glEnd()
	
	# Draw nodes.
	for node in graph.nodes:
		x = float(node.x) / 100
		y = float(node.y) / 100
		
		if node.name == 'N0':
			glColor3f(1.0, 0.0, 0.0)
		else:
			glColor3f(0.0, 0.0, 0.0)
		
		glBegin(GL_POINTS)
		glVertex2f(x, y)
		glEnd()
		
		graphicsutils.write(x-0.05, y-0.1, node.name, GLUT_BITMAP_HELVETICA_12)


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
	glutKeyboardFunc(keyPressed)
	# glutReshapeFunc(ReSizeGLScene)
	# glutFullScreen()
	InitGL(1024, 768)
	glutMainLoop()

# OMEGA: (#x.(x x) #x.(x x))
# OMEGA omega_3: ((#x.(x x) #x.(x x)) #x.((x x) x))
def d():
	draw('#B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))')

#if __name__ == "__main__":
#	d()