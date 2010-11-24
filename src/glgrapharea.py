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
import computegraph.randomgraph as randomgraph
import lambdaparser.lambdaparser as parser

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


	def OnMouseUp(self, evt):
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
	
	def InitDraw(self, event):
		if True:
			self.startnum = 1
			self.endnum = 1000000
			tempterm = "(#B1.(((B1 #B2.(#B3.(#B4.(B4)))) #B5.(#B6.(#B7.((((B7 B5) #B8.(#B9.(B5))) B7)))))) #B10.(#B11.(((((#B12.(B11) (#B13.(B11) #B14.((B10 B11)))) (B11 B10)) ((#B15.(#B16.(#B17.(#B18.(#B19.(B11))))) #B20.((#B21.(B20) #B22.(#B23.((#B24.(#B25.(B20)) B23)))))) F1)) (#B26.(#B27.(B27)) #B28.(#B29.(#B30.(#B31.(#B32.(B30))))))))))"
			self.term = parser.parse(tempterm.replace(u'\u03bb',"#"))
			self.mgs = []
			operations.assignvariables(self.term)
			self.selected = NeatoGraph
			self.startnumber = 1
			try:
				def iterator():
					Drawer = self.selected
					for (i,g) in enumerate(operations.reductiongraphiter(self.term, self.startnum, self.endnum)):
						yield g
				self.iterator = iterator()
			except KeyError:
				pass
			self.graphnumber = 0
			
			# INIT FUNCTION
			if True:
				Drawer = self.selected
				rg = self.iterator.next()
				g = Drawer(rg)
				self.reductiongraphlist = [rg]
				self.graph = g
				self.graphlist = [g]
				self.starttobig = False
			
			self.graph.update_layout()
			self.Draw()
			
	def Draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		if True:
			Xs = [node.x for node in self.graph.nodes]
			Ys = [node.y for node in self.graph.nodes]
			print "1"
			# print min(Xs)
			# print max(Xs)
			# print min(Ys)
			# print max(Ys)
			# scaling = [max(Xs) / (width - 50), max(Ys) / (height - 50)]
			
			# for node in drawing.graph.nodes:
			# 	print node.x
		
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			gluOrtho2D(0.0, (max(Xs)+10), 0.0, (max(Ys)+10))
			glMatrixMode(GL_MODELVIEW)
			
			# draw six faces of a cube
			# glColor3f(0.3, 0.6, 1.0)
			# glPointSize(10)
			
			for node in self.graph.nodes:
				for edge in node.children:
					glLineWidth(4.5)
					glColor4f(0.3, 0.9, 0.2, 0.1)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glColor4f(0.9, 0.1, 0.8, 0.1)
					glVertex2f(node.x, node.y)
					glEnd()
					
					glLineWidth(3.5)
					glColor4f(0.3, 0.9, 0.2, 0.2)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glColor4f(0.9, 0.1, 0.8, 0.2)
					glVertex2f(node.x, node.y)
					glEnd()
					
					glLineWidth(2.5)
					glColor4f(0.3, 0.9, 0.2, 0.4)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glColor4f(0.9, 0.1, 0.8, 0.4)
					glVertex2f(node.x, node.y)
					glEnd()
					
					glLineWidth(1.5)
					glColor4f(0.3, 0.9, 0.2, 0.6)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glColor4f(0.9, 0.1, 0.8, 0.6)
					glVertex2f(node.x, node.y)
					glEnd()
					
					glLineWidth(1.0)
					glColor4f(0.3, 0.9, 0.2, 0.8)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glColor4f(0.9, 0.1, 0.8, 0.8)
					glVertex2f(node.x, node.y)
					glEnd()
					
					glLineWidth(0.5)
					glColor4f(0.3, 0.9, 0.2, 1.0)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glColor4f(0.9, 0.1, 0.8, 1.0)
					glVertex2f(node.x, node.y)
					glEnd()

			for node in self.graph.nodes:
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

	def Forward(self, event):
		# clear color and depth buffers
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		Drawer = TwopiGraph
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
				print "gg"
		self.SwapBuffers()
		self.Draw()

	def OnDraw(self):
		# clear color and depth buffers
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.SwapBuffers()