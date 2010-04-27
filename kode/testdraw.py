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

global fullScreen
fullScreen = 0

global window_height
window_height = 768

global window_width
window_width = 1024

global window_x
window_x = (glutGet(GLUT_SCREEN_WIDTH) - window_width)/2;

global window_y
window_y = (glutGet(GLUT_SCREEN_HEIGHT) - window_height)/2;

global resizeWindow
resizeWindow = 0

global pointSize
pointSize = 26

global pointX
global pointY


def graphify():
	global term
	global graph
	
	if graph is None:
		operations.assignvariables(term)
		g = operations.reductiongraph(term, 40)
	else:
		g = graph
	
	kkGraph = KKGraph(g, 800, 500)
	print "Drawing graph with " + str(len(g.nodes)) + " nodes."
	return kkGraph

def keyPressed(*args):
	
	global resizeWindow
	global window_x
	global window_y
	
	if args[0] == ESCAPE:
	    sys.exit()
	elif args[0] == 'u':
		global kkgraph
		kkgraph = graphify()
		resizeWindow = 0
		DrawGLScene()
	elif args[0] == 'f':
		global fullScreen
		global window_height
		global window_width
		if fullScreen == 0:
			resizeWindow = 0
			window_width = glutGet(GLUT_WINDOW_WIDTH)
			window_height = glutGet(GLUT_WINDOW_HEIGHT)
			window_x = glutGet(GLUT_WINDOW_X)
			window_y = glutGet(GLUT_WINDOW_Y)
			glutFullScreen()
			fullScreen = 1
		else:
			glutReshapeWindow(window_width,window_height)
			glutPositionWindow(window_x,window_y)
			fullScreen = 0
			
def InitGL(Width, Height):
	# Set 2D-mode
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0, Width, 0, Height)
	glScalef(1, -1, 1)
	glTranslatef(0, -Height, 0)
	glMatrixMode(GL_MODELVIEW)
	
	glClearColor(1.0, 1.0, 1.0, 0.0)	# This Will Clear The Background Color To White
	# glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	glDisable(GL_DEPTH_TEST)			# Disables Depth Testing
	# glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
	glutMouseFunc(processMouse)
	
	# Anti-aliasing/prettyness stuff
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
	glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
	glEnable(GL_LINE_SMOOTH)
	glEnable(GL_POINT_SMOOTH)
	glEnable(GL_POLYGON_SMOOTH)
	
	global kkgraph
	kkgraph = graphify()
	
	global pointSize
	glPointSize(pointSize)

def DrawGLScene():
	global resizeWindow
	global kkgraph
	if resizeWindow == 0:
		kkgraph.update_layout_animated(DrawGraph)
		resizeWindow = 1
	else:
		DrawGraph(kkgraph)

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	# glutSwapBuffers()

def DrawGraph(graph):
	global pointSize
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLineWidth(1.5)
	
	# Draw directed arcs.
	for node in graph.nodes:
		for edge in node.children:
			far_node = edge.get_far(node)
			if node == far_node:
				print "Circular edge."
				continue
				
			# width = 1.1
