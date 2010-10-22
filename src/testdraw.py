import computegraph.operations as operations
from computegraph.reductiongraph import *
import lambdaparser as parser
from gldraw import GlDraw
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph
from drawingalgorithms.kkgraph import KKGraph



# t = '#x.(#y.((x y) y)) #x.(#y.((x y) y)) #x.(#y.((x y) y))'
# t = '(#x.((x x) x) #y.((y y) y))'
# t = '#a.(b) (#x.((x x) x) #y.((y y) y))'
# t = '#B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))'
# t = '#x.(#y.((x y) y)) #x.(#y.((x y) y)) #x.(#y.((x y) y))'
# Den her!
t = '#B1.(#B2.(#B3.(((#B4.((#B5.(#B6.(#B7.(B4))) #B8.(B3))) B3) (#B9.((#B10.(#B11.(B3)) B3)) (#B12.(#B13.(#B14.(#B15.(#B16.(B13))))) B1))))))'
# t = '(#B1.((#B2.((#B3.(F1) #B4.(#B5.((B2 B4))))) (#B6.(B6) #B7.(#B8.(#B9.(#B10.(B8))))))) ((((#B11.(#B12.(#B13.((#B14.(B13) B13)))) (#B15.(#B16.(#B17.(B17))) #B18.(#B19.(#B20.((B18 (B19 #B21.(#B22.((#B23.(B19) B19)))))))))) #B24.((#B25.(#B26.(#B27.(B26))) ((#B28.(B24) #B29.(#B30.(#B31.(#B32.(F2))))) B24)))) #B33.((B33 (#B34.(B33) (#B35.(((#B36.(#B37.(B36)) #B38.(B33)) #B39.(B33))) B33))))) (#B40.(#B41.(#B42.(#B43.(#B44.((#B45.(B41) #B46.(#B47.(B44)))))))) ((#B48.(((#B49.(#B50.(B48)) #B51.(B48)) #B52.(#B53.(B53)))) #B54.(#B55.((((#B56.(B56) #B57.(#B58.(B54))) #B59.(B54)) #B60.(#B61.(B61)))))) #B62.(#B63.(#B64.((#B65.(#B66.((B62 #B67.(#B68.((B66 B65)))))) (#B69.(#B70.(B69)) #B71.(B63))))))))))'
# t = '(#B1.(B1) (#B2.((#B3.((#B4.((B3 B3)) #B5.((B2 (#B6.(#B7.(#B8.(B7))) (#B9.(B9) B5)))))) #B10.(B10))) #B11.(#B12.(#B13.(B12)))))'
# t = '(#B1.(#B2.(#B3.(#B4.(B2)))) #B5.(#B6.((#B7.(#B8.((#B9.(B7) B7))) ((#B10.(#B11.(#B12.(B11))) B5) ((#B13.((#B14.(#B15.(#B16.(#B17.(B17)))) (B5 B5))) (#B18.(#B19.(#B20.(B18))) #B21.((#B22.(B6) B21)))) (#B23.(#B24.(B5)) B5)))))))'
# t = '((#B1.(B1) (#B2.(#B3.(#B4.(#B5.(#B6.(B5))))) #B7.(((#B8.(#B9.((#B10.(#B11.(#B12.(#B13.(B11)))) B9))) #B14.(#B15.(B7))) #B16.(#B17.(#B18.(#B19.(#B20.(#B21.(B21)))))))))) (#B22.((#B23.(#B24.(B24)) #B25.((#B26.(B26) #B27.(B27))))) #B28.(#B29.((B29 #B30.((F1 (B30 #B31.(#B32.(B29))))))))))'
# t = '(((((#B1.(#B2.(#B3.(#B4.(#B5.(B1))))) (#B6.((#B7.(B6) #B8.(B6))) F1)) #B9.(B9)) (#B10.(#B11.(#B12.(#B13.(#B14.(B11))))) #B15.((#B16.(B16) #B17.(#B18.(#B19.((B17 #B20.(F2))))))))) (#B21.(((#B22.(#B23.(#B24.(B21))) (B21 #B25.(#B26.(B26)))) #B27.(#B28.(#B29.((B27 B29)))))) #B30.(#B31.((((#B32.(#B33.(B32)) B30) #B34.(B34)) #B35.(#B36.(#B37.(#B38.(B30))))))))) (#B39.(#B40.(#B41.(#B42.(B39)))) (#B43.((B43 B43)) #B44.(B44))))'
# t = '#B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))'
# nedenstaaende har 600 knuder (med 200)
# t = '(((((#B1.(#B2.(#B3.(#B4.(#B5.(B1))))) (#B6.((#B7.(B6) #B8.(B6))) F1))#B9.(B9)) (#B10.(#B11.(#B12.(#B13.(#B14.(B11))))) #B15.((#B16.(B16)#B17.(#B18.(#B19.((B17 #B20.(F2)))))))))(#B21.(((#B22.(#B23.(#B24.(B21))) (B21 #B25.(#B26.(B26))))#B27.(#B28.(#B29.((B27 B29)))))) #B30.(#B31.((((#B32.(#B33.(B32)) B30)#B34.(B34)) #B35.(#B36.(#B37.(#B38.(B30)))))))))(#B39.(#B40.(#B41.(#B42.(B39)))) (#B43.((B43 B43)) #B44.(B44))))'
# The Y combinator
# t = '#f.(#x.(f (x x))) (#x.(f (x x))) #y.y'
# t = '(#B1.(B1) (((#B2.(#B3.(B3)) #B4.(#B5.((#B6.(B5) #B7.(#B8.(#B9.(B5))))))) #B10.((#B11.(#B12.(#B13.(B10))) #B14.(B14)))) #B15.(#B16.((B16 B16)))))'
#def draw(term):
#	g = operations.reductiongraph(term, 30)
#	print "Graph has " + str(len(g.nodes)) + " nodes."
#	graph = MajorizationGraph(g, 1000, 730)
#	gldraw = GlDraw()
#	gldraw.draw(graph)

