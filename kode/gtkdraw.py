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
t = '#B1.((((#B2.(#B3.(#B4.(B2))) (#B5.(#B6.(#B7.(#B8.(B1)))) #B9.((#B10.((#B11.(B9) #B12.(#B13.(#B14.(#B15.(B1)))))) #B16.(F1))))) #B17.(B1)) #B18.((#B19.(#B20.(B19)) (#B21.(B21) ((B1 #B22.(#B23.(B22))) #B24.(#B25.(#B26.((#B27.(B25) B25))))))))))'
#t = '#B1.(#B2.(#B3.(((#B4.((#B5.(#B6.(#B7.(B4))) #B8.(B3))) B3) (#B9.((#B10.(#B11.(B3)) B3)) (#B12.(#B13.(#B14.(#B15.(#B16.(B13))))) B1))))))'
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
		self.small_psize = 5
		self.medium_psize = 10
		self.large_psize = 15
		self.arrow_color = (1.0, 36.0 / 255.0, 0.0)


	def do_configure_event ( self, event ):
		print "do_configure_event"
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
			return True
		else:
			print "No more graphs"
			return False
		
	def back ( self ):
		#print "next graph"
		if self.graphnumber != 0:
			self.graphnumber = self.graphnumber - 1
			self.graph = self.mgs[self.graphnumber]
			return True
		else:
			print "No more graphs"
			return False
	
	def __render( self ):
		if self.graph:
			#print "rendering"
			self.graph.scale(800, 700)
			self.__cr.rectangle(0,0,self.__width, self.__height)
			self.__cr.set_source_rgb(1,1,1)
			self.__cr.fill()
        	
			self.__cr.save()

			# Edges
			if hasattr(self.graph, 'bezier') and self.graph.bezier:
				for node in self.graph.nodes:
					for edge in node.children:
						
						if node is self.graph.newest:
							self.__cr.set_line_width(3)
							self.__cr.set_source_rgb(34.0/255.0,139.0/255.0,34.0/255.0)
						else:
							self.__cr.set_line_width(1)
							self.__cr.set_source_rgb(130.0/255.0, 172.0/255.0, 245.0/255.0)
							
						if hasattr(edge, 'mouseover') and edge.mouseover:
							#print "	now really drawing"
							self.__cr.set_line_width(5)
							#self.__cr.set_source_rgb(0.0,238.0/255.0,0.0)
						
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
						for g in xrange(21):
							P = drawBezierGen(t, l, edge.ipoints)
							self.__cr.move_to(POld[0], POld[1])
							self.__cr.line_to(P[0], P[1])
							self.__cr.stroke()
							POld = P
							t = t + 0.05
							
						if len(node.term.redexpositions) == 0:
							pdia = self.large_psize
						elif node is self.graph.newest:
							pdia = self.medium_psize
						else:
							pdia = self.small_psize
							
						x1 = edge.ipoints[len(edge.ipoints)-1][0]
						y1 = edge.ipoints[len(edge.ipoints)-1][1]
						x2 = edge.get_far(node).x
						y2 = edge.get_far(node).y
						
						self.draw_arrowhead(x1, y1, x2, y2, pdia)
				self.__cr.restore()
				self.__cr.save()
			else:
				for node in self.graph.nodes:
						
					for edge in node.children:
						
						if node is self.graph.newest:
							self.__cr.set_line_width(3)
							self.__cr.set_source_rgb(34.0/255.0,139.0/255.0,34.0/255.0)
						else:
							self.__cr.set_line_width(1)
							self.__cr.set_source_rgb(130.0/255.0, 172.0/255.0, 245.0/255.0)
							
						if hasattr(edge, 'mouseover') and edge.mouseover:
							#print "	now really drawing"
							self.__cr.set_line_width(5)
							#self.__cr.set_source_rgb(0.0,238.0/255.0,0.0)
						
						far_node = edge.get_far(node)
						self.__cr.move_to(node.x, node.y)
						self.__cr.line_to(far_node.x, far_node.y)
						self.__cr.stroke()
						
						x1 = node.x
						y1 = node.y
						x2 = edge.get_far(node).x
						y2 = edge.get_far(node).y
						
						if len(edge.get_far(node).term.redexpositions) == 0:
							pdia = self.large_psize
						elif edge.get_far(node) is self.graph.newest:
							pdia = self.medium_psize
						else:
							pdia = self.small_psize
						#print "PDIA: " + str(pdia)
						
						self.draw_arrowhead(x1, y1, x2, y2, pdia)
						
				self.__cr.restore()
				self.__cr.save()
			
			# Nodes 34.0/255.0,139.0/255.0,34.0/255.0
			for node in self.graph.nodes:
				if len(node.term.redexpositions) == 0:
					self.__cr.arc(node.x, node.y, self.large_psize, 0, math.pi*2)
					#self.__cr.set_source_rgb(0xcc/255.0, 0, 0)
					self.__cr.set_source_rgb(0xa4/255.0, 0, 0)
					self.__cr.fill_preserve()
					self.__cr.set_source_rgb(0, 0, 0)
					self.__cr.stroke()
				elif node is self.graph.newest:
					self.__cr.arc(node.x, node.y, self.medium_psize, 0, math.pi*2)
					self.__cr.set_source_rgb(34.0/255.0,139.0/255.0,34.0/255.0)
					self.__cr.fill_preserve()
					self.__cr.set_source_rgb(0, 0, 0)
					self.__cr.stroke()
				else:
					self.__cr.arc(node.x, node.y, self.small_psize, 0, math.pi*2)
					self.__cr.set_source_rgb(0, 0, 0)
					self.__cr.fill_preserve()
					self.__cr.set_source_rgb(0, 0, 0)
					self.__cr.stroke()
				if hasattr(node, 'showterm') and node.showterm:
					parsedtermlist = str(node.term).split('#')
					parsedterm = ""
					lambdaletter = u'\u03bb'
					#for j in range(len(parsedtermlist)-1):
					#	parsedterm = parsedterm + parsedtermlist[j] + str(lambdaletter)
					#print "Term: " + str(parsedterm)
					#self.__cr.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
					#self.__cr.set_font_size(13)
					#self.__cr.move_to(10, 750)
					#self.__cr.show_text(unicode_to_glyph(parsedterm))
					###self.__cr.show_text(u'\u03bb')
			self.__cr.restore()
			#20115,11
			#3106
			#3106141126
			#9-31-8

	def draw_arrowhead(self, x1, y1, x2, y2, nodedia):
		'''
		Draws an arrow head on the line segment between the coordinate pairs
		(x1,y1) and (x2,y2). The arrow head is placed in the (x2,y2)-end.
		'''
		noderadius = nodedia / 2
		arrowwidth = 10
		Pi = math.pi
		angle = 20
		
		if x1 - x2 == 0:
			LineAngle = Pi / 2
		else:
			LineAngle = math.atan((y2 - y1) / (x2 - x1))
	
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
			
			Y3 -= yOffset
			Y4 -= yOffset
			X3 -= xOffset
			X4 -= xOffset
		else:
			x2 += xOffset
			y2 += yOffset
	
			Y3 = y2 + arrowwidth * math.sin(EndAngle1)
			Y4 = y2 + arrowwidth * math.sin(EndAngle2)
			X3 = x2 + arrowwidth * math.cos(EndAngle1)
			X4 = x2 + arrowwidth * math.cos(EndAngle2)
			
			Y3 += yOffset
			Y4 += yOffset
			X3 += xOffset
			X4 += xOffset
		
		# Draw the (filled) triangle.
		ac = self.arrow_color
		self.__cr.set_line_width(1)
		self.__cr.set_source_rgb(ac[0], ac[1], ac[2])
		self.__cr.move_to(x2,y2)
		self.__cr.line_to(X3,Y3)
		self.__cr.stroke_preserve()
		self.__cr.line_to(X4,Y4)
		self.__cr.stroke_preserve()
		self.__cr.line_to(x2,y2)
		self.__cr.stroke_preserve()
		self.__cr.fill()

