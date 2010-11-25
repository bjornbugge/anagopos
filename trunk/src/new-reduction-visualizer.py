# -*- coding: iso-8859-1 -*-
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

import wx
from wx import glcanvas
from glgrapharea import MyCubeCanvas
# 
# 
import computegraph.operations as operations
# import computegraph.lambda_randomgraph as randomgraph
import lambdaparser.lambdaparser as parser

# Drawing algorithms
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph

import gtk
import cairo
import sys
import math
import random
import time
import os
import wx

algorithms = {'Neato' : NeatoGraph,
			'Neato Animated' : MajorizationGraph,
			'Dot' : DotGraph,
			'TwoPi' : TwopiGraph,
			'Circo' : CircoGraph,
			'Fdp' : FdpGraph}

class MainWindow(wx.Frame):
	
	def __init__(self, parent = None, id = -1, title = "Reduction Visualizer"):
		# Init
		wx.Frame.__init__(
				self, parent, id, title, size = (1366,768),
				style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE
		)
		
		#graph = None
		self.drawing = MyCubeCanvas(self)
		# drawing = GraphArea(graph)
		self.drawing.ready = False
		self.drawing.shownewestedget = False

		# Buttons
		self.tf1 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE)
		self.bt1 = wx.Button(self, 0, "Draw Graph",         size=(200, 30))
		self.bt2 = wx.Button(self, 0, "Random Lambda term", size=(200, 30))
		self.bt3 = wx.Button(self, 0, "Forward",            size=(200, 30))
		self.bt4 = wx.Button(self, 0, "Back",               size=(200, 30))
		self.bt5 = wx.Button(self, 0, "Redraw Graph",       size=(200, 30))
		self.bt6 = wx.Button(self, 0, "Optimize Graph",     size=(200, 30))
		self.st1 = wx.StaticText(self, -1, 'Select Drawing Alg: ', (5, 5))
		self.cb1 = wx.ComboBox(self, -1, size=(200, -1), choices=[k for (k,v) in algorithms.iteritems()], style = wx.CB_READONLY)
		self.st2 = wx.CheckBox(self, -1, 'Start')
		self.st3 = wx.StaticText(self, -1, 'Clicked Term: ', (5, 5))
		self.tf2 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE|wx.TE_READONLY)
		self.st4 = wx.StaticText(self, -1, 'Output: ', (5, 5))
		self.tf3 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE|wx.TE_READONLY)
		
		# Button actions
		self.bt1.Bind(wx.EVT_BUTTON, self.DrawGraph)
		self.bt2.Bind(wx.EVT_BUTTON, self.Generate)
		self.bt3.Bind(wx.EVT_BUTTON, self.drawing.Forward)
		self.bt4.Bind(wx.EVT_BUTTON, self.drawing.Back)
		self.bt5.Bind(wx.EVT_BUTTON, self.drawing.Redraw)
		self.bt6.Bind(wx.EVT_BUTTON, self.drawing.Optimize)
		self.cb1.Bind(wx.EVT_COMBOBOX, self.NewAlgoSelected)
		# self.Bind(wx.EVT_LEFT_DOWN, self.drawing.OnMouseDown)
		# self.Bind(wx.EVT_LEFT_UP, self.drawing.OnMouseUp)
		# self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
		
		
		bts = wx.BoxSizer(wx.VERTICAL)
		bts.Add(self.tf1, 0, wx.ALIGN_CENTER|wx.ALL, 10)
		bts.Add(self.bt1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.bt2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.bt3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.bt4, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.bt5, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.bt6, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.st1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.cb1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.st2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.st3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.tf2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.st4, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(self.tf3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(bts, 0, wx.ALIGN_TOP, 15)
		box.Add(self.drawing, 1, wx.EXPAND)
		
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
		message = "Reduction Visualizer\n\nURL:\nhttp://code.google.com/p/reduction-visualizer/\n\nBy:\n Niels Bjoern Bugge Grathwohl\n Jens Duelund Pallesen"
		caption = "Reduction Visualizer"
		wx.MessageBox(message, caption, wx.OK)
	
	def OnExit(self,event):
		self.Close(True)
	
	# def OnMouseDown(self, evt):
	# 	self.CaptureMouse()
	# 	self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
	# 	print self.x
	# 	print self.y
	# 
	# def OnMouseUp(self, evt):
	# 	self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
	# 	print self.x
	# 	print self.y
	# 	# self.ReleaseMouse()
	# 
	# def OnMouseMotion(self, evt):
	# 	if evt.Dragging() and evt.LeftIsDown():
	# 		self.lastx, self.lasty = self.x, self.y
	# 		self.x, self.y = evt.GetPosition()
	# 		self.Refresh(False)
	
	
	def DrawGraph(self, drawing):
		Drawer = algorithms[self.cb1.GetValue()]
		print Drawer
		self.drawing.selected = Drawer
		if True:
			print self.tf1.GetValue()
			self.drawing.ready = True
			self.drawing.startnum = 0
			self.drawing.endnum = 1000000
			tempterm = self.tf1.GetValue()
			tempterm = "(#B1.(((B1 #B2.(#B3.(#B4.(B4)))) #B5.(#B6.(#B7.((((B7 B5) #B8.(#B9.(B5))) B7)))))) #B10.(#B11.(((((#B12.(B11) (#B13.(B11) #B14.((B10 B11)))) (B11 B10)) ((#B15.(#B16.(#B17.(#B18.(#B19.(B11))))) #B20.((#B21.(B20) #B22.(#B23.((#B24.(#B25.(B20)) B23)))))) F1)) (#B26.(#B27.(B27)) #B28.(#B29.(#B30.(#B31.(#B32.(B30))))))))))"
			#tempterm = "#B1.(#B2.(#B3.(B1)))"
			self.drawing.term = parser.parse(tempterm.replace(u'\u03bb',"#"))
			self.drawing.mgs = []
			operations.assignvariables(self.drawing.term)
			# self.drawing.selected = NeatoGraph
			self.drawing.startnumber = 1
			try:
				def iterator():
					Drawer = self.drawing.selected
					for (i,g) in enumerate(operations.reductiongraphiter(self.drawing.term, self.drawing.startnum, self.drawing.endnum)):
						yield g
				self.drawing.iterator = iterator()
			except KeyError:
				pass
			self.drawing.graphnumber = 0
			
			# INIT FUNCTION
			if True:
				Drawer = self.drawing.selected
				rg = self.drawing.iterator.next()
				g = Drawer(rg)
				self.drawing.reductiongraphlist = [rg]
				self.drawing.graph = g
				self.drawing.graphlist = [g]
				self.drawing.starttobig = False
			
			self.drawing.graph.update_layout()
		
		self.drawing.Draw()
	
	def NewAlgoSelected (self, event):
		if hasattr(self.drawing, 'ready') and self.drawing.ready:
			self.drawing.selectedhaschanged = True
			Drawer = algorithms[self.cb1.GetValue()]
			self.drawing.selected = Drawer
			rg = self.drawing.reductiongraphlist[self.drawing.graphnumber]
			g = Drawer(rg)
			self.drawing.graphlist[self.drawing.graphnumber] = g
			self.drawing.graph = self.drawing.graphlist[self.drawing.graphnumber]
			self.drawing.graph.update_layout()
			self.drawing.Draw()
	
	def Generate(self,event):
		print "Generate"
		# self.drawing.InitDraw()
	
	def Forward(self,event):
		print "Forward"
	
	def Back(self,event):
		print "Back"
	
	def Optimize(self,event):
		print "Optimize"
	
	def Redraw(self,event):
		print "Redraw"

operations.setmode('lambda')


app = wx.PySimpleApp()
frame = MainWindow()
app.MainLoop()

# destroying the objects, so that this script works more than once in IDLEdieses Beispiel
del frame
del app