#def drawGV(term):
#	g = operations.reductiongraph(term, 3)
#	print "Graph has " + str(len(g.nodes)) + " nodes."
#	gv = pygraphviztest.GraphViz()
#	gv.draw(g)

def drawitGV(term):
	mgs = []
	for (i,g) in enumerate(operations.reductiongraphiter(term, 0, 500)):
		mgs.append(DotGraph(g))
	#gldraw = GlDraw()
	#gldraw.drawlist(mgs)
	#g = gldraw2.GlDraw()
	#g.drawlist(mgs)
	print "asdasdasdasda"
	gtkd = GtkDraw()
	gtkd.draw
	
def drawit(term):
	mgs = []
	for (i,g) in enumerate(operations.reductiongraphiter(term, 0, 500)):
		#if len(g.nodes) <= 5:
		#	continue
		print "Graph no. " + str(i)
		mgs.append(MajorizationGraph(g, 1000, 730, 10**-2))
	print "Drawing " + str(len(mgs)) + " different graph versions."
	gldraw = GlDraw()
	gldraw.drawlist(mgs)

def drawit2(term):
	def f(term):
		for g in operations.reductiongraphiter(term, 0, 100):
			# yield KKGraph(g,1000,730)
			yield MajorizationGraph(g, 1024, 738, 10**-3)
			# yield DotGraph(g)
			# yield CircoGraph(g)
			# yield FdpGraph(g)
			# yield TwopiGraph(g)
			# yield NeatoGraph(g)
			# yield KKGraph(g)
	
	gldraw = GlDraw(iterable = f(term))
	gldraw.drawiter()

if __name__ == "__main__":
	term = parser.parse(t)
	operations.assignvariables(term)
	drawit2(term)