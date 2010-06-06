import gtk
import math
import cairo
import computegraph.operations as operations
import computegraph.randomgraph as randomgraph
import lambdaparser as parser

# Drawing algorithms
from drawingalgorithms.majorizationgraph import MajorizationGraph
from drawingalgorithms.graphvizdrawers import CircoGraph
from drawingalgorithms.graphvizdrawers import DotGraph
from drawingalgorithms.graphvizdrawers import NeatoGraph
from drawingalgorithms.graphvizdrawers import TwopiGraph
from drawingalgorithms.graphvizdrawers import FdpGraph


# t = '#x.(#y.((x y) y)) #x.(#y.((x y) y)) #x.(#y.((x y) y))'
# t = '(#x.((x x) x) #y.((y y) y))'
#t = '#a.(b) (#x.((x x) x) #y.((y y) y))'
# t = '#B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))'
# t = '#x.(#y.((x y) y)) #x.(#y.((x y) y)) #x.(#y.((x y) y))'
# Den her har fire normalformer som faas ved at lave max. 125 (maaske faerre!) iterationer.
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
graphnumber = 0

class GraphArea(gtk.DrawingArea):
	__gsignals__ = {
		"expose-event": "override",
		"configure_event": "override",
	}

	def __init__ ( self, mgs ):
		gtk.DrawingArea.__init__(self)
		self.mgs = mgs
		self.graphnumber = None
		self.graph = None
		self.currentgraph = None


	def do_configure_event ( self, event ):
		self.__width, self.__height = self.window.get_size()
		self.queue_draw()
		
	def do_expose_event ( self, event ):
		#print "exposing"
		self.__cr = self.window.cairo_create()
		self.__render()
		
	def initgraph (self, startnum):
		#print "Init Graph"
		#print "Start Num: " + str(startnum)
		#print "mgs len: " + str(len(self.mgs))
		self.graphnumber = 0
		self.graph = self.mgs[self.graphnumber]
		
	def forward ( self ):
		#print "next graph"
		if self.graphnumber+2 <= len(self.mgs):
			self.graphnumber = self.graphnumber + 1
			self.graph = self.mgs[self.graphnumber]
			update = True
			return update
		else:
			update = False
			print "No more graphs"
			return update
		
	def back ( self ):
		#print "next graph"
		if self.graphnumber != 0:
			self.graphnumber = self.graphnumber - 1
			self.graph = self.mgs[self.graphnumber]
			update = True
			return update
		else:
			print "No more graphs"
			update = False
			return update

