# -*- coding: utf-8 -*-
'''
Utility module. As of now it simply provides the scale()-function to use
in the drawing algorithms.
'''

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


def scale(nodes, width, height, bezier = False):
    '''
    Scale the positions of the given nodes to fit in a box with the size
    width * height. If 'bezier' is True, the control points of bezier curves
    are scaled as well.
    '''
    Xs = [node.x for node in nodes]
    Ys = [node.y for node in nodes]
    w = max(Xs) - min(Xs)
    h = max(Ys) - min(Ys)
    
    scaling = [max(Xs) / (width - 30), max(Ys) / (height - 30)]
    
    for node in nodes:
        if w == 0:
            node.x = width / 2
        else:
            node.x = float(node.x) / scaling[0]
        if h == 0:
            node.y = height / 2
        else:
            node.y = float(node.y) / scaling[1]
        
        if not bezier:
            continue
        
        for edge in node.children:
            for i, point in enumerate(edge.ipoints):
                edge.ipoints[i] = map(lambda x:float(x[0]) / x[1], zip(point, scaling))
    