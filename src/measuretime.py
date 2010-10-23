# Reduction Visualizer. A tool for visualization of reduction graphs.
# Copyright (C) 2010 Niels Bjørn Bugge Grathwohl & Jens Duelund Pallesen
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

# Drawing algorithms
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph

import computegraph.operations as operations
import computegraph.randomgraph as randomgraph
import lambdaparser.lambdaparser as parser

from timeit import Timer

# termStr = "((((#B1.(B1) #B2.(#B3.(B3))) #B4.((#B5.(B5) #B6.(#B7.(B6))))) #B8.(#B9.(#B10.(#B11.(B11))))) #B12.((#B13.(B13) #B14.(#B15.(#B16.((B14 #B17.(B15))))))))"
termStr = "#m.(#n.(#f.(#x.(m n f x)))) #f.(#x.(f (f x))) #f.(#x.(f (f x)))"
numGenerations = 35

term = parser.parse(termStr.replace(u'\u03bb',"#"))
operations.assignvariables(term)
graph = operations.reductiongraph(term, numGenerations)

def start(repeat = 1):
	importStr = "from measuretime import graph ; from drawingalgorithms.majorizationgraph import MajorizationGraph ; from drawingalgorithms.graphvizdrawers import CircoGraph ; from drawingalgorithms.graphvizdrawers import DotGraph ; from drawingalgorithms.graphvizdrawers import NeatoGraph ; from drawingalgorithms.graphvizdrawers import TwopiGraph ; from drawingalgorithms.graphvizdrawers import FdpGraph"
	for algo in ["MajorizationGraph", "CircoGraph", "DotGraph", "NeatoGraph", "TwopiGraph", "FdpGraph"]:
		t = Timer("d = " + algo + "(graph) ; d.update_layout()", importStr)
		print algo + ": %.2f" % (t.timeit(number = repeat)/repeat)



def gettime():
	t = Timer("a = 2")
	
	print "Time: %.2f" % t.timeit(1000000)