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

'''
Graph abstraction to be used with the Kamada-Kawai force-directed algorithm.
'''
import sys
import pdb
import math
import random
import numpy
import computegraph.shortestpath as SP
from drawingalgorithm import DrawingAlgorithm

# TODO Den her skal gaas igennem!
class KKGraph(DrawingAlgorithm):
    def __init__(self, graph, width = 200, height = 200):
        for name, value in vars(graph).iteritems():
            setattr(self, name, value)
        
        self.nodesdict = {}
        self.nodes = []
        self.graph = graph
        
        random.seed()
        
        self.spring = 1
        self.max_passes = 5000
        self.min_epsilon = 1
        self.updates = 1
        self.pad = 10
        self.width = width
        self.height = height
        
        self.reset()
    
    def update_layout( self ):
        self.drawingfunction = None
        for node in self.nodes:
            self.__run_kk_on( node )
    
    def initwith(self, g):
        self.reset()
    
    def scale(self, width, height):
        pass
    
    def reset( self ):
        for (key, node) in self.graph.nodesdict.iteritems():
            self.nodesdict[key] = node
            self.nodes.append(node)
            node.x = random.randint(1, self.width)
            node.y = random.randint(1, self.height)
    
    def update_layout_animated(self, drawingfunction):
        self.drawingfunction = drawingfunction
        for node in self.nodes:
            self.__run_kk_on( node )
        
    
    
    def __get_delta_m( self, i, l_matrix, k_matrix, x_array, y_array ):
        squared = lambda x:numpy.power(x, 2)
        M1, M2 = numpy.meshgrid(x_array, x_array)
        M3, M4 = numpy.meshgrid(y_array, y_array)
        dxs = (M1 - M2)
        dys = (M3 - M4)
        dds = numpy.sqrt(squared(dxs) + squared(dys))
        xpars = numpy.multiply(k_matrix, numpy.multiply(dxs - l_matrix, numpy.divide(dxs, dds)))
        ypars = numpy.multiply(k_matrix, numpy.multiply(dys - l_matrix, numpy.divide(dys, dds)))
        xsum = numpy.sum(xpars)
        ysum = numpy.sum(ypars)
        delta_m = math.sqrt(xsum**2 + ysum**2)
        return delta_m
        #nnodes = len(self.nodes)
        #delta_m = 0
        #x_partial = 0
        #y_partial = 0
        #
        #for j in xrange(nnodes):
        #   if i != j:
        #       dx = x_array[i] - x_array[j]
        #       dy = y_array[i] - y_array[j]
        #       dd = math.sqrt(dx * dx + dy * dy)
        #       km_val = k_matrix[i, j]
        #       lm_val = l_matrix[i, j]
        #       x_partial += km_val * (dx - lm_val * dx / dd)
        #       y_partial += km_val * (dy - lm_val * dy / dd)
        #
        #delta_m = math.sqrt((x_partial * x_partial) + (y_partial * y_partial))
        #return delta_m

    # the bulk of the KK inner loop, estimates location of local minima
    def __get_deltas( self, i, l_matrix, k_matrix, x_array, y_array ):
        # solve deltaM partial eqns to figure out new position for node of index i
        # where deltaM is close to 0 (or less then epsilon)
        nnodes = len(self.nodes)
        x_partial = 0
        y_partial = 0
        xx_partial = 0
        xy_partial = 0
        yx_partial = 0
        yy_partial = 0

        for j in range(nnodes):
            if i != j:
                dx = x_array[i] - x_array[j]
                dy = y_array[i] - y_array[j]
                dd = math.sqrt(dx * dx + dy * dy)

                km_val = k_matrix[i, j]
                lm_val = l_matrix[i, j]
                dd_cubed = dd * dd * dd

                x_partial += km_val * (dx - lm_val * dx / dd)
                y_partial += km_val * (dy - lm_val * dy / dd)
                xx_partial += km_val * (1 - lm_val * dy * dy / dd_cubed)
                xy_partial += km_val * (lm_val * dx * dy / dd_cubed)
                yx_partial += km_val * (lm_val * dy * dx / dd_cubed)
                yy_partial += km_val * (1 - lm_val * dx * dx / dd_cubed)

        # calculate x and y position difference using partials
        x_delta = ((-x_partial) * yy_partial - xy_partial * (-y_partial)) / (xx_partial * yy_partial - xy_partial * yx_partial)
        y_delta = (xx_partial * (-y_partial) - (-x_partial) * yx_partial) / (xx_partial * yy_partial - xy_partial * yx_partial)

        return (x_delta, y_delta)

    def __get_energy( self, l_matrix, k_matrix, x_array, y_array ):
        squared = lambda x:numpy.power(x, 2)
        
        M1, M2 = numpy.meshgrid(x_array, x_array)
        M3, M4 = numpy.meshgrid(y_array, y_array)
        dxs2 = squared(M1 - M2)
        dys2 = squared(M3 - M4)
        A = 0.5 * k_matrix
        B = dxs2 + dys2 + squared(l_matrix) - 2 * l_matrix * numpy.sqrt(dxs2 + dys2)
        C = numpy.multiply(A, B)
        
        return numpy.sum(C)
        
        #nnodes = len(self.nodes)
        #energy = 0.0
        #for i in range(nnodes - 1):
        #   for j in range(nnodes):
        #       dx = x_array[i] - x_array[j]
        #       dy = y_array[i] - y_array[j]
        #       lij = l_matrix[i, j]
        #       a = 0.5 * k_matrix[i, j]
        #       b = (dx * dx + dy * dy + lij * lij - 2 * lij * math.sqrt(dx * dx + dy * dy))
        #       c = (a * b)
        #       # work around a weird nan bug in python
        #       if a > 1e308:
        #           c = 0.0
        #       energy = energy + c
        #return energy

    def __get_diameter( self, dist_matrix ):
        nnodes = len(self.nodes)
        graph_diam = 0
        for i in range(nnodes):
            for j in range(nnodes):
                graph_diam = max(graph_diam, dist_matrix[i, j])
        return int(graph_diam)

    def __calc_k_matrix( self, dist_matrix):
        nnodes = len(self.nodes)
        kmatrix = numpy.ndarray((nnodes, nnodes))

        for i in range(nnodes):
            for j in range(nnodes):
                dist_m = dist_matrix[i, j]
                kmatrix[i, j] = self.spring / (dist_m * dist_m)
        return kmatrix

    def __calc_l_matrix( self, dist_matrix, optimal_distance):
        nnodes = len(self.nodes)
        lmatrix = numpy.ndarray((nnodes, nnodes))

        for i in range(nnodes):
            for j in range(nnodes):
                lmatrix[i, j] = optimal_distance * dist_matrix[i, j]
        return lmatrix

    # FIXME HUGE bug here regarding priority list and dist matrix always being 0
    def __get_idist_matrix (self):
        
        # pdb.set_trace()
        (D, A) = SP.seidel(self)
        # (D, A) = SP.floydwarshal(self)
        return D
        
        #nnodes = len(self.nodes)
        #dist_matrix = numpy.ndarray((nnodes, nnodes))
        #
        ## Set each array element to infinity
        #for i in range(nnodes):
        #   for j in range(nnodes):
        #       dist_matrix[i, j] = 1e308
        #
        #for node in self.nodes:
        #   i = self.nodes.index(node)
        #   node_queue = []
        #   checked_nodes = []
        #   priority_list = []
        #
        #   # find paths to all nodes connected to i
        #   dist_matrix[i, i] = 0.0
        #   checked_nodes.append(node)
        #   priority_list.append(0.0)
        #   node_queue.append(node)
        #
        #   while len(node_queue) > 0:
        #       # find node with smallest priority value
        #       fringe_node_priority = 1e308
        #       fringe_node_index = sys.maxint
        #
        #       for n in range(len(priority_list)):
        #           if priority_list[n] < fringe_node_priority:
        #               fringe_node_index = n
        #               fringe_node_priority = priority_list[fringe_node_index]
        #
        #       fringe_node = node_queue[fringe_node_index]
        #       fringe_node_dist = priority_list[fringe_node_index]
        #       node_queue.remove(fringe_node)
        #       priority_list.remove(priority_list[fringe_node_index])
        #       checked_nodes.append(fringe_node)
        #
        #       # put distance in matrix
        #       index = self.nodes.index(fringe_node)
        #       dist_matrix[i, index] = fringe_node_dist
        #       dist_matrix[index, i] = fringe_node_dist
        #
        #       # loop over its edges, adding nodes to queue
        #       edges = fringe_node.parents + fringe_node.children
        #       for edge in edges:
        #           work_node = edge.get_far(fringe_node)
        #           try:
        #               checked_nodes.index(work_node)
        #           except:
        #               # calc work_node's distance from node
        #               work_node_dist = fringe_node_dist + edge.weight
        #               try:
        #                   prev_dist_index = node_queue.index(work_node)
        #               except:
        #                   prev_dist_index = -1
        #
        #               if prev_dist_index >= 0:
        #                   # check if it has a lower distance
        #                   if priority_list[prev_dist_index] > work_node_dist:
        #                       # repace it with new value
        #                       priority_list[prev_dist_index] = work_node_dist
        #               else:
        #                   # add the worknode to the queue with priority
        #                   priority_list.append (work_node_dist)
        #                   node_queue.append (work_node)
        #return dist_matrix

    def __run_kk_on( self, node ):
        nnodes = len(self.nodes)
        dist_matrix = self.__get_idist_matrix()

        k_matrix = self.__calc_k_matrix(dist_matrix)
        optimal_distance = min(self.width, self.height) / max(self.__get_diameter(dist_matrix), 1)
        l_matrix = self.__calc_l_matrix(dist_matrix, optimal_distance)

        x_array = numpy.ndarray(nnodes)
        y_array = numpy.ndarray(nnodes)

        for node in self.nodes:
            x_array[self.nodes.index(node)] = node.x
            y_array[self.nodes.index(node)] = node.y

        # calc value to start minimization from (should be based on previous?)
        # figure out the initial stat to compare to at the end
        initial_energy = self.__get_energy(l_matrix, k_matrix, x_array, y_array)
        epsilon = initial_energy / nnodes
        # figure out which node to start moving first
        max_delta_m_index = 0
        max_delta_m = self.__get_delta_m(0, l_matrix, k_matrix, x_array, y_array)
        for i in range(nnodes):
            delta_m = self.__get_delta_m(i, l_matrix, k_matrix, x_array, y_array)
            if delta_m > max_delta_m:
                max_delta_m = delta_m
                max_delta_m_index = i

        stop = False
        passes = 0
        sub_passes = 0
        while epsilon > self.min_epsilon:
            previous_max_delta_m = max_delta_m + 1
            # KAMADA-KAWAI LOOP: while the delta_m of the node with the largest delta_m > epsilon..
            while max_delta_m > epsilon and previous_max_delta_m - max_delta_m > 0.1 and not stop:
                move_node_delta_m = max_delta_m
                # KK INNER LOOP while the node with the largest energy > epsilon...
                while move_node_delta_m > epsilon and not stop:
                    # get the deltas which will move node towards the local minima
                    (x_delta, y_delta) = self.__get_deltas(max_delta_m_index, l_matrix, k_matrix, x_array, y_array)
                    # set coords of node to old coords + changes
                    
                    x_array[max_delta_m_index] += x_delta
                    y_array[max_delta_m_index] += y_delta
                    # previousDeltaM = moveNodeDeltaM
                    # recalculate the deltaM of the node w/ new vals
                    move_node_delta_m = self.__get_delta_m(max_delta_m_index, l_matrix, k_matrix, x_array, y_array)
                    sub_passes = sub_passes + 1
                    if sub_passes > self.max_passes: stop = True

                # recalculate deltaMs and find node with max
                max_delta_m_index = 0
                max_delta_m = self.__get_delta_m(0, l_matrix, k_matrix, x_array, y_array)
                for i in range(nnodes):
                    delta_m = self.__get_delta_m(i, l_matrix, k_matrix, x_array, y_array)
                    if delta_m > max_delta_m:
                        max_delta_m = delta_m
                        max_delta_m_index = i

                # if set to update display, update on every nth pass
                if self.updates > 0:
                    if passes % self.updates == 0:
                        for i in range(len(self.nodes)):
                            node = self.nodes[i]
                            node.x = x_array[i]
                            node.y = y_array[i]
                        self.iter_done()

                passes = passes + 1

            epsilon -= epsilon / 4

        for i in range(len(self.nodes)):
            node = self.nodes[i]
            node.x = x_array[i]
            node.y = y_array[i]
        self.iter_done()

    def iter_done( self ):
        """
        Placeholder function for calling a screen update
        """
        if not self.drawingfunction is None:
            self.drawingfunction(self)

        pass
