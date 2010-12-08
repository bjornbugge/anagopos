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

import pdb

import sys
import math
import random
import time
import os
import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
import computegraph.operations as operations

# Drawing algorithms
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph

class ReductionGraphCanvas(glcanvas.GLCanvas):
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
        
        self.forward_step_size = 1
        self.back_step_size = 1
        self.show_start_node = False
        self.show_newest_node = False
        
        # When clicking on nodes, this is the widget that should be updated.
        self.node_text_widget = None
    
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
    
    def iter_animated(self):
        self.Draw()
    
    def OnMouseDown(self, event):
        if not self.ready:
            return
        
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = event.GetPosition()
        propX = float(self.x) / float(self.GetSize()[0])
        propY = float(self.y) / float(self.GetSize()[1])
        scX = self.orthoRight - self.orthoLeft
        scY = self.orthoBottom - self.orthoTop
        
        X = propX * scX
        Y = propY * scY
        
        rX = 20 / float(self.GetSize()[0]) * scX
        rY = 20 / float(self.GetSize()[1]) * scY
        
        for node in self.graph.nodes:
            nX = node.x - self.orthoLeft
            nY = node.y - self.orthoTop
            
            if (X > (nX - rX)) and (X < (nX + rX)) and (Y > (nY - rY)) and (Y < (nY + rY)):
                self.graph.dragnode = True
                self.graph.dragnodename = node.name
                self.graph.dragnodex = self.x
                self.graph.dragnodey = self.y
                # Cut the first 5 chars. They are "NODE ".
                self.node_text_widget.SetValue("" + str(node)[5:])
            else:
                self.graph.dragnode = False
    
    def OnMouseUp(self, event):
        if hasattr(self.graph, 'dragnode') and self.graph.dragnode:
            x = self.x
            y = self.y
            self.x, self.y = event.GetPosition()
            self.lastx, self.lasty = x, y
            if (y != self.y) or (x != self.x):
                print "you are trying to drag node: " + self.graph.dragnodename
                print "new pixel coordinates: (" + str(self.x) + "," + str(self.y) + ")"
                print "new gviz coordinates:  (" + str(self.x) + "," + str(self.y) + ")"
                self.nodetext = ""
            else:
                print "you have clicked node " + self.graph.dragnodename
        
        if self.HasCapture():
            self.ReleaseMouse()
    
    def OnMouseMotion(self, event):
        # TODO Does not work!
        if event.Dragging() and event.LeftIsDown() and False:
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = event.GetPosition()
            self.Refresh(False)
    
    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        Xs = [node.x for node in self.graph.nodes]
        Ys = [node.y for node in self.graph.nodes]
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.orthoLeft = min(Xs) - max(Xs) * 0.02
        self.orthoRight = max(Xs) + max(Xs) * 0.02
        self.orthoBottom = max(Ys) + max(Ys) * 0.02
        self.orthoTop = min(Ys) - max(Ys) * 0.02
        self.orthoDiagonal = self.orthoRight + self.orthoBottom
                    
        gluOrtho2D(self.orthoLeft, self.orthoRight, self.orthoBottom, self.orthoTop)
        glMatrixMode(GL_MODELVIEW)
        
        for node in self.graph.nodes:
            for edge in node.children:
                if hasattr(self.graph, 'bezier') and self.graph.bezier:
                    (x1, y1, x2, y2) = draw_bezier_edge(node, edge)
                else:
                    far_node = edge.get_far(node)
                    (x1, y1, x2, y2) = (node.x, node.y, far_node.x, far_node.y)
                    draw_regular_line(x1, y1, x2, y2)
                
                radius = self.orthoDiagonal
                if node != edge.get_far(node):
                    # FIXME These arrows are hideous!!!!!
                    
                    draw_arrowhead(x1, y1, x2, y2, radius/150, self.orthoDiagonal/230, 1.0, 15)
                    # self.draw_arrowhead(x1, y1, x2, y2, radius/160, self.orthoDiagonal/220, 0.9, 16)
                    draw_arrowhead(x1, y1, x2, y2, radius/170, self.orthoDiagonal/210, 0.8, 17)
                    # self.draw_arrowhead(x1, y1, x2, y2, radius/180, self.orthoDiagonal/200, 0.7, 18)
                    draw_arrowhead(x1, y1, x2, y2, radius/190, self.orthoDiagonal/190, 0.6, 19)
                    # self.draw_arrowhead(x1, y1, x2, y2, radius/200, self.orthoDiagonal/180, 0.5, 20)
                    draw_arrowhead(x1, y1, x2, y2, radius/210, self.orthoDiagonal/170, 0.4, 21)
                    # self.draw_arrowhead(x1, y1, x2, y2, radius/220, self.orthoDiagonal/160, 0.3, 22)
                    draw_arrowhead(x1, y1, x2, y2, radius/230, self.orthoDiagonal/150, 0.1, 23)
        
        for node in self.graph.nodes:
            if len(node.term.redexpositions) == 0:
                draw_nf_node(node.x, node.y)
            elif node.name == "N0" and self.show_start_node:
                draw_start_node(node.x, node.y)
            elif (node is self.graph.newest) and self.show_newest_node:
                draw_newest_node(node.x, node.y)
            else:
                draw_regular_node(node.x, node.y)
        
        self.SwapBuffers()
    
    def set_forward_step_size(self, s):
        if s < 1 or s > 100:
            return
        self.forward_step_size = s
        
    def set_back_step_size(self, s):
        if s < 1 or s > 100:
            return
        self.back_step_size = s
    
    def Forward(self, event):
        Drawer = self.selected
        self.firstgraph = False
        if hasattr(self, 'nomoregraphs') and self.nomoregraphs:
            c = 0
        else:
            c = self.forward_step_size
        if self.graphnumber + c < len(self.graphlist):
            self.graphnumber += self.forward_step_size
            if self.graphnumber > len(self.graphlist):
                self.graphnumber = len(self.graphlist) - 1
            if hasattr(self, 'selectedhaschanged') and self.selectedhaschanged:
                rg = self.reductiongraphlist[self.graphnumber]
                g = Drawer(rg)
                self.graphlist[self.graphnumber] = g
                self.graph = g
                self.graph.initwith(self.graphlist[self.graphnumber - 1])
                self.graph.update_layout()
            else:
                self.graph = self.graphlist[self.graphnumber]
                self.graph.initwith(self.graphlist[self.graphnumber - 1])
                self.graph.update_layout()
        else:
            i = 0
            rg = None
            g = None
            try:
                while i < self.forward_step_size:
                    rg = self.iterator.next()
                    g = Drawer(rg)
                    self.reductiongraphlist.append(rg)
                    self.graphlist.append(g)
                    i += 1
            except StopIteration:
                self.nomoregraphs = True
                print "No more graphs"
            
            if i > 0:
                self.graphnumber += i
                self.graph = self.graphlist[self.graphnumber]
                if type(self.graph) is type(self.graphlist[self.graphnumber - 1]):
                    self.graph.initwith(self.graphlist[self.graphnumber - 1])
                self.graph.update_layout_animated(self.iter_animated)
        
        self.Draw()
    
    def Back(self, event):
        Drawer = self.selected
        if self.graphnumber == 0:
            self.firstgraph = True
        else:
            self.firstgraph = False
            self.graphnumber -= self.back_step_size
            if self.graphnumber < 0:
                self.graphnumber = 0
            if hasattr(self, 'selectedhaschanged') and self.selectedhaschanged:
                rg = self.reductiongraphlist[self.graphnumber]
                g = Drawer(rg)
                self.graphlist[self.graphnumber] = g
                self.graph = g
                self.graph.initwith(self.graphlist[self.graphnumber + 1])
                self.graph.update_layout_animated(self.iter_animated)
            else:
                self.graph = self.graphlist[self.graphnumber]
                self.graph.update_layout_animated(self.iter_animated)
        
        self.Draw()
    
    def Redraw(self, event):
        if self.ready:
            self.graph.reset()
            self.graph.update_layout_animated(self.iter_animated)
            self.Draw()
        else:
            print "No graph created yet!"
        
    def Optimize(self, event):
        if self.ready:
            self.graph.update_layout_animated(self.iter_animated)
            self.Draw()
        else:
            print "No graph created yet!"
    
    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.SwapBuffers()
    
    def ToggleShowStart(self, event):
        self.show_start_node = not self.show_start_node
        if self.ready:
            self.Draw()
    
    def ToggleShowNewest(self, event):
        self.show_newest_node = not self.show_newest_node
        if self.ready:
            self.Draw()


