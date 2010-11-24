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


import computegraph.operations as operations
# import computegraph.lambda_randomgraph as randomgraph
# import lambdaparser.lambdaparser as parser

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

class MainWindow(wx.Frame):

	def __init__(self, parent = None, id = -1, title = "Reduction Visualizer"):
		# Init
		wx.Frame.__init__(
				self, parent, id, title, size = (1366,768),
				style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE
		)
		
		graph = None
		drawing = MyCubeCanvas(self)
		# drawing = GraphArea(graph)
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
		bt1.Bind(wx.EVT_BUTTON, drawing.InitDraw)
		bt2.Bind(wx.EVT_BUTTON, self.Generate)
		bt3.Bind(wx.EVT_BUTTON, drawing.Forward)
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
		box.Add(drawing, 1, wx.EXPAND)
		
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
	
	def DrawGraph(self, drawing):
		if True:
			drawing.startnum = 20
			drawing.endnum = 1000000
			tempterm = "(#B1.(((B1 #B2.(#B3.(#B4.(B4)))) #B5.(#B6.(#B7.((((B7 B5) #B8.(#B9.(B5))) B7)))))) #B10.(#B11.(((((#B12.(B11) (#B13.(B11) #B14.((B10 B11)))) (B11 B10)) ((#B15.(#B16.(#B17.(#B18.(#B19.(B11))))) #B20.((#B21.(B20) #B22.(#B23.((#B24.(#B25.(B20)) B23)))))) F1)) (#B26.(#B27.(B27)) #B28.(#B29.(#B30.(#B31.(#B32.(B30))))))))))"
			# drawing.term = parser.parse(tempterm.replace(u'\u03bb',"#"))
			drawing.term = operations.parse(tempterm.replace(u'\u03bb',"#"))
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

			if True:
				Drawer = drawing.selected
				rg = drawing.iterator.next()
				g = Drawer(rg)
				drawing.reductiongraphlist = [rg]
				drawing.graph = g
				drawing.graphlist = [g]
				drawing.starttobig = False
			drawing.graph.update_layout()
		drawing.Draw(drawing)
		# if event.ready:
		# 	print "DrawGraph 1"
		# else:
		# 	print "DrawGraph 2"
	
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

operations.setmode('lambda')


app = wx.PySimpleApp()
frame = MainWindow()
app.MainLoop()

# destroying the objects, so that this script works more than once in IDLEdieses Beispiel
del frame
del app