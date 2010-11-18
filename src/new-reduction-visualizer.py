#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
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
from glgrapharea import GraphArea
from glgrapharea import CanvasBase

# Drawing algorithms
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph

# TEMP
import pygraphviz as pgv


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




class CubeCanvas(MyCanvasBase):
	
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



	def OnDraw(self):
		# clear color and depth buffers
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		graph = None
		drawing = GraphArea(graph)
		drawing.ready = False
		drawing.shownewestedget = False
		
		# DRAW GRAPH FUNCTION
		if True:
			drawing.startnum = 5
			drawing.endnum = 1000000
			tempterm = "(#B1.(((B1 #B2.(#B3.(#B4.(B4)))) #B5.(#B6.(#B7.((((B7 B5) #B8.(#B9.(B5))) B7)))))) #B10.(#B11.(((((#B12.(B11) (#B13.(B11) #B14.((B10 B11)))) (B11 B10)) ((#B15.(#B16.(#B17.(#B18.(#B19.(B11))))) #B20.((#B21.(B20) #B22.(#B23.((#B24.(#B25.(B20)) B23)))))) F1)) (#B26.(#B27.(B27)) #B28.(#B29.(#B30.(#B31.(#B32.(B30))))))))))"
			drawing.term = parser.parse(tempterm.replace(u'\u03bb',"#"))
			drawing.mgs = []
			operations.assignvariables(drawing.term)
			drawing.selected = NeatoGraph
			drawing.startnumber = 1
			try:
				def iterator():
					Drawer = drawing.selected
					for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
						yield g
				drawing.iterator = iterator()
			except KeyError:
				pass
			drawing.graphnumber = 0
			
			# INIT FUNCTION
			if True:
				Drawer = drawing.selected
				rg = drawing.iterator.next()
				g = Drawer(rg)
				drawing.reductiongraphlist = [rg]
				drawing.graph = g
				drawing.graphlist = [g]
				drawing.starttobig = False
			
			drawing.graph.update_layout()
			
			Xs = [node.x for node in drawing.graph.nodes]
			Ys = [node.y for node in drawing.graph.nodes]
			print min(Xs)
			print max(Xs)
			print min(Ys)
			print max(Ys)
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
			
			for node in drawing.graph.nodes:
				for edge in node.children:
					glLineWidth(4.0)
					glColor4f(0.3, 0.9, 0.2, 0.3)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glVertex2f(node.x, node.y)
					glEnd()
					
					glLineWidth(2.0)
					glColor4f(0.3, 0.9, 0.2, 0.4)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glVertex2f(node.x, node.y)
					glEnd()
					
					glLineWidth(0.5)
					glColor4f(0.3, 0.9, 0.2, 1.0)
					far_node = edge.get_far(node)
					glBegin(GL_LINES)
					glVertex2f(far_node.x, far_node.y)
					glVertex2f(node.x, node.y)
					glEnd()
        	
				glPointSize(15)
				glColor4f(0.3, 0.6, 1.0, 0.3)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()
				
				glPointSize(10)
				glColor4f(0.3, 0.6, 1.0, 0.6)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()
				
				glPointSize(5)
				glColor4f(0.3, 0.6, 1.0, 1.0)
				glBegin(GL_POINTS)
				glVertex2f(node.x, node.y)
				glEnd()

		self.SwapBuffers()

class MainWindow(wx.Frame):

	def __init__(self, parent = None, id = -1, title = "Reduction Visualizer"):
		# Init
		wx.Frame.__init__(
				self, parent, id, title, size = (1366,768),
				style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE
		)
		
		graph = None
		drawing = GraphArea(graph)
		drawing.ready = False
		drawing.shownewestedget = False

		# Buttons
		tf1 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE)
		bt1 = wx.Button(self, 0, "Draw Graph")
		bt2 = wx.Button(self, 0, "Generate Random Lambda term")
		bt3 = wx.Button(self, 0, "Forward")
		bt4 = wx.Button(self, 0, "Back")
		bt5 = wx.Button(self, 0, "Redraw Graph")
		bt6 = wx.Button(self, 0, "Optimize Graph")
		st1 = wx.StaticText(self, -1, 'Select Drawing Alg: ', (5, 5))
		cb1 = wx.ComboBox(self, -1, size=(120, -1))
		st2 = wx.CheckBox(self, -1, 'Start')
		st3 = wx.StaticText(self, -1, 'Clicked Term: ', (5, 5))
		tf2 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE|wx.TE_READONLY)
		st4 = wx.StaticText(self, -1, 'Output: ', (5, 5))
		tf3 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE|wx.TE_READONLY)
		
		# Button actions
		bt1.Bind(wx.EVT_BUTTON, self.DrawGraph)
		bt2.Bind(wx.EVT_BUTTON, self.Generate)
		bt3.Bind(wx.EVT_BUTTON, self.Forward)
		bt4.Bind(wx.EVT_BUTTON, self.Back)
		bt5.Bind(wx.EVT_BUTTON, self.Redraw)
		bt6.Bind(wx.EVT_BUTTON, self.Optimize)
		
		bts = wx.BoxSizer(wx.VERTICAL)
		bts.Add(tf1, 0, wx.ALIGN_CENTER|wx.ALL, 10)
		bts.Add(bt1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt4, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt5, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt6, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(st1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(cb1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(st2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(st3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(tf2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(st4, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(tf3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(bts, 0, wx.ALIGN_TOP, 15)
		box.Add(CubeCanvas(self), 1, wx.EXPAND)
		
		self.SetAutoLayout(True)
		self.SetSizer(box)
		self.Layout()

		# StatusBar
		self.CreateStatusBar()

		# Filemenu
		filemenu = wx.Menu()

		# Filemenu - About
		menuitem = filemenu.Append(-1, "&About", "Reduction Visualizer")
		self.Bind(wx.EVT_MENU, self.OnAbout, menuitem) # here comes the event-handler
		# Filemenu - Separator
		filemenu.AppendSeparator()

		# Filemenu - Exit
		menuitem = filemenu.Append(-1, "E&xit", "Terminate the program")
		self.Bind(wx.EVT_MENU, self.OnExit, menuitem) # here comes the event-handler

		# Menubar
		menubar = wx.MenuBar()
		menubar.Append(filemenu,"&File")
		self.SetMenuBar(menubar)

		# Show
		self.Show(True)


	def OnAbout(self,event):
		message = "Reduction Visualizer\n\nURL:\nhttp://code.google.com/p/reduction-visualizer/\n\nBy:\n Niels Bjørn Bugge Grathwohl\n Jens Duelund Pallesen"
		caption = "Reduction Visualizer"
		wx.MessageBox(message, caption, wx.OK)
	
	def OnExit(self,event):
		self.Close(True)
	
	def DrawGraph(self,event):
		print "DrawGraph"
	
	def Generate(self,event):
		print "Generate"
	
	def Forward(self,event):
		print "Forward"
	
	def Back(self,event):
		print "Back"
	
	def Optimize(self,event):
		print "Optimize"
	
	def Redraw(self,event):
		print "Redraw"


app = wx.PySimpleApp()
frame = MainWindow()
app.MainLoop()

# destroying the objects, so that this script works more than once in IDLEdieses Beispiel
del frame
del app