##############################################################################
# Drawing functions for edges, nodes, etc.
##############################################################################

def draw_node(x, y, sizes, colors):
    '''
    Draw a node at the given position using max(len(sizes), len(colors))
    points having the specified sizes and colors.
    '''
    if not len(sizes) == len(colors):
        print "Size and colour count for node drawer not equal. Adjusting."
        align_lists(sizes, colors)
    
    for i, size in enumerate(sizes):
        color = colors[i]
        
        glPointSize(size)
        glColor4f(color[0], color[1], color[2], color[3])
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

def draw_line(x1, y1, x2, y2, widths, colors):
    '''
    Draw a line between the two given points using max(len(widths), len(colors))
    primitive lines with the specified widths and colors.
    '''
    if not len(widths) == len(colors):
        print "Width and colour count for node drawer not equal. Adjusting."
        align_lists(widths, colors)
    
    for i, width in enumerate(widths):
        color = colors[i]
        
        glLineWidth(width)
        glColor4f(color[0], color[1], color[2], color[3])
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

def draw_regular_node(x, y):
    sizes = [15, 13, 11, 9, 7, 5]
    colors = [(0.3, 0.6, 1.0, 0.1), (0.3, 0.6, 1.0, 0.2), (0.3, 0.6, 1.0, 0.4),
              (0.3, 0.6, 1.0, 0.6), (0.3, 0.6, 1.0, 0.8), (0.3, 0.6, 1.0, 1.0)]
    draw_node(x, y, sizes, colors)

