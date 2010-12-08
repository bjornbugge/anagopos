'''
Deep-copy function. Use instead of built-in deep-copy because this is specialized
and thus faster for reduction graphs.
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

import reductiongraph

def copygraph(graph):
    '''
    Perform a deep copy of the given graph.
    Use this function instead of copy.deepcopy() because this one is much faster!
    '''
    graphcopy = reductiongraph.Graph()
    # Add nodes
    map(lambda x:graphcopy.addnode(x[1].term, x[1].name), graph.nodesdict.iteritems())
    
    # Add edges
    for (key, node) in graph.nodesdict.iteritems():
        nodecopy = graphcopy.nodesdict[key]
        for c in node.children:
            destkey = str(c.destination.term)
            nodecopy.addchild(graphcopy.nodesdict[destkey])
    
    newestkey = str(graph.newest.term)
    graphcopy.newest = graphcopy.nodesdict[newestkey]
    return graphcopy

