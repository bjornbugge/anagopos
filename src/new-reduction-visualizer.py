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
from glgrapharea import MyCubeCanvas
import computegraph.operations as operations
import parser.lambdaparser.lambdaparser as parser

# Drawing algorithms
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph

import sys
import math
import random
from os import getcwd
from os import environ as osenviron
# import wx

MACPORTS_PATH = "/opt/local/bin:/opt/local/sbin"
FINK_PATH = "/sw/bin"

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
                self, parent, id, title, size = (1200,768),
                style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE
        )
        
        # Hack! Add the extra path so the application knows where to find the 
        # GraphViz binaries when run with a "double click" (in which case the
        # path set in .profile isn't used).
        osenviron['PATH'] = osenviron['PATH'] + ":" + MACPORTS_PATH + ":" + FINK_PATH
        #graph = None
        self.drawing = MyCubeCanvas(self)
        # drawing = GraphArea(graph)
        self.drawing.ready = False
        self.drawing.shownewestedget = False
        
        # Create the radio buttons to select between lambda calculus and TRS.
        self.radio_lambda = wx.RadioButton(self, -1, 'Lambda', style = wx.RB_GROUP)
        self.radio_trs = wx.RadioButton(self, -1, 'TRS')
        self.Bind(wx.EVT_RADIOBUTTON, self.SetRadioVal, id = self.radio_lambda.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.SetRadioVal, id = self.radio_trs.GetId())
        self.active_rule_file_text = wx.StaticText(self, -1, 'Rule set: N/A')
        radio_box = wx.BoxSizer(wx.HORIZONTAL)
        radio_box.Add(self.radio_lambda, 0, wx.ALIGN_LEFT, 10)
        radio_box.Add(self.radio_trs, 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        self.radio_lambda.SetValue(True) # Lambda is default active
        self.radio_trs.SetToolTip(wx.ToolTip("Select 'File > Load Rule Set' to activate TRS mode."))
        # self.radio_trs.Disable()
        
        # Buttons
        self.term_input = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE)
        self.draw_button = wx.Button(self, 0, "Draw Graph",         size = (200, 30))
        self.random_button = wx.Button(self, 0, "Random Lambda term", size = (200, 30))
        self.forward_button = wx.Button(self, 0, "Forward", size = (140, 30))
        self.back_button = wx.Button(self, 0, "Back",       size = (140, 30))
        self.redraw_button = wx.Button(self, 0, "Redraw Graph",       size = (200, 30))
        self.optimize_button = wx.Button(self, 0, "Optimize Graph",     size = (200, 30))
        algo_label = wx.StaticText(self, -1, 'Select Drawing Alg: ', (5, 5))
        self.algo_combo = wx.ComboBox(self, -1, size=(200, -1), choices = [k for (k,v) in algorithms.iteritems()], style = wx.CB_READONLY)
        self.start_checkbox = wx.CheckBox(self, -1, 'Start')
        term_label = wx.StaticText(self, -1, 'Clicked Term: ', (5, 5))
        self.term_text = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE|wx.TE_READONLY)
        output_label = wx.StaticText(self, -1, 'Output: ', (5, 5))
        self.status_text = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE|wx.TE_READONLY)
        
        # Spinners (for choosing step size)
        self.forward_spinner = wx.SpinCtrl(self, -1, "1", min = 1, max = 100, initial = 1, size = (60, 30))
        forward_box = wx.BoxSizer(wx.HORIZONTAL)
        forward_box.Add(self.forward_button, 0, wx.ALIGN_LEFT, 10)
        forward_box.Add(self.forward_spinner, 0, wx.ALIGN_RIGHT, 10)
        self.back_spinner = wx.SpinCtrl(self, -1, "1", min = 1, max = 100, initial = 1, size = (60, 30))
        back_box = wx.BoxSizer(wx.HORIZONTAL)
        back_box.Add(self.back_button, 0, wx.ALIGN_LEFT, 10)
        back_box.Add(self.back_spinner, 0, wx.ALIGN_RIGHT, 10)
        
        # Button actions
        self.draw_button.Bind(wx.EVT_BUTTON, self.DrawGraph)
        self.random_button.Bind(wx.EVT_BUTTON, self.Generate)
        self.forward_button.Bind(wx.EVT_BUTTON, self.drawing.Forward)
        self.back_button.Bind(wx.EVT_BUTTON, self.drawing.Back)
        self.redraw_button.Bind(wx.EVT_BUTTON, self.drawing.Redraw)
        self.optimize_button.Bind(wx.EVT_BUTTON, self.drawing.Optimize)
        self.algo_combo.Bind(wx.EVT_COMBOBOX, self.NewAlgoSelected)
        
        # self.Bind(wx.EVT_LEFT_DOWN, self.drawing.OnMouseDown)
        # self.Bind(wx.EVT_LEFT_UP, self.drawing.OnMouseUp)
        # self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        # self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        # self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        
        
        bts = wx.BoxSizer(wx.VERTICAL)
        bts.Add(radio_box, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        bts.Add(self.active_rule_file_text, 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        bts.Add(self.term_input, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        bts.Add(self.draw_button, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(self.random_button, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        # bts.Add(self.forward_button, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(forward_box, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        # bts.Add(self.back_button, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(back_box, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(self.redraw_button, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(self.optimize_button, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(algo_label, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(self.algo_combo, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(self.start_checkbox, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(term_label, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(self.term_text, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(output_label, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(self.status_text, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        
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
        
        # Filemenu - Open
        menuitem = filemenu.Append(-1, "&Load Rule Set", "Load a TRS rule set")
        self.Bind(wx.EVT_MENU, self.OnLoadRuleSet, menuitem) # Event handler
        
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
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)

        # Show
        self.Show(True)
        
        self.dirname = getcwd() + '/parser' # From 'os'
        self.rule_set = None # Used for the TRS
        self.last_used_rule_set = None
        self.last_used_rule_name = ""

    def OnAbout(self,event):
        message = "Reduction Visualizer\n\nURL:\nhttp://code.google.com/p/reduction-visualizer/\n\nBy:\n Niels Bjoern Bugge Grathwohl\n Jens Duelund Pallesen"
        caption = "Reduction Visualizer"
        wx.MessageBox(message, caption, wx.OK)
    
    def OnLoadRuleSet(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetPath()
            rulename = dlg.GetFilename()
            suffix = name[-3:]
            if suffix == 'trs':
                print "Opened a .trs file: " + name
            elif suffix == 'xml':
                print "Opened an XML file: " + name
            else:
                print "Unrecognized file format: " + name
                return
            
            operations.setmode('trs')
            # self.radio_trs.Enable(True)
            self.radio_trs.SetValue(True)
            self.radio_lambda.SetValue(False)
            self.UpdateRuleInfo(rulename)
            
            with open(name, 'r') as f:
                contents = f.read()
            
            ruleset = operations.parse_rule_set(suffix, contents)
            self.rule_set = self.last_used_rule_set = ruleset
            self.last_used_rule_name = rulename
            print "GOT RULE SET: " + str(ruleset)
    
    def SetRadioVal(self, event):
        if self.radio_lambda.GetValue():
            operations.setmode('lambda')
            self.rule_set = None
            self.UpdateRuleInfo("N/A")
        else:
            if self.last_used_rule_set == None:
                self.OnLoadRuleSet(True)
            else:
                self.rule_set = self.last_used_rule_set
                self.UpdateRuleInfo(self.last_used_rule_name)
            operations.setmode('trs')
    
    def UpdateRuleInfo(self, text):
        self.active_rule_file_text.SetLabel("Rule Set: " + text)
    
    def OnExit(self,event):
        self.Close(True)
    
    def OnMouseDown(self, evt):
        print "mouse down"
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
        print self.x
        print self.y
    
    def OnMouseUp(self, evt):
        print  "mouse up"
        self.term_text.SetValue(self.drawing.nodetest)
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
        print self.x
        print self.y
        self.ReleaseMouse()
    
    def OnMouseMotion(self, evt):
        print "mouse moving"
        # if evt.Dragging() and evt.LeftIsDown():
        #   self.lastx, self.lasty = self.x, self.y
        #   self.x, self.y = evt.GetPosition()
        #   self.Refresh(False)
    
    
    def DrawGraph(self, drawing):
        Drawer = algorithms[self.algo_combo.GetValue()]
        print Drawer
        self.drawing.selected = Drawer
        if True:
            print self.term_input.GetValue()
            self.drawing.ready = True
            self.drawing.startnum = 0
            self.drawing.endnum = 1000000
            tempterm = self.term_input.GetValue()
            # tempterm = "(#B1.(((B1 #B2.(#B3.(#B4.(B4)))) #B5.(#B6.(#B7.((((B7 B5) #B8.(#B9.(B5))) B7)))))) #B10.(#B11.(((((#B12.(B11) (#B13.(B11) #B14.((B10 B11)))) (B11 B10)) ((#B15.(#B16.(#B17.(#B18.(#B19.(B11))))) #B20.((#B21.(B20) #B22.(#B23.((#B24.(#B25.(B20)) B23)))))) F1)) (#B26.(#B27.(B27)) #B28.(#B29.(#B30.(#B31.(#B32.(B30))))))))))"
            #tempterm = "#B1.(#B2.(#B3.(B1)))"
            self.drawing.term = operations.parse(tempterm.replace(u'\u03bb',"#"))
            self.drawing.mgs = []
            operations.assignvariables(self.drawing.term)
            # self.drawing.selected = NeatoGraph
            self.drawing.startnumber = 1
            try:
                def iterator():
                    Drawer = self.drawing.selected
                    for (i,g) in enumerate(operations.reductiongraphiter(self.drawing.term, self.drawing.startnum, self.drawing.endnum, self.rule_set)):
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
            
            self.drawing.graph.update_layout_animated(self.drawing.iter_animated)
        
        self.drawing.Draw()
    
    def NewAlgoSelected(self, event):
        if hasattr(self.drawing, 'ready') and self.drawing.ready:
            self.drawing.selectedhaschanged = True
            Drawer = algorithms[self.algo_combo.GetValue()]
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