def draw_start_node(x, y):
    sizes = [15, 13, 11, 9, 7, 5]
    colors = [(0.5, 0.8, 1.0, 0.1), (0.5, 0.8, 1.0, 0.2), (0.5, 0.8, 1.0, 0.4),
              (0.5, 0.8, 1.0, 0.6), (0.5, 0.8, 1.0, 0.8), (0.5, 0.8, 1.0, 1.0)]
    draw_node(x, y, sizes, colors)

def draw_nf_node(x, y):
    sizes = [17, 15, 13, 11, 9, 7]
    colors = [(1.0, 0.0, 0.0, 0.1), (1.0, 0.0, 0.0, 0.2), (1.0, 0.0, 0.0, 0.4),
              (1.0, 0.0, 0.0, 0.6), (1.0, 0.0, 0.0, 0.8), (1.0, 0.0, 0.0, 1.0)]
    draw_node(x, y, sizes, colors)

def draw_newest_node(x, y):
    sizes = [15, 13, 11, 9, 7, 5]
    colors = [(0.0, 1.0, 1.0, 0.1), (0.0, 1.0, 1.0, 0.2), (0.0, 1.0, 1.0, 0.4),
              (0.0, 1.0, 1.0, 0.6), (0.0, 1.0, 1.0, 0.8), (0.0, 1.0, 1.0, 1.0)]
    draw_node(x, y, sizes, colors)

def draw_regular_line(x1, y1, x2, y2):
    widths = [4.5, 3.5, 2.5, 1.5, 0.8, 0.5]
    colors = [(0.3, 0.9, 0.2, 0.1), (0.3, 0.9, 0.2, 0.2), (0.3, 0.9, 0.2, 0.4),
              (0.3, 0.9, 0.2, 0.6), (0.3, 0.9, 0.2, 0.3), (0.3, 0.9, 0.2, 1.0)]
    
    draw_line(x1, y1, x2, y2, widths, colors)

def draw_bezier_edge(node, edge):
    far_node = edge.get_far(node)
    if edge.destination == node:
        return
    
    destX = edge.destination.x
    destY = edge.destination.y
    
    lastX = edge.ipoints[len(edge.ipoints) - 1][0]
    lastY = edge.ipoints[len(edge.ipoints) - 1][1]
    
    if node.y != edge.ipoints[0][1] or node.x != edge.ipoints[0][0]:
        draw_regular_line(node.x, node.y, edge.ipoints[0][0], edge.ipoints[0][1])
    if destY != lastY or destX != lastX:
        draw_regular_line(far_node.x, far_node.y, lastX, lastY)
    
    POld = [edge.ipoints[0][0], edge.ipoints[0][1]]
    t = 0.00
    l = len(edge.ipoints)
    for g in xrange(101):
        P = calculate_bezier_points(t, l, edge.ipoints)
        draw_regular_line(POld[0], POld[1], P[0], P[1])
        POld = P
        t = t + 0.01
    x1 = edge.ipoints[len(edge.ipoints) - 1][0]
    y1 = edge.ipoints[len(edge.ipoints) - 1][1]
    return (x1, y1, far_node.x, far_node.y)
    

def draw_arrowhead(x1, y1, x2, y2, noderadius, arrowwidth, transparency, angle):
    '''
    Draws an arrow head on the line segment between the coordinate pairs
    (x1,y1) and (x2,y2). The arrow head is placed in the (x2,y2)-end.
    '''
    if x1 - x2 == 0:
        if y2 <= y1:
            LineAngle = math.pi / 2
        else:
            LineAngle = 3 * math.pi / 2
    else:
        LineAngle = math.atan((y2 - y1) / (x2 - x1))

    EndAngle1 = LineAngle + angle * math.pi/180
    EndAngle2 = LineAngle - angle * math.pi/180

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
    
    # TODO Do we need these again? (InitGL())
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

##############################################################################
# Miscellaneous helper functions.
##############################################################################

def binomial(n, i):
    bin = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
    return bin

def calculate_bezier_points(t, l, ipoints):
    n = l - 1
    fun = lambda a, b:a + b
    x = reduce(fun, (binomial(n, i) * pow((1 - t), n - i) * pow(t, i) * ipoints[i][0] for i in xrange(l)))
    y = reduce(fun, (binomial(n, i) * pow((1 - t), n - i) * pow(t, i) * ipoints[i][1] for i in xrange(l)))
    return [x, y]

def align_lists(l1, l2):
    if len(l1) < len(l2):
        l1[len(l1) - 1:len(l2)] = l1[len(l1) - 1]
    elif len(l2) > len(l1):
        l2[len(l2) - 1:len(l1)] = l2[len(l1) - 1]
