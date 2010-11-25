# Reduction Visualizer. A tool for visualization of reduction graphs.
# Copyright (C) 2010 Niels Bjoern Bugge Grathwohl and Jens Duelund Pallesen
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import cairo
import sys
import math
import random
import time
import os
import wx
from wx import glcanvas
from OpenGL.GL import *	 
from OpenGL.GLU import *	 
from OpenGL.GLUT import *
import computegraph.operations as operations
# import computegraph.randomgraph as randomgraph
# import lambdaparser.lambdaparser as parser

# Drawing algorithms
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph

class MyCanvasBase(glcanvas.GLCanvas):
	def __init__(self, parent, width = 1024, height = 768, iterable = None):
		glcanvas.GLCanvas.__init__(self, parent, -1)
		self.init = False
		self.context = glcanvas.GLContext(self)
		
		# initial mouse position
		self.lastx = self.x = 30
		self.lasty = self.y = 30
		self.size = None
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
		self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
		self.term = None
		self.graph = None
		self.node = None
		self.fullscreen = 0
		self.orthoLeft = 0.0
		self.orthoRight = 0.0
		self.orthoBottom = 0.0
		self.orthoTop = 0.0
		self.window_height = height
		self.window_width = width
		self.resizeWindow = 0
		self.pointSize = 5
		self.pointArray = None
		self.graphiterable = iterable
		self.graphlist = []
		# self.InitGL(width, height)
		self.ipoints = None
		self.cr = None


	def OnEraseBackground(self, event):
		pass # Do nothing, to avoid flashing on MSW.


	def OnSize(self, event):
		wx.CallAfter(self.DoSetViewport)
		event.Skip()

	def DoSetViewport(self):
		size = self.size = self.GetClientSize()
		self.SetCurrent(self.context)
		glViewport(0, 0, size.width, size.height)
		


	def OnPaint(self, event):
		dc = wx.PaintDC(self)
		self.SetCurrent(self.context)
		if not self.init:
			self.InitGL(self.window_height, self.window_width)
			self.init = True
		self.OnDraw()


	def OnMouseDown(self, evt):
		self.CaptureMouse()
		self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
		# print self.GetSize()[0]
		# print self.GetSize()[1]
		
		propX = float(self.x)/float(self.GetSize()[0])
		propY = float(self.y)/float(self.GetSize()[1])
		
		scX = self.orthoRight - self.orthoLeft
		scY = self.orthoBottom - self.orthoTop
		
		X = propX * scX
		Y = propY * scY
		
		# print "X = " + str(self.x) + "/" + str(self.GetSize()[0]) + "(" + str(self.orthoRight) + "-" + str(self.orthoLeft) + ")"
		# print "Y = " + str(self.y) + "/" + str(self.GetSize()[1]) + "(" + str(self.orthoBottom) + "-" + str(self.orthoTop) + ")"
		
		# print self.x
		# print self.y
		# print self.orthoLeft
		# print self.orthoRight
		# print self.orthoBottom
		# print self.orthoTop
		x = self.x#/self.orthoRight
		y = self.y#/self.orthoBottom
		# print "X:         " + str(x)
		# print "Y:         " + str(y)
		rX = 20/float(self.GetSize()[0])*scX
		rY = 20/float(self.GetSize()[1])*scY
		# print rX
		# print rY
		if self.ready:
			for node in self.graph.nodes:
				
				nX = node.x - self.orthoLeft
				nY = node.y - self.orthoTop
				
				# print "node name:           " + node.name
				# print "     X node coord:   " + str(nX)
				# print "     Y node coord:   " + str(nY)
				# print "     X node clicked: " + str(X)
				# print "     Y node clicked: " + str(Y)
				
				if (X > (nX-rX)) and (X < (nX + rX)) and (Y > (nY - rY)) and (Y < (nY + rY)):
					# self.graph.dragnode = True
					# self.graph.dragnodename = node.name
					# self.graph.dragnodex = x
					# self.graph.dragnodey = y
					# self.graph.dragnodenode = node
					print "you have clicked node " + node.name
					print node
				# else:
				# 	print "you have NOT clicked a node"

	def OnMouseUp(self, evt):
		self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
		# print self.x
		# print self.y
		self.ReleaseMouse()


	def OnMouseMotion(self, evt):
		if evt.Dragging() and evt.LeftIsDown() and False:
			self.lastx, self.lasty = self.x, self.y
			self.x, self.y = evt.GetPosition()
			self.Refresh(False)


