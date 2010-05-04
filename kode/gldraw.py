import math
import time
import random
import computegraph.operations as operations
import lambdaparser as parser
import randomgraph
import graphicsutils
import testdraw
from computegraph.kkgraph import KKGraph
from computegraph.reductiongraph import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


class GlDraw(object):
	def __init__(self):
		self.term = None
		self.graph = None
		self.node = None
		self.fullScreen = 0
		self.dirty = None
		self.window_height = 768
		self.window_width = 1024
		self.window_x = (glutGet(GLUT_SCREEN_WIDTH) - self.window_width)/2
		self.window_y = (glutGet(GLUT_SCREEN_HEIGHT) - self.window_height)/2
		self.resizeWindow = 0
		self.pointSize = (((self.window_height + self.window_width)/2)/50)
		self.pointX = None
		self.pointY = None
		self.pointArray = None
		self.InitGL(1024, 768)
		
	def InitGL(self, Width, Height):
		
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		
		self.resizeWindow = 0
		
		glutInitWindowSize(1024, 768)
		glutInitWindowPosition(self.window_x,self.window_y)
		window = glutCreateWindow("Graphs")
		glutDisplayFunc(self.DrawGLScene)
		glutKeyboardFunc(self.keyPressed)
		
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
		glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
    
		glutMouseFunc(self.processMouse)
    
		# Anti-aliasing/prettyness stuff
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)
		glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
		glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
		glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
		glEnable(GL_LINE_SMOOTH)
		glEnable(GL_POINT_SMOOTH)
		glEnable(GL_POLYGON_SMOOTH)
		
		glPointSize(self.pointSize)
	
	def keyPressed(self, *args):
		if args[0] == '\033':
		    sys.exit()
		elif args[0] == 'u':
			self.pointSize = (((glutGet(GLUT_WINDOW_HEIGHT) + glutGet(GLUT_WINDOW_WIDTH))/2)/50)
			k = 0
			for node in self.graph.nodes:
				node.x = random.randint(1, self.window_width)
				node.y = random.randint(1, self.window_height)
				self.pointArray[k][3] = 0
				k = k + 1
			self.graph.update_layout_animated(self.DrawGraph)
			self.resizeWindow = 0
			self.DrawGLScene()
			glutSwapBuffers()
		elif args[0] == 'f':
			self.pointSize = (((glutGet(GLUT_WINDOW_HEIGHT) + glutGet(GLUT_WINDOW_WIDTH))/2)/50)
			if self.fullScreen == 0:
				self.resizeWindow = 0
				self.window_width = glutGet(GLUT_WINDOW_WIDTH)
				self.window_height = glutGet(GLUT_WINDOW_HEIGHT)
				self.window_x = glutGet(GLUT_WINDOW_X)
				self.window_y = glutGet(GLUT_WINDOW_Y)
				glutFullScreen()
				self.fullScreen = 1
			else:
				glutReshapeWindow(self.window_width,self.window_height)
				glutPositionWindow(self.window_x,self.window_y)
				self.fullScreen = 0


	def DrawGLScene(self):
		if self.resizeWindow == 0:
			self.graph.update_layout_animated(self.DrawGraph)
			self.resizeWindow = 1
		else:
			self.DrawGraph(self.graph)
			
			
			for k in range(len(self.pointArray)):
				if self.pointArray[k][3] == 1:
					graphicsutils.write(self.pointArray[k][0]+self.pointSize, self.pointArray[k][1]+self.pointSize, str(self.pointArray[k][2]), GLUT_BITMAP_HELVETICA_12)
			glutSwapBuffers()


	def DrawGraph(self, graph):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLineWidth(1.5)
    
		# Draw directed arcs.
		for node in self.graph.nodes:
			for edge in node.children:
				far_node = edge.get_far(node)
				if node == far_node:
					print "Circular edge."
					continue
    
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
				graphicsutils.arrowhead(x1, y1, x2, y2, self.pointSize / 2, 20, 12)
    
		#glColor3f(0.7, 0.7, 0.7)
		#graphicsutils.write(0.0, 0.0, "(0,0)")
		#graphicsutils.write(100, 10, "(100,10)")
		#graphicsutils.write(100, 100, "(100,100)")
		#graphicsutils.write(200, 100, "(200,100)")
		#graphicsutils.write(500, 500, "(500,500)")
		
		j = 0
		# Draw nodes.
		for node in self.graph.nodes:
			self.pointArray[j][0] = float(node.x)
			self.pointArray[j][1] = float(node.y)
			self.pointArray[j][2] = node.term
    
			if node.name == 'N0':
				glColor3f(1.0, 0.0, 0.0)
			else:
				glColor3f(0.0, 0.0, 0.0)
			
			glBegin(GL_POINTS)
			glVertex2f(self.pointArray[j][0], self.pointArray[j][1])
			glEnd()
			
			self.pointX = self.pointArray[j][0]
			self.pointY = self.pointArray[j][1]
    
			graphicsutils.write(self.pointArray[j][0], self.pointArray[j][1]+self.pointSize, node.name, GLUT_BITMAP_HELVETICA_12)
			
			j = j + 1
			
		glutSwapBuffers()


	def processMouse(self, button, state, x, y):
		    
		pointylow = self.pointY-10
		pointyhigh = self.pointY+10
		pointxlow = self.pointX-10
		pointxhigh = self.pointX+10
		
		k = 0
		for node in self.graph.nodes:
			self.pointX = self.pointArray[k][0]
			self.pointY = self.pointArray[k][1]
			pointName = self.pointArray[k][2]
    
			pointylow = self.pointY-10
			pointyhigh = self.pointY+10
			pointxlow = self.pointX-10
			pointxhigh = self.pointX+10
    
			if state == GLUT_UP:
				if button == GLUT_LEFT_BUTTON:
					if x>pointxlow and x<pointxhigh and y>pointylow and y<pointyhigh:
						if self.pointArray[k][3] == 1:
							self.pointArray[k][3] = 0
							self.DrawGLScene()
						elif self.pointArray[k][3] == 0:
							self.pointArray[k][3] = 1
							self.DrawGLScene()
			k = k + 1


	def draw(self, kkgraph):
		self.graph = kkgraph
		self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
		glutMainLoop()