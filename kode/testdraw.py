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
		print "assigning vars"
		operations.assignvariables(term)
		g = operations.reductiongraph(term)
	else:
		g = graph
	
	kkGraph = KKGraph(g, 400, 400)
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
	glColor3f(1.0, 0.0, 0.0)
	for node in graph.nodes:
		x = float(node.x)/100
		y = float(node.y)/100
		glPointSize(10.0);
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		glVertex2f(x, y)
		glEnd()
		glColor3f(0.0, 0.0, 0.0)
		# glColor3f(1.0, 0.0, 0.0)
		# graphicsutils.drawtext(x, y, node.name)
		
	for node in graph.nodes:
		for edge in node.children:
			
			far_node = edge.get_far(node)
			
			X2 = float(far_node.x)/100
			Y2 = float(far_node.y)/100
			X1 = float(node.x)/100
			Y1 = float(node.y)/100
			
			glLineWidth(2.0)
			glBegin(GL_LINES)
			glColor3f(0.3, 0.2, 0.6)
			glVertex2f(X1, Y1)
			glVertex2f(X2, Y2)
			glEnd()
			
			Pi = math.pi
			ArrowHeadLength1 = 0.13
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

if __name__ == "__main__":
	draw("#B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))")