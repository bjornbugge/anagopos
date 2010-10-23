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

class DrawingAlgorithm(object):
	'''
	Class that all drawing algorithms must extend.
	'''
	
	# The attributes below must be set if an algorithm should be added to the
	# application
	'''
	Set to true if the algorithm uses bezier curves.
	'''
	bezier = None
	'''
	True if the nodes can be dragged with the mouse.
	'''
	draggable = None
	'''
	True if the graph should optmize its layout after a node has been dragged.
	'''
	draggableupdate = None

	
	def __init__(self, graph):
		raise NotImplementedError()
	
	def reset(self, control = 0):
		'''
		Reset the positions of the nodes in the graph, by e.g. assigning them
		random positions. The optional argument "control" can be used to control
		which node positions should be reset and which not, for instance when
		initializing this graph with the positions from another graph.
		'''
		raise NotImplementedError()
	
	def initwith(self, othergraph):
		'''
		Initialize this graph with the node positions from the given graph.
		The positions of the rest of the nodes, those that are not present in 
		the given graph, are not specified.
		'''
		raise NotImplementedError()
	
	def update_layout(self):
		'''
		Execute the drawing algorithm. After a run of this method, the nodes in
		the graph have been assigned (x,y)-coordinates.
		'''
		raise NotImplementedError()
		
	def update_layout_animated(self, callback):
		'''
		Execute the drawing algorithm, but perform a call to the given callback
		function at certain points in the algorithm (e.g. after each iteration).
		The callback function would typically be a call to the graphics routines
		that prompts an update of the screen.
		'''
		raise NotImplementedError()
	
	def scale(self, width, heigth):
		'''
		Scale the graph to fit into a box with the size "width" times "height".
		'''
		raise NotImplementedError()