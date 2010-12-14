# -*- coding: utf-8 -*-
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
import pdb
import pickle
from glgrapharea import ReductionGraphCanvas
import computegraph.operations as operations
import parser.lambdaparser.lambdaparser as parser
import computegraph.lambda_randomgraph as lambda_randomgraph

# Drawing algorithms
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph

import colors

import sys
import math
import random
from os import getcwd
from os import environ as osenviron
from pyparsing import ParseException

MACPORTS_PATH = "/opt/local/bin:/opt/local/sbin"
FINK_PATH = "/sw/bin"

algorithms = {'Neato' : NeatoGraph,
            'Neato Animated' : MajorizationGraph,
            'Dot' : DotGraph,
            'TwoPi' : TwopiGraph,
            'Circo' : CircoGraph,
            'Fdp' : FdpGraph}

TERM_PARSE_ERROR_COLOUR = "#BB4444"

VERSION = "0.1"

class State(object):
    def __init__(self):
        self.save_dir = osenviron['HOME']
        self.rule_dir = osenviron['HOME']
        self.color_scheme = 'black'
    def __repr__(self):
        return self.save_dir + " " + self.rule_dir + " " + self.color_scheme

class MainWindow(wx.Frame):
    
    def __init__(self, parent = None, id = -1, title = "Reduction Visualizer"):
        wx.Frame.__init__(
                self, parent, id, title, size = (1200, 768),
                style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE
        )
        
        # Hack! Add the extra path so the application knows where to find the 
        # GraphViz binaries when run with a "double click" (in which case the
        # path set in .profile isn't used).
        osenviron['PATH'] = osenviron['PATH'] + ":" + MACPORTS_PATH + ":" + FINK_PATH
        
        self.load_state()
        
        self.drawing = ReductionGraphCanvas(self)
        self.drawing.ready = False
        
        # Create the radio buttons to select between lambda calculus and TRS.
        self.radio_lambda = wx.RadioButton(self, -1, 'Lambda', style = wx.RB_GROUP)
        self.radio_trs = wx.RadioButton(self, -1, 'TRS')
        self.Bind(wx.EVT_RADIOBUTTON, self.SetRadioVal, id = self.radio_lambda.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.SetRadioVal, id = self.radio_trs.GetId())
        self.active_rule_file_text = wx.StaticText(self, -1, 'Rule set: N/A')
        radio_box = wx.BoxSizer(wx.HORIZONTAL)
        radio_box.Add(self.radio_lambda, 0, wx.ALIGN_LEFT, 10)
        radio_box.Add(self.radio_trs, 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        self.radio_lambda.SetValue(True)    # Lambda is by default active
        self.radio_trs.SetToolTip(wx.ToolTip("Select 'File > Load Rule Set' to activate TRS mode."))
        
        width = 200
        spinner_width = 60
        button_size = (width, -1)
        step_size = (width - spinner_width, -1)
        # Buttons
        self.term_input = wx.TextCtrl(self, 0, style = wx.TE_MULTILINE, size = (width, 100))
        draw_button     = wx.Button(self, 0, "Draw Graph",         size = button_size)
        self.random_button = wx.Button(self, 0, "Random Lambda term", size = button_size)
        forward_button  = wx.Button(self, 0, "Forward",            size = step_size)
        back_button     = wx.Button(self, 0, "Back",               size = step_size)
        redraw_button   = wx.Button(self, 0, "Redraw Graph",       size = button_size)
        optimize_button = wx.Button(self, 0, "Optimize Graph",     size = button_size)
        algo_label      = wx.StaticText(self, -1, 'Select Drawing Alg: ', (5, 5))
        self.algo_combo = wx.ComboBox(self, -1, size = (width, -1), choices = [k for (k,v) in algorithms.iteritems()], style = wx.CB_READONLY)
        
        term_label      = wx.StaticText(self, -1, 'Clicked Term: ')
        term_text  = wx.TextCtrl(self, -1, size = (width, 150), style = wx.TE_MULTILINE | wx.TE_READONLY)

        def node_click_callback(node):
            term_text.SetValue("" + str(node)[5:])
        self.drawing.node_clicked = node_click_callback
        
        start_checkbox  = wx.CheckBox(self, -1, 'Show start')
        newest_checkbox = wx.CheckBox(self, -1, 'Show newest')
        
        # Spinners (for choosing step size)
        self.forward_spinner = wx.SpinCtrl(self, -1, "1", min = 1, max = 100, initial = 1, size = (spinner_width, -1))
        forward_box = wx.BoxSizer(wx.HORIZONTAL)
        forward_box.Add(forward_button, 0, wx.ALIGN_LEFT, 10)
        forward_box.Add(self.forward_spinner, 0, wx.ALIGN_RIGHT, 10)
        self.back_spinner = wx.SpinCtrl(self, -1, "1", min = 1, max = 100, initial = 1, size = (spinner_width, -1))
        back_box = wx.BoxSizer(wx.HORIZONTAL)
        back_box.Add(back_button, 0, wx.ALIGN_LEFT, 10)
        back_box.Add(self.back_spinner, 0, wx.ALIGN_RIGHT, 10)
        
        # Button/spinner actions
        draw_button.Bind(wx.EVT_BUTTON, self.DrawGraph)
        self.random_button.Bind(wx.EVT_BUTTON, self.Generate)
        forward_button.Bind(wx.EVT_BUTTON, self.drawing.Forward)
        back_button.Bind(wx.EVT_BUTTON, self.drawing.Back)
        redraw_button.Bind(wx.EVT_BUTTON, self.drawing.Redraw)
        optimize_button.Bind(wx.EVT_BUTTON, self.drawing.Optimize)
        self.algo_combo.Bind(wx.EVT_COMBOBOX, self.NewAlgoSelected)
        self.forward_spinner.Bind(wx.EVT_SPINCTRL, self.forward_spin)
        self.back_spinner.Bind(wx.EVT_SPINCTRL, self.back_spin)
        start_checkbox.Bind(wx.EVT_CHECKBOX, self.drawing.ToggleShowStart)
        newest_checkbox.Bind(wx.EVT_CHECKBOX, self.drawing.ToggleShowNewest)
        
        # Layout the control panel
        bts = wx.BoxSizer(wx.VERTICAL)
        bts.Add(radio_box, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        bts.Add(self.active_rule_file_text, 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        bts.Add(self.term_input, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        bts.Add(draw_button, 0, wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM, 3)
        bts.Add(self.random_button, 0, wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM, 3)
        bts.Add(forward_box, 0, wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM, 3)
        bts.Add(back_box, 0, wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM, 3)
        bts.Add(redraw_button, 0, wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM, 3)
        bts.Add(optimize_button, 0, wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM, 3)
        bts.Add(algo_label, 0, wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM, 3)
        bts.Add(self.algo_combo, 0, wx.ALIGN_CENTER | wx.LEFT | wx.BOTTOM, 10)
        bts.Add(start_checkbox, 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        bts.Add(newest_checkbox, 0, wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, 10)
        bts.Add(term_label, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        bts.Add(term_text, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        
        # Layout the whole window frame
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(bts, 0, wx.ALIGN_TOP, 15)
        box.Add(self.drawing, 1, wx.EXPAND)
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        
        self.CreateStatusBar()
        
        def status_bar_callback(grapharea):
            s = "Number of nodes: " + str(len(grapharea.graph.nodes)) + "."
            
            if hasattr(grapharea, 'nomoregraphs') and grapharea.nomoregraphs:
                s += " No more graphs."
            self.SetStatusText(s)
        
        self.drawing.output_graph_status = status_bar_callback
        
        # Menus
        filemenu = wx.Menu()
        color_scheme_menu = wx.Menu()
        
        # Menu actions
        menuitem = filemenu.Append(-1, "&Save Image\tCtrl+S", "Take a screenshot")
        self.Bind(wx.EVT_MENU, self.OnScreenshot, menuitem)
        menuitem = filemenu.Append(-1, "&Open Rule Set\tCtrl+O", "Load a TRS rule set")
        self.Bind(wx.EVT_MENU, self.OnLoadRuleSet, menuitem)
        
        self.color_scheme_black = color_scheme_menu.AppendRadioItem(-1, "Black Funk\tCtrl+1")
        self.Bind(wx.EVT_MENU, self.OnColorSchemeChange, self.color_scheme_black)
        self.color_scheme_white = color_scheme_menu.AppendRadioItem(-1, "White Snow\tCtrl+2")
        self.Bind(wx.EVT_MENU, self.OnColorSchemeChange, self.color_scheme_white)
        self.color_scheme_grey = color_scheme_menu.AppendRadioItem(-1, "Grey Dawn\tCtrl+3")
        self.Bind(wx.EVT_MENU, self.OnColorSchemeChange, self.color_scheme_grey)
        filemenu.AppendMenu(-1, "Color Schemes", color_scheme_menu)
        
        menuitem = filemenu.Append(-1, "&About", "About")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuitem)
        filemenu.AppendSeparator()
        menuitem = filemenu.Append(-1, "E&xit", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, menuitem)
        
        # Menubar, containg the menu(s) created above
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)
        
        self.lambda_contents = self.trs_contents = ""
        
        self.rule_set = None # Used for the TRS
        self.last_used_rule_set = None
        self.last_used_rule_name = ""
        
    
    def load_state(self):
        s = getcwd() + "/state.dat"
        try:
            f = open(s, 'r')
        except IOError:
            f = file(s, 'w')
        finally:
            f.close()
        
        with file(s, 'r') as statefile:
            c = statefile.read()
            if not c == '':
                statefile.seek(0)
                self.state = pickle.load(statefile)
            else:
                self.state = State()
        
        if self.state.color_scheme == 'black':
            colors.set_color_scheme_black()
        elif self.state.color_scheme == 'white':
            colors.set_color_scheme_white()
        elif self.state.color_scheme == 'grey':
            colors.set_color_scheme_grey()
    
    def save_state(self):
        with file(getcwd() + "/state.dat", 'w') as statefile:
            pickle.dump(self.state, statefile)
        print "Saved state: " + str(self.state)

    def OnAbout(self,event):
        message = "Reduction Visualizer " + VERSION + "\n\n"
        message += "URL:\nhttp://code.google.com/p/reduction-visualizer/\n\n"
        message += "By:\n Niels Bjørn Bugge Grathwohl\n Jens Duelund Pallesen"
        caption = "Reduction Visualizer"
        wx.MessageBox(message, caption, wx.OK)
    
    def OnLoadRuleSet(self, event):
        dlg = wx.FileDialog(self, "Open Rule Set", self.state.rule_dir, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetPath()
            rulename = dlg.GetFilename()
            self.state.rule_dir = name[:name.index(rulename) - 1]
            suffix = name[-3:]
            if not (suffix == 'trs' or suffix == 'xml'):
                print "Unrecognized file format: " + name
                return
            
            operations.setmode('trs')
            self.radio_trs.SetValue(True)
            self.radio_lambda.SetValue(False)
            self.UpdateRuleInfo(rulename)
            
            with open(name, 'r') as f:
                contents = f.read()
            
            ruleset = operations.parse_rule_set(suffix, contents)
            self.rule_set = self.last_used_rule_set = ruleset
            self.last_used_rule_name = rulename
            self.SetRadioVal(None)
            self.save_state()
    
    def OnColorSchemeChange(self, event):
        if self.color_scheme_black.IsChecked():
            colors.set_color_scheme_black()
            self.state.color_scheme = 'black'
        elif self.color_scheme_grey.IsChecked():
            colors.set_color_scheme_grey()
            self.state.color_scheme = 'grey'
        else:
            colors.set_color_scheme_white()
            self.state.color_scheme = 'white'
        self.save_state()
        self.drawing.Draw()
        
    
    def SetRadioVal(self, event):
        if self.radio_lambda.GetValue():
            operations.setmode('lambda')
            self.rule_set = None
            self.UpdateRuleInfo("N/A")
            self.trs_contents = self.term_input.GetValue()
            self.term_input.SetValue(self.lambda_contents)
            self.random_button.Enable(True)
        else:
            if self.last_used_rule_set == None:
                self.OnLoadRuleSet(True)
            else:
                self.rule_set = self.last_used_rule_set
                self.UpdateRuleInfo(self.last_used_rule_name)
            self.random_button.Enable(False)
            self.lambda_contents = self.term_input.GetValue()
            self.term_input.SetValue(self.trs_contents)
            operations.setmode('trs')
    
    def UpdateRuleInfo(self, text):
        self.active_rule_file_text.SetLabel("Rule Set: " + text)
    
    def OnExit(self,event):
        self.Close(True)
    
    def DrawGraph(self, drawing):
        Drawer = algorithms[self.algo_combo.GetValue()]
        self.drawing.selected = Drawer
        self.drawing.ready = True
        self.drawing.startnum = 0
        self.drawing.endnum = 1000000
        term = self.term_input.GetValue()
        try:
            self.drawing.term = operations.parse(term.replace(u'\u03bb',"#"))
        except (ParseException, UnboundLocalError):
            # The TRS parser throws ParseException when it fails.
            # The lambda parser hasn't got any specific parse exception,
            # but it throws UnboundLocalError at failure. It's an artefact of Yapps.
            self.term_input.SetBackgroundColour(TERM_PARSE_ERROR_COLOUR)
            return
        self.term_input.SetBackgroundColour("#FFFFFF")
        self.drawing.mgs = []
        operations.assignvariables(self.drawing.term)
        self.drawing.startnumber = 1
        try:
            def iterator():
                Drawer = self.drawing.selected
                for (i,g) in enumerate(operations.reductiongraphiter(self.drawing.term, self.drawing.startnum, self.drawing.endnum, self.rule_set)):
                    yield g
            self.drawing.iterator = iterator()
        except KeyError:
            pass
        
        rg = self.drawing.iterator.next()
        g = Drawer(rg)
        self.drawing.reductiongraphlist = [rg]
        self.drawing.graph = g
        self.drawing.graphlist = [g]
        self.drawing.graphnumber = 0
        self.drawing.nomoregraphs = False
        self.drawing.starttobig = False
        
        self.drawing.graph.update_layout_animated(self.drawing.iter_animated)
        
        # self.drawing.Draw()
    
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
    
    def Generate(self, event):
        g = lambda_randomgraph.randomterm()
        self.term_input.SetValue("" + str(g))
    
    def OnScreenshot(self, event):
        dlg = wx.FileDialog(self, "Save Screenshot", self.state.save_dir, "", "*.*", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetPath()
            filename = dlg.GetFilename()
            self.state.save_dir = name[:name.index(filename) - 1]
            self.drawing.export_canvas(name)
            self.save_state()
    
    def forward_spin(self, event):
        self.drawing.set_forward_step_size(self.forward_spinner.GetValue())
    
    def back_spin(self, event):
        self.drawing.set_back_step_size(self.back_spinner.GetValue())

operations.setmode('lambda')

app = wx.PySimpleApp()
frame = MainWindow()
frame.Show(True)
app.MainLoop()

del frame
del app