def binomial(n, i):
	bin = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
	return bin

def drawBezierGen(t, l, ipoints):
	n = l - 1
	x = reduce(lambda x, b:x+b, (binomial(n, i) * pow((1 - t), n - i) * pow(t, i) * ipoints[i][0] for i in xrange(l)))
	y = reduce(lambda y, b:y+b, (binomial(n, i) * pow((1 - t), n - i) * pow(t, i) * ipoints[i][1] for i in xrange(l)))
	return [x, y]
	
def redraw(widget):
	if drawing.ready:
		drawing.graph.reset()
		drawing.graph.update_layout()
		drawing.queue_draw()
	else:
		print "No graph created yet!"
	
def optimize(widget):
	if drawing.ready:
		drawing.graph.update_layout()
		drawing.queue_draw()
	else:
		print "No graph created yet!"

def back(widget):
	if drawing.ready:
		if drawing.back():
			drawing.graph.update_layout()
			drawing.queue_draw()
	else:
		print "No graph created yet!"
	
def forward(widget):
	if drawing.ready:
		if drawing.forward():
			drawing.graph.update_layout()
			drawing.queue_draw()
	else:
		print "No graph created yet!"

algorithms = {'Neato' : NeatoGraph,
			'Dot' : DotGraph,
			'TwoPi' : TwopiGraph,
			'Circo' : CircoGraph,
			'Fdp' : FdpGraph,
			'Majorization' : MajorizationGraph}

