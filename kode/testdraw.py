import math
import time
import computegraph.operations as operations
import lambdaparser as parser
import randomgraph
import graphicsutils
import gldraw
from computegraph.kkgraph import KKGraph
from computegraph.reductiongraph import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

ESCAPE = '\033'

def graphify(termstr = '', gr = None):
	
	graph = None
	term = ''
	if not termstr == '':
		term = parser.parse(termstr)
	elif not gr == None:
		graph = gr
	else:
		graph = randomgraph.generatereductiongraph()
		while len(graph.nodes) == 0 or len(graph.nodes) > 50: # For now, draw only smaller graphs.
			graph = randomgraph.generatereductiongraph()
	
	if graph is None:
		operations.assignvariables(term)
		g = operations.reductiongraph(term, 20)
	else:
		g = graph
	
	kkGraph = KKGraph(g, 800, 500)
	print "Drawing graph with " + str(len(g.nodes)) + " nodes."
	return kkGraph

if __name__ == "__main__":
	kkgraph = graphify('#B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))')
	g = gldraw.GlDraw()
	g.draw(kkgraph)