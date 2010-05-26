import math
import time
import random
import computegraph.operations as operations
import lambdaparser as parser
import randomgraph
import graphicsutils
import gldraw2
import testdraw
import pygraphviztest
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
		self.pointSize = 5
		self.pointX = None
		self.pointY = None
		self.pointArray = None
		self.InitGL(1024, 768)
		self.ipoints = ipoints = None
		self.scalingX = None
		self.scalingY = None
		self.c1 = None
		self.c2 = None
		self.c3 = None
		self.c1old = None
		self.c2old = None
		self.c3old = None
		
		
	def InitGL(self, Width, Height):
		
		#print "2"
		
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
    
		# glutMouseFunc(self.processMouse)
    
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
			print "     update"
			self.ipoints = None
			#self.pointSize = 10# (((glutGet(GLUT_WINDOW_HEIGHT) + glutGet(GLUT_WINDOW_WIDTH))/2)/50)
			k = 0
			for node in self.graph.nodes:
				node.x = random.randint(1, self.window_width)
				self.pointArray[k][0] = node.x
				node.y = random.randint(1, self.window_height)
				self.pointArray[k][1] = node.y
				self.pointArray[k][3] = 0
				k = k + 1
			g = pygraphviztest.GraphViz()
			#print type(self.graph)
			self.graph = g.update(self.graph)
			#print type(self.graph)
			self.resizeWindow = 0
			self.DrawGLScene()
			glutSwapBuffers()
		elif args[0] == 'f':
			self.pointSize = 10# (((glutGet(GLUT_WINDOW_HEIGHT) + glutGet(GLUT_WINDOW_WIDTH))/2)/50)
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
		elif args[0] == 'n': # Step forwards
			self.graphindex += 1
			if self.graphindex == len(self.graphlist):
				self.graphindex -= 1
				return
			self.graph = self.graphlist[self.graphindex]
			if self.graph.virgin:
				self.graph.virgin = False
				self.graph.initwith(self.graphlist[self.graphindex - 1])
				self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
				#self.graph.update_layout_animated(self.DrawGraph)
			else:
				self.DrawGraph(self.graph)
        
		elif args[0] == 'b': # Step backwards
			self.graphindex -= 1
			if self.graphindex < 0:
				self.graphindex = 0
			self.graph = self.graphlist[self.graphindex]
			# self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
			# self.graph.update_layout()
			self.DrawGraph(self.graph)


	def DrawGLScene(self):
		#print "3"
		if self.resizeWindow == 0:
			#print "WHAT"
			self.DrawGraph(self.graph)
			#self.graph.update_layout_animated(self.DrawGraph)
			self.resizeWindow = 1
		else:
			#print "BETTER"
			self.DrawGraph(self.graph)
			
			
			#for k in range(len(self.pointArray)):
			#	if self.pointArray[k][3] == 1:
			#		graphicsutils.write(self.pointArray[k][0]+self.pointSize, self.pointArray[k][1]+self.pointSize, str(self.pointArray[k][2]), GLUT_BITMAP_HELVETICA_12)
			#glutSwapBuffers()

	def drawLine(self, p1, p2):
		glBegin(GL_LINES);
		#glColor3f(self.c1old, self.c2old, self.c3old)
		glVertex2f(p1[0], p1[1]);
		#glColor3f(self.c1, self.c2, self.c3)
		glVertex2f(p2[0], p2[1]);
		glEnd();
		self.c1old = self.c1
		self.c2old = self.c2
		self.c2old = self.c3
		self.c1 = self.c1 + (0.040000/5)
		self.c2 = self.c2 - (0.026861/5)
		self.c3 = self.c3 - (0.019988/5)
		
	def binomial(self, n, i):
		bin = math.factorial(n)/(math.factorial(i) * math.factorial(n - i))
		return bin
	
	def drawBezierGen(self, t):
		l = len(self.ipoints)
		n = l-1
		#print "Length: " + str(l)
		x = y = 0
		for i in range(l):
			#print "I: " + str(i)
			#print "!: " + str((math.factorial(n)/(math.factorial(i) * math.factorial(n - i))))
			x = x + self.binomial(n,i) * pow((1 - t),n-i) * pow(t,i) * self.ipoints[i][0]
			y = y + self.binomial(n,i) * pow((1 - t),n-i) * pow(t,i) * self.ipoints[i][1]
			#glBegin(GL_POINTS)
			#glVertex2f(self.ipoints[i][0], self.ipoints[i][1])
			#glEnd()
		return [x,y]
	
		
		
	#def drawBezier2(self, t):
	#	# ipointsX = edge.ipoints[:][0]
	#	# ipointsY = edge.ipoints[:][1]
	#	# 
	#	# 
	#	# for s in edge.ipoints[0][0]:
	#	
	#	for g in range(len(self.ipoints)):
	#		
	#	x = pow((1 - t), 2) * self.ipoints[0][0] + 2 * t * (1 -t) * self.ipoints[1][0] + pow(t, 2) * self.ipoints[2][0]
	#	y = pow((1 - t), 2) * self.ipoints[0][1] + 2 * t * (1 -t) * self.ipoints[1][1] + pow(t, 2) * self.ipoints[2][1]
	#	return [x,y]
	
	def drawlist(self, graphlist):
		self.graphindex = 0
		self.graphlist = graphlist
		self.graph = graphlist[0]
		#print "Graph: " + str(self.graph)
		# self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
		# self.graph.update_layout_animated(self.DrawGraph)
		glutMainLoop()

	def DrawGraph(self, graph):
		
		self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
		
		#print "4"
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLineWidth(1)
		
		# print "Gamle positioner"
		h = 0
		for node in self.graph.nodes:
			print "Node: " + str(node.x)
			self.pointArray[h][0] = float(node.x)
			self.pointArray[h][1] = float(node.y)
			# print "X: " + str(self.pointArray[h][0])
			# print "Y: " + str(self.pointArray[h][1])
			h = h + 1
			
		maxPosX = max(self.pointArray)[0]
		maxPosY = (max(self.pointArray,key=lambda x:x[1]))[1]
		scalingX = (maxPosX)/(self.window_width-50)
		scalingY = (maxPosY)/(self.window_height-50)
		
		self.scalingX = scalingX
		self.scalingY = scalingY
		
		#print "Scaling X: " + str(scalingX)
		#print "Scaling Y: " + str(scalingY)
		#print "Width X: " + str(self.window_width)
		#print "Height Y: " + str(self.window_height)
		
		# print "Nye positioner"
		h = 0
		for node in self.graph.nodes:
			self.pointArray[h][0] = float(node.x)/(scalingX)
			self.pointArray[h][1] = float(node.y)/(scalingY)
			node.x = float(node.x)/(scalingX)
			node.y = float(node.y)/(scalingY)
			# print "X: " + str(self.pointArray[h][0])
			# print "Y: " + str(self.pointArray[h][1])
			h = h + 1
    
		# Draw directed arcs.
		for node in self.graph.nodes:
			for edge in node.children:
				glColor3f(random.random(), random.random(), random.random())
				#print "1: " + str((edge[0][0])/(scalingX)) + ", " + str((edge.ipoints[0][1])/(scalingY))
				#print "2: " + str(float(node.x)) + ", " + str(float(node.y))
				
				
				far_node = edge.get_far(node)
				if node == far_node:
					print "Circular edge."
					continue
				
				# glBegin(GL_LINES);
				# glVertex2f(far_node.x, far_node.y);
				# glVertex2f(edge.ipoints[1][0], edge.ipoints[1][1]);
				# glEnd();
				# 
				# glBegin(GL_LINES);
				# glVertex2f(node.x, node.y);
				# glVertex2f(edge.ipoints[1][0], edge.ipoints[1][1]);
				# glEnd();
				
				self.c1 = 0.00000
				self.c2 = 0.63722
				self.c3 = 0.99976
				self.c1old = 0.00000
				self.c2old = 0.63722
				self.c3old = 0.99976
				
				print "edge.ipoints" + str(edge.ipoints)
				
				self.ipoints = [[0 for col in range(2)] for row in range(len(edge.ipoints))]
				#self.ipoints = [[0 for col in range(2)] for row in range(len(edge.ipoints))]
				
				ff = 0
				for point in range(len(edge.ipoints)):
					self.ipoints[ff][0] = edge.ipoints[ff][0]/self.scalingX
					self.ipoints[ff][1] = edge.ipoints[ff][1]/self.scalingY
					ff = ff + 1
				
				
				
				self.ipoints[0][0] = node.x
				self.ipoints[0][1] = node.y
				self.ipoints[len(edge.ipoints)-1][0] = far_node.x
				self.ipoints[len(edge.ipoints)-1][1] = far_node.y
				
				POld = [self.ipoints[0][0], self.ipoints[0][1]]
				t = 0.00
				
				bezier = 0
				
				
				if bezier == 1:
					if len(edge.ipoints) == 4:
						#print "Length of array: " + str(len(edge.ipoints)) + "	- Y = " + str(node.y) + "	- X = " + str(node.x)
						for g in range(101):
							P = self.drawBezierGen(t)
							self.drawLine(POld, P)
							POld = P
							t = t + 0.01
					elif len(edge.ipoints) == 11:
						#print "Length of array: " + str(len(edge.ipoints)) + "	- Y = " + str(node.y) + "	- X = " + str(node.x)
						for g in range(101):
							P = self.drawBezierGen(t)
							self.drawLine(POld, P)
							POld = P
							t = t + 0.01
					elif len(edge.ipoints) == 110:
						for g in range(101):
							P = self.drawBezierGen(t)
							self.drawLine(POld, P)
							POld = P
							t = t + 0.01
					elif len(edge.ipoints) == 113:
						for g in range(101):
							P = self.drawBezierGen(t)
							self.drawLine(POld, P)
							POld = P
							t = t + 0.01
				else:
					x1 = float(node.x)#/(scalingX)			#/100
					y1 = float(node.y)#/(scalingY)			#/100
					x2 = float(far_node.x)#/(scalingX)		#/100
					y2 = float(far_node.y)#/(scalingY)		#/100
					#glColor3f(0.80000, 0.10000, 0.99976)
					glColor3f(random.random(), random.random(), random.random())
					glBegin(GL_LINES)
					glVertex2f(x1, y1)
					#glColor3f(0.00000, 0.63722, 0.60000)
					glVertex2f(x2, y2)
					glEnd()
				
				# glColor3f(0.1, 0.3, 0.7)
				# graphicsutils.arrowhead(x1, y1, x2, y2, self.pointSize / 2, 20, 12)
    
		#glColor3f(0.7, 0.7, 0.7)
		#graphicsutils.write(0.0, 0.0, "(0,0)")
		#graphicsutils.write(100, 10, "(100,10)")
		#graphicsutils.write(100, 100, "(100,100)")
		#graphicsutils.write(200, 100, "(200,100)")
		#graphicsutils.write(500, 500, "(500,500)")
		
		j = 0
		# Draw nodes.
		for node in self.graph.nodes:
			self.pointArray[j][0] = float(node.x)#/(scalingX)
			self.pointArray[j][1] = float(node.y)#/(scalingY)
			self.pointArray[j][2] = node.term
			
			#print "X cord: " + str(node.x)
			# print "Y cord: " + str(node.y)
    
			if node.name == 'N0':
				glPointSize(8)
				glColor3f(0.8, 0.0, 0.3)
			else:
				glPointSize(self.pointSize)
				glColor3f(0.0, 0.0, 0.0)
			
			glBegin(GL_POINTS)
			glVertex2f(self.pointArray[j][0], self.pointArray[j][1])
			glEnd()
			
			self.pointX = self.pointArray[j][0]
			self.pointY = self.pointArray[j][1]
			
			if len(self.graph.nodes) < 100:
				graphicsutils.write(self.pointArray[j][0], self.pointArray[j][1]+self.pointSize, node.name, GLUT_BITMAP_HELVETICA_10)
			
			j = j + 1
			
		glutSwapBuffers()
		
		print "Nu skulle grafen vaere tegnet"


	#def processMouse(self, button, state, x, y):
	#	    
	#	pointylow = self.pointY-10
	#	pointyhigh = self.pointY+10
	#	pointxlow = self.pointX-10
	#	pointxhigh = self.pointX+10
	#	
	#	k = 0
	#	for node in self.graph.nodes:
	#		self.pointX = self.pointArray[k][0]
	#		self.pointY = self.pointArray[k][1]
	#		pointName = self.pointArray[k][2]
    #
	#		pointylow = self.pointY-10
	#		pointyhigh = self.pointY+10
	#		pointxlow = self.pointX-10
	#		pointxhigh = self.pointX+10
    #
	#		if state == GLUT_UP:
	#			if button == GLUT_LEFT_BUTTON:
	#				if x>pointxlow and x<pointxhigh and y>pointylow and y<pointyhigh:
	#					if self.pointArray[k][3] == 1:
	#						self.pointArray[k][3] = 0
	#						self.DrawGLScene()
	#					elif self.pointArray[k][3] == 0:
	#						self.pointArray[k][3] = 1
	#						self.DrawGLScene()
	#		k = k + 1


	def draw(self, kkgraph):
		#print "1"
		self.graph = kkgraph
		self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
		glutMainLoop()