def apply(widget):
	drawing.startnum = int(start.get_text())
	drawing.endnum = int(end.get_text())
	drawing.term = parser.parse(entry.get_text().replace(u'\u03bb',"#"))
	drawing.mgs = []
	operations.assignvariables(drawing.term)
	drawing.selected = str(algo.get_child().get_text())
	try:
		Drawer = algorithms[drawing.selected]
		for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			drawing.mgs.append(Drawer(g))
	except KeyError:
		pass
	drawing.initgraph(drawing.startnum)
	drawing.graph.update_layout()
	drawing.queue_draw()
	drawing.ready = True

def generateTerm(widget):
	drawing.term = randomgraph.randomterm()
	entry.set_text(str(drawing.term).replace("#",u'\u03bb'))
	entry.set_tooltip_text(str(drawing.term).replace("#",u'\u03bb'))
	
def changed_cb(entry):
	if hasattr(drawing, 'ready') and drawing.ready:
		drawing.selected = entry.get_text()
		drawing.mgs = []
		try:
			Drawer = algorithms[drawing.selected]
			for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
				drawing.mgs.append(Drawer(g))
		except KeyError:
			pass
		
		drawing.graph = drawing.mgs[drawing.graphnumber]
		drawing.graph.update_layout()
		drawing.queue_draw()

def key_press_event(widget, event):
	if event.keyval == 102 or event.keyval == 110: 
		forward(widget)
	elif event.keyval == 98: 
		back(widget)
	elif event.keyval == 114:
		redraw(widget)
	elif event.keyval == 111:
		optimize(widget)
		
def button_press_event(widget, event):
	#print "			PRESS"
	x = event.x - 240
	y = event.y
	r = 5
	if drawing.ready:
		for node in drawing.graph.nodes:
			if int(x) in xrange(int(node.x) - r, int(node.x) + r) and int(y) in xrange(int(node.y) - r, int(node.y) + r):
				print "Clicked on note"
				drawing.dragnode = True
				drawing.dragnodename = node
				window.connect("motion_notify_event", motion_notify_event)
				#if hasattr(node, 'showterm') and node.showterm:
				#	node.showterm = False
				#else:
				#	node.showterm = True
				#for edge in node.children:
				#	if hasattr(edge, 'mouseover') and edge.mouseover:
				#		edge.mouseover = False
				#	else:
				#		edge.mouseover = True
				#drawing.queue_draw()

def button_release_event(widget, event):
	#print "			RELEASE"
	x = event.x - 240
	y = event.y
	r = 5
	if drawing.ready:
		for node in drawing.graph.nodes:
			if int(x) in xrange(int(node.x) - r, int(node.x) + r) and int(y) in xrange(int(node.y) - r, int(node.y) + r):
				if hasattr(node, 'showterm') and node.showterm:
					node.showterm = False
				else:
					node.showterm = True
				for edge in node.children:
					if hasattr(edge, 'mouseover') and edge.mouseover:
						edge.mouseover = False
					else:
						edge.mouseover = True
				drawing.dragnode = False
				window.connect("motion_notify_event", motion_notify_event)
				#drawing.graph.update_layout()
				drawing.queue_draw()
			else:
				drawing.dragnode = False
				window.connect("motion_notify_event", motion_notify_event)
				node.showterm = False
				for edge in node.children:
					edge.mouseover = False
	
