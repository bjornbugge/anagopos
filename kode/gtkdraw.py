import gtk
import math
import computegraph.operations as operations
import computegraph.randomgraph as randomgraph
import lambdaparser.lambdaparser as parser
from grapharea import GraphArea

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
	drawing.initgraph()
	drawing.graph.update_layout()
	drawing.queue_draw()
	drawing.ready = True

def applyiterator(widget):
	drawing.startnum = int(start.get_text())
	drawing.endnum = int(end.get_text())
	drawing.term = parser.parse(entry.get_text().replace(u'\u03bb',"#"))
	drawing.mgs = []
	operations.assignvariables(drawing.term)
	drawing.selected = str(algo.get_child().get_text())
	try:
		def iterator():
			Drawer = algorithms[drawing.selected]
			for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
				print "Yielding graph"
				yield Drawer(g)
		drawing.iterator = iterator()
	except KeyError:
		pass
	drawing.initgraph()
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
		# print "Current position - (" + str(x) + "," + str(y) + ") - Node name: " + str(drawing.dragnodename.name)
		drawing.graph.nodenametable[drawing.dragnodename.name].x = x - 240
		drawing.graph.nodenametable[drawing.dragnodename.name].y = y
		drawing.queue_draw()
		
		
if __name__ == "__main__":
	window = gtk.Window()
	window.connect("delete-event", gtk.main_quit)
	window.connect("key_press_event", key_press_event)
	window.connect("button_release_event", button_release_event)
	window.connect("button_press_event", button_press_event)
	window.connect("motion_notify_event", motion_notify_event)
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
	b2.connect("clicked", applyiterator)
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