#			if edge.weight > 1:
#				width += edge.weight * 0.5
#			glLineWidth(width)
			
			x1 = float(node.x)		#/100
			y1 = float(node.y)		#/100
			x2 = float(far_node.x)	#/100
			y2 = float(far_node.y)	#/100
			
			glColor3f(0.2, 0.4, 0.8)
			glBegin(GL_LINES)
			glVertex2f(x1, y1)
			glVertex2f(x2, y2)
			glEnd()
			
			glColor3f(0.1, 0.3, 0.7)
			graphicsutils.arrowhead(x1, y1, x2, y2, pointSize / 2, 20, 12)
	
	glColor3f(0.7, 0.7, 0.7)
	graphicsutils.write(0.0, 0.0, "(0,0)")
	graphicsutils.write(100, 10, "(100,10)")
	graphicsutils.write(100, 100, "(100,100)")
	graphicsutils.write(200, 100, "(200,100)")
	graphicsutils.write(500, 500, "(500,500)")
	
	i = 0
	for node in graph.nodes:		
		i = i + 1
	
		
	global pointArray
	# pointArray[7][1]
	
	pointArray = [[0 for col in range(3)] for row in range(i)]
	
	j = 0
	
	# Draw nodes.
	for node in graph.nodes:
		x = float(node.x) #/ 100
		y = float(node.y) #/ 100

		if node.name == 'N0':
			glColor3f(1.0, 0.0, 0.0)
		else:
			glColor3f(0.0, 0.0, 0.0)
		
		glBegin(GL_POINTS)
		glVertex2f(x, y)
		glEnd()
		
		global pointArray
		pointArray[j][0] = x
		pointArray[j][1] = y
		pointArray[j][2] = node.term
		j = j + 1
		
		global pointX
		pointX = x
		
		global pointY
		pointY = y
				
		graphicsutils.write(x, y+pointSize, node.name, GLUT_BITMAP_HELVETICA_12)
	
	glutSwapBuffers()

def processMouse(button, state, x, y):
	
	global pointX
	global pointY
	# print "Point X: " + str(pointX)
	# print "Point Y: " + str(pointY)
	
	pointylow = pointY-10
	pointyhigh = pointY+10
	pointxlow = pointX-10
	pointxhigh = pointX+10
	
	global pointArray
	# print "Point Array:"
	# print pointArray
	
	for k in range(len(pointArray)):
		# print "Point " + str(k) + " - X: " + str(pointArray[k][0]) + " Y: " + str(pointArray[k][1])
		pointX = pointArray[k][0]
		pointY = pointArray[k][1]
		pointName = pointArray[k][2]
		
		pointylow = pointY-10
		pointyhigh = pointY+10
		pointxlow = pointX-10
		pointxhigh = pointX+10
		
		if state == GLUT_UP:
			if button == GLUT_LEFT_BUTTON:
				if x>pointxlow and x<pointxhigh and y>pointylow and y<pointyhigh:
					# print "you selected point: " + str(pointArray[k][2])
					print "X: " + str(x)
					print "Y: " + str(y)
					lambdaTerm = str(pointArray[k][2])
					print "Lambda Term: " + lambdaTerm
					graphicsutils.write(x, y, lambdaTerm)
					glutSwapBuffers()


	# for x in pointArray:
	# 	print x
	# 	print pointArray[x]
	
	# State
	# if state == GLUT_UP:
	# 	if button == GLUT_LEFT_BUTTON:
	# 		if x>pointxlow and x<pointxhigh and y>pointylow and y<pointyhigh:
	# 			print "you hit the point"
	# 		print "LEFT - X: " + str(x) + " Y: " + str(y)
	# 	elif button == GLUT_RIGHT_BUTTON:
	# 		print "RIGHT: - X: " + str(x) + " Y: " + str(y)
	# 	else:
	# 		print "MIDDLE: - X: " + str(x) + " Y: " + str(y)
	

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

	global window_height
	global window_width
	
	global window_x
	global window_y
	
	global resizeWindow
	resizeWindow = 0
	
	glutInitWindowSize(1024, 768)
	glutInitWindowPosition(window_x,window_y)
	window = glutCreateWindow("Graphs")
	glutDisplayFunc(DrawGLScene)
	glutKeyboardFunc(keyPressed)
	# glutReshapeFunc(ReSizeGLScene)
	# glutFullScreen()
	InitGL(1024, 768)
	glutMainLoop()

# OMEGA: (#x.(x x) #x.(x x))
# OMEGA omega_3: (#x.(x x) (#x.(x x) #x.((x x) x)))
# omega_3 omega_3: (#x.((x x) x) #y.((y y) y))
def d():
	# draw()
	draw('#B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))')
	# draw('(#x.(x x) #x.(x x))') # OMEGA

if __name__ == "__main__":
	d()