def motion_notify_event(widget, event):
	if drawing.dragnode:
		#print "			Node: " + str(node.x)
		x = event.x
		y = event.y
		print "Current position - (" + str(x) + "," + str(y) + ") - Node name: " + str(drawing.dragnodename.name)
		drawing.graph.nodenametable[drawing.dragnodename.name].x = x - 240
		drawing.graph.nodenametable[drawing.dragnodename.name].y = y
		drawing.queue_draw()
		
		
if __name__ == "__main__":
	window = gtk.Window()
	window.connect("delete-event", gtk.main_quit)
	window.connect("key_press_event", key_press_event)
	window.connect("button_release_event", button_release_event)
	window.connect("button_press_event", button_press_event)
	#window.connect("motion_notify_event", motion_notify_event)
	window.set_events(gtk.gdk.BUTTON_RELEASE_MASK
						| gtk.gdk.BUTTON_PRESS_MASK
						| gtk.gdk.POINTER_MOTION_MASK)
	width = 1024
	height = 768
	window.resize(width, height)
	mgs = []
	graph = None
	
	drawing = GraphArea(graph)
	
	drawing.ready = False
	
	widgetboxH = gtk.HBox(False, 10)
	widgetboxV = gtk.VBox(False, 10)

	#update_button = gtk.Button("Organise graph")
	#update_button.connect("clicked", update_layout, testgraph)
	
	# GTK Buttons
	b1 = gtk.Button("Generate Random Term")
	b2 = gtk.Button("Draw Graph")
	b3 = gtk.Button("Forward")
	b4 = gtk.Button("Back")
	b5 = gtk.Button("Redraw Graph")
	b6 = gtk.Button("Optimize Graph")
	
	# GTK Labels
	l1 = gtk.Label("Start")
	l1.set_text("Start:")
	l2 = gtk.Label("End")
	l2.set_text("End:   ")
	l3 = gtk.Label("Alg")
	l3.set_text("Alg:   ")
	
	drawing.term = t
	
	entry = gtk.Entry()
	entry.set_text(drawing.term)
	entry.set_tooltip_text(str(drawing.term))
	
	start = gtk.Entry()
	start.set_text("0")
	
	end = gtk.Entry()
	end.set_text("10000")
	
	algo = gtk.ComboBoxEntry()
	liststore = gtk.ListStore(str)
	algo.set_model(liststore)
	[liststore.append([k]) for k in algorithms.keys()]
	algo.set_text_column(0)
	algo.set_active(0)
	algo.child.connect('changed', changed_cb)
	
	
	
	b1.connect("clicked", generateTerm)
	b2.connect("clicked", apply)
	b3.connect("clicked", forward)
	b4.connect("clicked", back)
	b5.connect("clicked", redraw)
	b6.connect("clicked", optimize)
	
	startbox = gtk.HBox(False, 10)
	startbox.pack_start(l1, False, False, 1)
	startbox.pack_start(start, False, False, 1)
	
	endbox = gtk.HBox(False, 10)
	endbox.pack_start(l2, False, False, 1)
	endbox.pack_start(end, False, False, 1)
	
	#algobox = gtk.HBox(False, 10)
	#algobox.pack_start(l3, False, False, 1)
	#algobox.pack_start(algo, False, False, 1)
	
	widgetboxV.pack_start(entry, False, False, 1)
	widgetboxV.pack_start(b1, False, False, 1)
	widgetboxV.pack_start(algo, False, False, 1)
	widgetboxV.pack_start(startbox, False, False, 1)
	widgetboxV.pack_start(endbox, False, False, 1)
	widgetboxV.pack_start(b2, False, False, 1)
	widgetboxV.pack_start(b3, False, False, 1)
	widgetboxV.pack_start(b4, False, False, 1)
	widgetboxV.pack_start(b5, False, False, 1)
	widgetboxV.pack_start(b6, False, False, 1)
	
	widgetboxH.pack_start(widgetboxV, False, False, 5)
	widgetboxH.pack_end(drawing, True, True, 5)

	window.add(widgetboxV)
	window.add(widgetboxH)

	widgetboxV.show()
	startbox.show()
	endbox.show()
	#algobox.show()
	widgetboxH.show()
	entry.show()
	b1.show()
	#l3.show()
	algo.show()
	l1.show()
	start.show()
	l2.show()
	end.show()
	b2.show()
	b3.show()
	b4.show()
	b5.show()
	b6.show()
	drawing.show()
	window.present()
	gtk.main()