#	def iter_done( self ):
#		print "drawing" 
#		while gtk.events_pending():
#			gtk.main_iteration(False)		
#		self.queue_draw()
#		time.sleep(0.03)
	
	
	def __render( self ):
		if self.graph:
			#print "rendering"
			self.graph.update_layout()
			self.graph.scale(800, 700)
			self.__cr.rectangle(0,0,self.__width, self.__height)
			self.__cr.set_source_rgb(1,1,1)
			self.__cr.fill()
        	
			self.__cr.save()

			# Edges
			if hasattr(self.graph, 'bezier') and self.graph.bezier:

				for node in self.graph.nodes:
					if node is self.graph.newest:
						self.__cr.set_line_width(3)
						self.__cr.set_source_rgb(34.0/255.0,139.0/255.0,34.0/255.0)
					else:
						self.__cr.set_line_width(1)
						self.__cr.set_source_rgb(130.0/255.0, 172.0/255.0, 245.0/255.0)
						
					for edge in node.children:
						self.graph.ipoints = edge.ipoints
						far_node = edge.get_far(node)
						
						destX = edge.destination.x
						destY = edge.destination.y
						
						lastX = edge.ipoints[len(edge.ipoints)-1][0]
						lastY = edge.ipoints[len(edge.ipoints)-1][1]
						if node.y != edge.ipoints[0][1] or node.x != edge.ipoints[0][0]:
							self.__cr.move_to(node.x, node.y)
							self.__cr.line_to(edge.ipoints[0][0], edge.ipoints[0][1])
							self.__cr.stroke()
						if destY != lastY or destX != lastX:
							self.__cr.move_to(far_node.x, far_node.y)
							self.__cr.line_to(lastX, lastY)
							self.__cr.stroke()
							
						POld = [edge.ipoints[0][0], edge.ipoints[0][1]]
						t = 0.00
						l = len(edge.ipoints)
						for g in range(101):
							P = drawBezierGen(t, l, edge.ipoints)
							self.__cr.move_to(POld[0], POld[1])
							self.__cr.line_to(P[0], P[1])
							self.__cr.stroke()
							POld = P
							t = t + 0.01
							
						x1 = node.x
						y1 = node.y
						x2 = edge.get_far(node).x
						y2 = edge.get_far(node).y
                        
						[X3, Y3, X4, Y4] = arrowhead(x1, y1, x2, y2)
                        
						self.__cr.move_to(x2,y2)
						self.__cr.line_to(X3,Y3)
						self.__cr.stroke()
						self.__cr.move_to(X3,Y3)
						self.__cr.line_to(X4,Y4)
						self.__cr.stroke()
						self.__cr.move_to(X4,Y4)
						self.__cr.line_to(x2,y2)
						self.__cr.stroke()
				self.__cr.restore()
				self.__cr.save()
			else:
				for node in self.graph.nodes:
					
					if node is self.graph.newest:
						self.__cr.set_line_width(3)
						self.__cr.set_source_rgb(34.0/255.0,139.0/255.0,34.0/255.0)
					else:
						self.__cr.set_line_width(1)
						self.__cr.set_source_rgb(130.0/255.0, 172.0/255.0, 245.0/255.0)
						
					for edge in node.children:
						far_node = edge.get_far(node)
						self.__cr.move_to(node.x, node.y)
						self.__cr.line_to(far_node.x, far_node.y)
						self.__cr.stroke()
						
						'''
						Draws an arrow head on the line segment between the coordinate pairs
						(x1,y1) and (x2,y2). The arrow head is placed in the (x2,y2)-end.
						'''
						x1 = node.x
						y1 = node.y
						x2 = edge.get_far(node).x
						y2 = edge.get_far(node).y
						
						[X3, Y3, X4, Y4] = arrowhead(x1, y1, x2, y2)
						
						self.__cr.move_to(x2,y2)
						self.__cr.line_to(X3,Y3)
						self.__cr.stroke()
						self.__cr.move_to(X3,Y3)
						self.__cr.line_to(X4,Y4)
						self.__cr.stroke()
						self.__cr.move_to(X4,Y4)
						self.__cr.line_to(x2,y2)
						self.__cr.stroke()
						
						self.__cr.stroke()
				self.__cr.restore()
				self.__cr.save()
			
			# Nodes 34.0/255.0,139.0/255.0,34.0/255.0
			for node in self.graph.nodes:
				if len(node.term.redexpositions) == 0:
					psize = 15
					self.__cr.arc(node.x, node.y, psize, 0, math.pi*2)
					self.__cr.set_source_rgb(0xcc/255.0, 0, 0)
					self.__cr.fill_preserve()
					self.__cr.set_source_rgb(0xa4/255.0, 0, 0)
					self.__cr.stroke()
				elif node is self.graph.newest:
					psize = 10
					self.__cr.arc(node.x, node.y, psize, 0, math.pi*2)
					self.__cr.set_source_rgb(34.0/255.0,139.0/255.0,34.0/255.0)
					self.__cr.fill_preserve()
					self.__cr.set_source_rgb(34.0/255.0,139.0/255.0,34.0/255.0)
					self.__cr.stroke()
				else:
					psize = 5
					self.__cr.arc(node.x, node.y, psize, 0, math.pi*2)
					self.__cr.set_source_rgb(0, 0, 0)
					self.__cr.fill_preserve()
					self.__cr.set_source_rgb(0, 0, 0)
					self.__cr.stroke()
			self.__cr.restore()
		else:
			print "Graph not defined!"
			

def arrowhead(x1, y1, x2, y2):
	noderadius = 2.5
	arrowwidth = 15
	Pi = math.pi
	angle = 10
	
	if x1 - x2 == 0:
		LineAngle = math.atan(0)
	else:
		LineAngle = math.atan((y2-y1)/(x2-x1))

	EndAngle1 = LineAngle + angle * Pi/180
	EndAngle2 = LineAngle - angle * Pi/180

	xOffset = noderadius * math.cos(LineAngle)
	yOffset = noderadius * math.sin(LineAngle)
	if x1 < x2:
		x2 -= xOffset
		y2 -= yOffset

		Y3 = y2 - arrowwidth * math.sin(EndAngle1)
		Y4 = y2 - arrowwidth * math.sin(EndAngle2)
		X3 = x2 - arrowwidth * math.cos(EndAngle1)
		X4 = x2 - arrowwidth * math.cos(EndAngle2)
	else:
		x2 += xOffset
		y2 += yOffset

		Y3 = y2 + arrowwidth * math.sin(EndAngle1)
		Y4 = y2 + arrowwidth * math.sin(EndAngle2)
		X3 = x2 + arrowwidth * math.cos(EndAngle1)
		X4 = x2 + arrowwidth * math.cos(EndAngle2)
	return [X3, Y3, X4, Y4]

def binomial(n, i):
	bin = math.factorial(n)/(math.factorial(i) * math.factorial(n - i))
	return bin

def drawBezierGen(t, l, ipoints):
	n = l-1
	x = y = 0
	for i in range(l):
		x = x + binomial(n,i) * pow((1 - t),n-i) * pow(t,i) * ipoints[i][0]
		y = y + binomial(n,i) * pow((1 - t),n-i) * pow(t,i) * ipoints[i][1]
	return [x,y]
	
def redraw(widget):
	print "You have clicked redraw!!!"
	