class MyCubeCanvas(MyCanvasBase):
	
	def InitGL(self, Width, Height):

		# Anti-aliasing/prettyness stuff
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)
		glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
		glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
		glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
		glEnable(GL_LINE_SMOOTH)
		glEnable(GL_POINT_SMOOTH)
		glEnable(GL_POLYGON_SMOOTH)
			
	def Draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		if True:
			Xs = [node.x for node in self.graph.nodes]
			Ys = [node.y for node in self.graph.nodes]
		
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			self.orthoLeft = min(Xs) - max(Xs)*0.02
			self.orthoRight = ( max(Xs) + max(Xs)*0.02)
			self.orthoBottom = ( max(Ys) + max(Ys)*0.02)
			self.orthoTop = min(Ys) - max(Ys)*0.02
			self.orthoDiagonal = self.orthoRight + self.orthoBottom
			
			# print "Min Xs" + str(min(Xs))
			# print "Max Xs" + str(max(Xs))
			# print "Min Ys" + str(min(Ys))
			# print "Max Ys" + str(max(Ys))
			# 
			# print "Ortho Left:   " + str(self.orthoLeft)
			# print "Ortho Right:  " + str(self.orthoRight)
			# print "Ortho Bottom: " + str(self.orthoBottom)
			# print "Ortho Top:    " + str(self.orthoTop)
			
			
			gluOrtho2D(self.orthoLeft, self.orthoRight, self.orthoBottom, self.orthoTop)
			glMatrixMode(GL_MODELVIEW)
			
			# draw six faces of a cube
			# glColor3f(0.3, 0.6, 1.0)
			# glPointSize(10)
			for node in self.graph.nodes:
				for edge in node.children:
					if hasattr(self.graph, 'bezier') and self.graph.bezier:
						far_node = edge.get_far(node)
						if edge.destination == node:
							continue
						
						destX = edge.destination.x
						destY = edge.destination.y
						
						lastX = edge.ipoints[len(edge.ipoints) - 1][0]
						lastY = edge.ipoints[len(edge.ipoints) - 1][1]
						
						if node.y != edge.ipoints[0][1] or node.x != edge.ipoints[0][0]:
							self.DrawLine(node.x, node.y, edge.ipoints[0][0], edge.ipoints[0][1])
							# self.__cr.move_to(node.x, node.y)
							# self.__cr.line_to(edge.ipoints[0][0], edge.ipoints[0][1])
							# self.__cr.stroke()
						if destY != lastY or destX != lastX:
							self.DrawLine(far_node.x, far_node.y, lastX, lastY)
							# self.__cr.move_to(far_node.x, far_node.y)
							# self.__cr.line_to(lastX, lastY)
							# self.__cr.stroke()
							
						POld = [edge.ipoints[0][0], edge.ipoints[0][1]]
						t = 0.00
						l = len(edge.ipoints)
						for g in xrange(101):
							P = drawBezierGen(t, l, edge.ipoints)
							self.DrawLine(POld[0], POld[1], P[0], P[1])
							# self.__cr.move_to(POld[0], POld[1])
							# self.__cr.line_to(P[0], P[1])
							# self.__cr.stroke()
							POld = P
							t = t + 0.01
					else:
						far_node = edge.get_far(node)
						x1 = far_node.x
						y1 = far_node.y
						x2 = node.x
						y2 = node.y
						self.DrawLine(x1, y1, x2, y2)
					
						radius = self.orthoDiagonal
						if node != edge.get_far(node):
							#    draw_arrowhead(x1, y1, x2, y2, noderadius, arrowwidth, transparency, angle):
							self.draw_arrowhead(x1, y1, x2, y2, radius/150, self.orthoDiagonal/230, 1.0, 15)
							# self.draw_arrowhead(x1, y1, x2, y2, radius/160, self.orthoDiagonal/220, 0.9, 16)
							self.draw_arrowhead(x1, y1, x2, y2, radius/170, self.orthoDiagonal/210, 0.8, 17)
							# self.draw_arrowhead(x1, y1, x2, y2, radius/180, self.orthoDiagonal/200, 0.7, 18)
							self.draw_arrowhead(x1, y1, x2, y2, radius/190, self.orthoDiagonal/190, 0.6, 19)
							# self.draw_arrowhead(x1, y1, x2, y2, radius/200, self.orthoDiagonal/180, 0.5, 20)
							self.draw_arrowhead(x1, y1, x2, y2, radius/210, self.orthoDiagonal/170, 0.4, 21)
							# self.draw_arrowhead(x1, y1, x2, y2, radius/220, self.orthoDiagonal/160, 0.3, 22)
							self.draw_arrowhead(x1, y1, x2, y2, radius/230, self.orthoDiagonal/150, 0.1, 23)
							
							# if node != edge.get_far(node):
							# 	self.draw_arrowhead(x1, y1, x2, y2, radius)

			for node in self.graph.nodes:
				# print node.x
				# print node.y
				glPointSize(20)
				glColor4f(0.3, 0.6, 1.0, 0.1)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()
				
				glPointSize(18)
				glColor4f(0.3, 0.6, 1.0, 0.2)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()
				
				glPointSize(16)
				glColor4f(0.3, 0.6, 1.0, 0.4)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()
				
				glPointSize(14)
				glColor4f(0.3, 0.6, 1.0, 0.6)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()
				
				glPointSize(12)
				glColor4f(0.3, 0.6, 1.0, 0.8)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()
				
				glPointSize(10)
				glColor4f(0.3, 0.6, 1.0, 1.0)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()
		
		self.SwapBuffers()
	def DrawLine(self, x1, y1, x2, y2):
		glLineWidth(4.5)
		glColor4f(0.3, 0.9, 0.2, 0.1)
		glBegin(GL_LINES)
		glVertex2f(x1, y1)
		glVertex2f(x2, y2)
		glEnd()
		
		glLineWidth(3.5)
		glColor4f(0.3, 0.9, 0.2, 0.2)
		glBegin(GL_LINES)
		glVertex2f(x1, y1)
		glVertex2f(x2, y2)
		glEnd()
		
		glLineWidth(2.5)
		glColor4f(0.3, 0.9, 0.2, 0.4)
		glBegin(GL_LINES)
		glVertex2f(x1, y1)
		glVertex2f(x2, y2)
		glEnd()
		
		glLineWidth(1.5)
		glColor4f(0.3, 0.9, 0.2, 0.6)
		glBegin(GL_LINES)
		glVertex2f(x1, y1)
		glVertex2f(x2, y2)
		glEnd()
		
		glLineWidth(1.0)
		glColor4f(0.3, 0.9, 0.2, 0.8)
		glBegin(GL_LINES)
		glVertex2f(x1, y1)
		glVertex2f(x2, y2)
		glEnd()
		
		glLineWidth(0.5)
		glColor4f(0.3, 0.9, 0.2, 1.0)
		glBegin(GL_LINES)
		glVertex2f(x1, y1)
		glVertex2f(x2, y2)
		glEnd()
		
	
	def draw_arrowhead(self, x1, y1, x2, y2, noderadius, awidth, transparency, angle):
		'''
		Draws an arrow head on the line segment between the coordinate pairs
		(x1,y1) and (x2,y2). The arrow head is placed in the (x2,y2)-end.
		'''
		arrowwidth = awidth
		Pi = math.pi
		# angle = 30
		
		if x1 - x2 == 0:
			if y2 <= y1:
				LineAngle = Pi / 2
			else:
				LineAngle = 3 * Pi / 2
		else:
			LineAngle = math.atan((y2 - y1) / (x2 - x1))
	
		EndAngle1 = LineAngle + angle * Pi/180
		EndAngle2 = LineAngle - angle * Pi/180
	
		xOffset = noderadius * math.cos(LineAngle)
		yOffset = noderadius * math.sin(LineAngle)
		if x1 < x2:
			Y3 = y2 - arrowwidth * math.sin(EndAngle1)
			Y4 = y2 - arrowwidth * math.sin(EndAngle2)
			X3 = x2 - arrowwidth * math.cos(EndAngle1)
			X4 = x2 - arrowwidth * math.cos(EndAngle2)
			
			x2 -= xOffset
			y2 -= yOffset
			Y3 -= yOffset
			Y4 -= yOffset
			X3 -= xOffset
			X4 -= xOffset
		else:
			Y3 = y2 + arrowwidth * math.sin(EndAngle1)
			Y4 = y2 + arrowwidth * math.sin(EndAngle2)
			X3 = x2 + arrowwidth * math.cos(EndAngle1)
			X4 = x2 + arrowwidth * math.cos(EndAngle2)
			x2 += xOffset
			y2 += yOffset
			Y3 += yOffset
			Y4 += yOffset
			X3 += xOffset
			X4 += xOffset
		
		# Anti-aliasing/prettyness stuff
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)
		glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
		glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
		glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
		glEnable(GL_LINE_SMOOTH)
		glEnable(GL_POINT_SMOOTH)
		glEnable(GL_POLYGON_SMOOTH)
		
		glLineWidth(1.0)
		glColor4f(1.0, 0.2, 0.9, transparency)
		glBegin(GL_TRIANGLES)
		glVertex2f(x2, y2)
		glVertex2f(X3, Y3)
		glVertex2f(X4, Y4)
		glEnd()

	
	def Forward(self, event):
		# clear color and depth buffers
		# glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		Drawer = self.selected
		self.firstgraph = False
		if self.graphnumber + 2 <= len(self.graphlist):
			if hasattr(self, 'selectedhaschanged') and self.selectedhaschanged:
				self.graphnumber += 1
				rg = self.reductiongraphlist[self.graphnumber]
				g = Drawer(rg)
				self.graphlist[self.graphnumber] = g
				self.graph = g
				self.graph.initwith(self.graphlist[self.graphnumber - 1])
				# outputtext()
				self.graph.update_layout(self.term, self.startnum, self.endnum)
				# drawing.selectedhaschanged = False
				print "ee"
			else:
				self.graphnumber += 1
				self.graph = self.graphlist[self.graphnumber]
				self.graph.initwith(self.graphlist[self.graphnumber - 1])
				self.graph.update_layout(self.term, self.startnum, self.endnum)
				print "jj"
		else:
			try:
				rg = self.iterator.next()
				g = Drawer(rg)
				self.reductiongraphlist.append(rg)
				self.graphlist.append(g)
				self.graphnumber += 1
				self.graph = self.graphlist[self.graphnumber]
				if type(self.graph) is type(self.graphlist[self.graphnumber - 1]):
					self.graph.initwith(self.graphlist[self.graphnumber - 1])
				self.graph.update_layout()
				print "uu"
			except StopIteration:
				self.nomoregraphs = True
				# outputtext()
				print "No more graphs"
		# self.SwapBuffers()
		self.Draw()
	
	def Back(self, event):
		Drawer = self.selected
		self.nomoregraphs = False
		if self.graphnumber == 0:
			# outputtext()
			self.firstgraph = True
		else:
			self.firstgraph = False
			if hasattr(self, 'selectedhaschanged') and self.selectedhaschanged:
				self.graphnumber -= 1
				rg = self.reductiongraphlist[self.graphnumber]
				g = Drawer(rg)
				self.graphlist[self.graphnumber] = g
				self.graph = g
				self.graph.initwith(self.graphlist[self.graphnumber + 1])
				# outputtext()
				self.graph.update_layout_animated(iter_animated)
				# self.queue_draw()
				# drawing.selectedhaschanged = False
			else:
				self.graphnumber -= 1
				self.graph = self.graphlist[self.graphnumber]
				# outputtext()
				self.graph.update_layout()
				# drawing.queue_draw()
		# outputtext()
		self.Draw()
	
	def Redraw(self, event):
		if self.ready:
			self.graph.reset()
			self.graph.update_layout()
			self.Draw()
		else:
			print "No graph created yet!"
		
	def Optimize(self, event):
		if self.ready:
			self.graph.update_layout()
			self.Draw()
		else:
			print "No graph created yet!"
	
	def OnDraw(self):
		# clear color and depth buffers
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.SwapBuffers()

def binomial(n, i):
	bin = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
	return bin

# calculated the bezier lines
def drawBezierGen(t, l, ipoints):
	n = l - 1
	fun = lambda a, b:a + b
	x = reduce(fun, (binomial(n, i) * pow((1 - t), n - i) * pow(t, i) * ipoints[i][0] for i in xrange(l)))
	y = reduce(fun, (binomial(n, i) * pow((1 - t), n - i) * pow(t, i) * ipoints[i][1] for i in xrange(l)))
	return [x, y]