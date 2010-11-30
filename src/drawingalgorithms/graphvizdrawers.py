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

import random
import pygraphviz as pgv
from drawingalgorithm import DrawingAlgorithm

class GraphVizDrawer(DrawingAlgorithm):
    '''
    Common ancestor for the drawing algorithms from GraphViz. 
    '''
    def __init__(self, graph):
        for name, value in vars(graph).iteritems():
            setattr(self, name, value)
        
        self._newagraph()
    
    # Reset node positions
    def reset(self, f = 0):
        for node in self.nodes:
            node.x = random.randint(1, 100)
            node.y = random.randint(1, 100)
        self._newagraph()
    
    # Generates new graph
    def _newagraph(self):
        self.G = pgv.AGraph()
        for name in (n.name for n in self.nodes):
            self.G.add_node(name, width = "0.00", heigth = "0.00", fixedsize = "0", 
                            margin = "0.00")#, label = " ", shape = "none"), fontsize = "8")
        for node in self.nodes:
            for edge in node.children:
                far_node = edge.get_far(node)
                self.G.add_edge(str(node.name), str(far_node.name))
    
    # Initial width of graph
    def initwith(self, othergraph): 
        self.reset()
    
    # Dragging nodes
    def dragnodes(self):
        Npre = self.G.nodes()
        
        # If node is dragged new position will be put into GraphViz graph
        if hasattr(self, 'dragnode') and self.dragnode:
            for Anode in Npre:
                if hasattr(self, 'dragnodename') and Anode.title() == self.dragnodename:
                    newx = self.dragnodex
                    newy = self.dragnodey
                    Anode.attr["pos"]= str(int(newx)) + "," + str(int(newy))
        
        # Updates layout of GraphViz graph with new node position.
        # High epsilon so graph wont change that much
        self.G.layout(prog = self.algorithm, args="-Gepsilon=5000")
        
        N = self.G.nodes()
        
        # Assigns new positions in the GraphViz graph to the "correct" graph
        for Anode in N:
            graphnode = self.nodenametable[Anode.title()]
            graphnode.x, graphnode.y = map(float, Anode.attr["pos"].split(','))
            
            for edge in graphnode.children:
                Aedge = self.G.get_edge(graphnode.name, edge.get_far(graphnode).name)
                newEdgePos = Aedge.attr["pos"].split(' ')
            
                if not hasattr(self, 'bezier') or not self.bezier:
                    continue
                
                edge.ipoints = [[0, 0] for row in range(len(newEdgePos))]
                for i, pos in enumerate(newEdgePos):
                    edge.ipoints[i] = map(float, pos.split(','))
    
    # Updates layout on GraphViz graph
    def update_layout(self):
        self.G.layout(prog = self.algorithm)
        
        N = self.G.nodes()
        
        # Assigns new positions in the GraphViz graph to the "correct" graph
        for Anode in N:
            graphnode = self.nodenametable[Anode.title()]
            graphnode.x, graphnode.y = map(float, Anode.attr["pos"].split(','))
            
            for edge in graphnode.children:
                Aedge = self.G.get_edge(graphnode.name, edge.get_far(graphnode).name)
                newEdgePos = Aedge.attr["pos"].split(' ')
            
                if not hasattr(self, 'bezier') or not self.bezier:
                    continue
                
                edge.ipoints = [[0, 0] for row in range(len(newEdgePos))]
                # pdb.set_trace()
                for i, pos in enumerate(newEdgePos):
                    edge.ipoints[i] = map(float, pos.split(','))
    
    # Updates layout animated
    # Wont work on the GraphViz graphs
    def update_layout_animated(self, f):
        self.update_layout()
        f()
    
    # Scales the node positions to fit the GTK GraphArea
    def scale(self, width, height):
        Xs = [node.x for node in self.nodes]
        Ys = [node.y for node in self.nodes]
        scaling = [max(Xs) / (width - 50), max(Ys) / (height - 50)]
        self.scaling = scaling
        
        for node in self.nodes:
            node.x = float(node.x) / scaling[0]
            node.y = float(node.y) / scaling[1]
            
            if not hasattr(self, 'bezier') or not self.bezier:
                continue
            
            for edge in node.children:
                for i, point in enumerate(edge.ipoints):
                    edge.ipoints[i] = map(lambda x:float(x[0]) / x[1], zip(point, scaling))
        
        return scaling


class CircoGraph(GraphVizDrawer):
    algorithm = 'circo'
    draggable = True
    draggableupdate = False

class DotGraph(GraphVizDrawer):
    algorithm = 'dot'
    bezier = True
    draggable = True
    draggableupdate = False

class NeatoGraph(GraphVizDrawer):
    algorithm = 'neato'
    draggable = True
    draggableupdate = True

class FdpGraph(GraphVizDrawer):
    algorithm = 'fdp'
    draggable = True
    draggableupdate = False

class TwopiGraph(GraphVizDrawer):
    algorithm = 'twopi'
    draggable = True
    draggableupdate = False
