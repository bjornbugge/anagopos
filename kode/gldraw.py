import random
import math
import time
import computegraph.operations as operations
import graphicsutils
#from computegraph.kkgraph import KKGraph
from computegraph.reductiongraph import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import pdb

class GlDraw(object):
	def __init__(self, width = 1024, height = 768, iterable = None):
		self.term = None
		self.graph = None
		self.node = None
		self.fullscreen = 0
		self.window_height = height
		self.window_width = width
		self.resizeWindow = 0
		self.pointSize = 5
		self.pointArray = None
		self.graphiterable = iterable
		self.graphlist = []
		self.InitGL(width, height)
		self.ipoints = None
		self.cr = None
	
	def InitGL(self, Width, Height):
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		self.window_x = (glutGet(GLUT_SCREEN_WIDTH) - self.window_width)/2
		self.window_y = (glutGet(GLUT_SCREEN_HEIGHT) - self.window_height)/2
		
		self.resizeWindow = 0
		
		glutInitWindowSize(Width, Height)
		glutInitWindowPosition(self.window_x, self.window_y)
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
		# self.pointSize = (((glutGet(GLUT_WINDOW_HEIGHT) + glutGet(GLUT_WINDOW_WIDTH))/2)/50)
	
	def keyPressed(self, *args):
		if args[0] == '\033':
		    sys.exit()
		elif args[0] == 'u':
			self.graph.reset()
			self.graph.update_layout_animated(self.DrawGraph)
			self.resizeWindow = 0
			self.DrawGLScene()
			glutSwapBuffers()
		elif args[0] == 'f':
			if self.fullscreen == 0:
				self.resizeWindow = 0
				self.window_width = glutGet(GLUT_WINDOW_WIDTH)
				self.window_height = glutGet(GLUT_WINDOW_HEIGHT)
				self.window_x = glutGet(GLUT_WINDOW_X)
				self.window_y = glutGet(GLUT_WINDOW_Y)
				glutFullScreen()
				self.fullscreen = 1
			else:
				glutReshapeWindow(self.window_width,self.window_height)
				glutPositionWindow(self.window_x,self.window_y)
				self.fullscreen = 0
		
		elif args[0] == 'n': # Step forwards
			self.graphindex += 1
			
			if self.graphiterable is not None:
				try:
					g = self.graphiterable.next()
					self.graphlist.append(g)
				except StopIteration:
					# We have all the graphs.
					self.graphiterable = None
					self.graphindex -= 1
					print "StopIteration!"
			else:
				if self.graphindex == len(self.graphlist):
					self.graphindex -= 1
			
			self.graph = self.graphlist[self.graphindex]
			if not hasattr(self.graph, 'virgin'):
				self.graph.virgin = False
				self.graph.initwith(self.graphlist[self.graphindex - 1])
				self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
				self.graph.update_layout_animated(self.DrawGraph)
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
		
		elif args[0] == 'm': # Improve current graph
			self.graph.update_layout()
			self.DrawGraph(self.graph)
	
	def DrawGLScene(self):
		if self.resizeWindow == 0:
			self.graph.update_layout_animated(self.DrawGraph)
			self.resizeWindow = 1
		else:
			self.DrawGraph(self.graph)
			p = self.pointSize
			for (x, y, term, c) in self.pointArray:
				if c == 1:
					graphicsutils.write(x + p, y + p, str(term))
			glutSwapBuffers()
	
	def DrawGraph(self, graph):
		self.graph.scale(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		newcolor = (153.0/255.0, 32.0/255.0, 32.0/255.0)
		# Draw directed arcs before the nodes so the arcs don't overlap the nodes.
		# pdb.set_trace()
		
		# Newest
		newest = graph.newest
		
		# Drawing bezier curves if graph is using the dot layout
		if hasattr(graph, 'bezier') and graph.bezier:
			for node in self.graph.nodes:
				for edge in node.children:
					self.ipoints = edge.ipoints
					far_node = edge.get_far(node)
					#edge.ipoints[0][0] = node.x
					#edge.ipoints[0][1] = node.y
					
					#glPointSize(30)
					destX = edge.destination.x
					destY = edge.destination.y
					#print "Dest X: " + str(lastX)
					#print "Dest Y: " + str(lastY)
					#glBegin(GL_POINTS)
					#glVertex2f(lastX, lastY)
					#glEnd()
					#glPointSize(5)
					#glColor3f(random.random(), random.random(), random.random())
					#glPointSize(15)
					#glBegin(GL_POINTS)					
					#for p in edge.ipoints:
					#	glVertex2f(p[0], p[1])
					#glEnd()
					#glColor3f(0,0,0)
					#glPointSize(5)
					
					lastX = edge.ipoints[len(edge.ipoints)-1][0]
					lastY = edge.ipoints[len(edge.ipoints)-1][1]
					if node.y != edge.ipoints[0][1] or node.x != edge.ipoints[0][0]:
						glBegin(GL_LINES)
						glVertex2f(node.x, node.y)
						glVertex2f(edge.ipoints[0][0], edge.ipoints[0][1])
						glEnd()
					if destY != lastY or destX != lastX:
						glBegin(GL_LINES)
						glVertex2f(far_node.x, far_node.y)
						glVertex2f(lastX, lastY)
						glEnd()
					
					POld = [edge.ipoints[0][0], edge.ipoints[0][1]]
					t = 0.00
					l = len(edge.ipoints)
					for g in range(101):
						P = self.drawBezierGen(t, l)
						self.drawLine(POld, P)
						POld = P
						t = t + 0.01
						
		# Drawing regular straight edges
		else:
			for node in graph.nodes:
				for edge in node.children:
					#print "IPOINTS: " + str(edge.ipoints)
					far_node = edge.get_far(node)
					if node == far_node:
						print "Circular edge."
						continue
        	
					x1 = float(node.x)
					y1 = float(node.y)
					x2 = float(far_node.x)
					y2 = float(far_node.y)
					
					# if node.new or far_node.new:
					if node is newest:
						glColor3f(newcolor[0], newcolor[1], newcolor[2])
						glLineWidth(2)
					else:
						glColor3f(130.0/255.0, 172.0/255.0, 245.0/255.0)
						glLineWidth(1)
					glBegin(GL_LINES)
					glVertex2f(x1, y1)
					#if node.new or far_node.new:
					#	glColor3f(32.0/255.0, 153.0/255.0, 34.0/255.0)
					#else:
					#	glColor3f(165.0/255.0, 255/255, 135.0/255.0)
						
					glVertex2f(x2, y2)
					glEnd()
					
					glColor3f(255.0/255.0, 150.0/255.0, 31.0/255.0)
					graphicsutils.arrowhead(x1, y1, x2, y2, self.pointSize / 2, 15, 12)
		
		# Drawing nodes
		for (j, node) in enumerate(graph.nodes):
			self.pointArray[j][0] = node.x
			self.pointArray[j][1] = node.y
			self.pointArray[j][2] = node.term
    
			if node.name == 'N0':
				glColor3f(1.0, 0.0, 0.0)
			elif node is newest:
				glColor3f(newcolor[0], newcolor[1], newcolor[2])
			else:
				glColor3f(0.0, 0.0, 0.0)
			
			if len(node.term.redexpositions) == 0:
				p = 5 * self.pointSize
			elif node is newest:
				p = 2 * self.pointSize
			else:
				p = self.pointSize
			
			glPointSize(p)
			
			glBegin(GL_POINTS)
			glVertex2f(node.x, node.y)
			glEnd()
			
			glColor3f(0.0, 0.0, 0.0)
			
			# Drawing node names
			graphicsutils.write(node.x, node.y + p, node.name)
		
		glutSwapBuffers()
	
	def processMouse(self, button, state, x, y):
		r = 10
		for (k, (pX, pY, n, c)) in enumerate(self.pointArray):
			if state == GLUT_UP:
				if button == GLUT_LEFT_BUTTON:
					if int(x) in xrange(pX - r, pX + r) and int(y) in xrange(pY - r, pY + r):
						if c == 1:
							self.pointArray[k][3] = 0
							self.DrawGLScene()
						elif c == 0:
							self.pointArray[k][3] = 1
							self.DrawGLScene()
	
	def drawiter(self):
		if self.graphiterable is None:
			print "self.graphiterable is None"
			return
		
		self.graphlist.append(self.graphiterable.next())
		self.graphindex = 0
		self.graph = self.graphlist[0]
		self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
		self.graph.update_layout()
		glutMainLoop()
		
	def drawLine(self, p1, p2):
		glBegin(GL_LINES);
		#glColor3f(self.c1old, self.c2old, self.c3old)
		glVertex2f(p1[0], p1[1]);
		#glColor3f(self.c1, self.c2, self.c3)
		glVertex2f(p2[0], p2[1]);
		glEnd();
		#self.c1old = self.c1
		#self.c2old = self.c2
		#self.c2old = self.c3
		#self.c1 = self.c1 + (0.040000/5)
		#self.c2 = self.c2 - (0.026861/5)
		#self.c3 = self.c3 - (0.019988/5)
    
	def binomial(self, n, i):
		bin = math.factorial(n)/(math.factorial(i) * math.factorial(n - i))
		return bin
    
	def drawBezierGen(self, t, l):
		#l = len(self.ipoints)
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
	
	def drawlist(self, graphlist):
		self.graphindex = 0
		self.graphlist = graphlist
		self.graph = graphlist[0]
		self.pointArray = [[0 for col in range(4)] for row in range(len(self.graph.nodes))]
		# self.graph.update_layout_animated(self.DrawGraph)
		self.graph.update_layout()
		glutMainLoop()
			
	def draw(self, kkgraph):
		self.drawlist([kkgraph])