def optimize(widget):
	print "You have clicked optimize!!!"

def back(widget):
	#print "Graph Number: " + str(graphnumber)
	update = drawing.back()
	if update:
		drawing.queue_draw()
	
def forward(widget):
	#print "Graph Number: " + str(graphnumber)
	update = drawing.forward()
	if update:
		drawing.queue_draw()

def apply(widget):
	drawing.startnum = int(start.get_text())
	drawing.endnum = int(end.get_text())
	drawing.term = parser.parse(entry.get_text())
	drawing.mgs = []
	operations.assignvariables(drawing.term)
	drawing.selected = str(algo.get_child().get_text())
	if drawing.selected == "Neato":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(NeatoGraph(g))
	elif drawing.selected == "Dot":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(DotGraph(g))
	elif drawing.selected == "TwoPi":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(TwopiGraph(g))
	elif drawing.selected == "Circo":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(CircoGraph(g))
	elif drawing.selected == "Fdp":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(FdpGraph(g))
	elif drawing.selected == "Matrix":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(MajorizationGraph(g, 800, 700, 10**-2))
	drawing.mgs# = mgs
	drawing.initgraph(drawing.startnum)
	drawing.queue_draw()

def generateTerm(widget):
	drawing.term = randomgraph.randomterm()
	print "Random term: " + str(drawing.term)
	entry.set_text(str(drawing.term))
	tooltips.set_tip(entry, str(drawing.term))

def changed_cb(entry):
	drawing.selected = entry.get_text()
	drawing.mgs = []
	if drawing.selected == "Neato":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(NeatoGraph(g))
	elif drawing.selected == "Dot":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(DotGraph(g))
	elif drawing.selected == "TwoPi":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(TwopiGraph(g))
	elif drawing.selected == "Circo":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(CircoGraph(g))
	elif drawing.selected == "Fdp":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(FdpGraph(g))
	elif drawing.selected == "Matrix":
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(MajorizationGraph(g, 800, 700, 10**-2))
	drawing.mgs
	drawing.graph = drawing.mgs[drawing.graphnumber]
	drawing.queue_draw()


if __name__ == "__main__":
	window = gtk.Window()
	window.connect("delete-event", gtk.main_quit)
	width = 1024
	height = 768
	window.resize(width, height)
	mgs = []
	graph = None
	
	drawing = GraphArea(graph)
	
	widgetboxH = gtk.HBox(False, 10)
	widgetboxV = gtk.VBox(False, 10)

	#update_button = gtk.Button("Organise graph")
	#update_button.connect("clicked", update_layout, testgraph)
	
	b1 = gtk.Button("Generate Random Term")
	b2 = gtk.Button("Draw Term")
	b3 = gtk.Button("Forward")
	b4 = gtk.Button("Back")
	b5 = gtk.Button("Redraw Graph")
	b6 = gtk.Button("Optimize Graph")
	
	drawing.term = t
	
	entry = gtk.Entry()
	entry.set_text(drawing.term)
	
	tooltips = gtk.Tooltips()
	tooltips.set_tip(entry, str(drawing.term))
	
	start = gtk.Entry()
	start.set_text("0")
	
	end = gtk.Entry()
	end.set_text("10000")
	
	algo = gtk.ComboBoxEntry()
	liststore = gtk.ListStore(str)
	algo.set_model(liststore)
	liststore.append(["Neato"])
	liststore.append(["Dot"])
	liststore.append(["TwoPi"])
	liststore.append(["Circo"])
	liststore.append(["Fdp"])
	liststore.append(["Matrix"])
	algo.set_text_column(0)
	algo.set_active(0)
	algo.child.connect('changed', changed_cb)
	
	
	
	b1.connect("clicked", generateTerm)
	b2.connect("clicked", apply)
	b3.connect("clicked", forward)
	b4.connect("clicked", back)
	b5.connect("clicked", redraw)
	b6.connect("clicked", optimize)
	
	widgetboxV.pack_start(b1, False, False, 10)
	widgetboxV.pack_start(entry, False, False, 10)
	widgetboxV.pack_start(algo, False, False, 10)
	widgetboxV.pack_start(start, False, False, 10)
	widgetboxV.pack_start(end, False, False, 10)
	widgetboxV.pack_start(b2, False, False, 10)
	widgetboxV.pack_start(b3, False, False, 10)
	widgetboxV.pack_start(b4, False, False, 10)
	widgetboxV.pack_start(b5, False, False, 10)
	widgetboxV.pack_start(b6, False, False, 10)
	
	widgetboxH.pack_start(widgetboxV, False, False, 5)
	widgetboxH.pack_end(drawing, True, True, 5)

	window.add(widgetboxV)
	window.add(widgetboxH)

	widgetboxV.show()
	widgetboxH.show()
	b1.show()
	entry.show()
	algo.show()
	start.show()
	end.show()
	b2.show()
	b3.show()
	b4.show()
	b5.show()
	b6.show()
	drawing.show()
	window.present()
	gtk.main()