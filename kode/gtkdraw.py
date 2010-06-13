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
#t = '#B1.((((#B2.(#B3.(#B4.(B2))) (#B5.(#B6.(#B7.(#B8.(B1)))) #B9.((#B10.((#B11.(B9) #B12.(#B13.(#B14.(#B15.(B1)))))) #B16.(F1))))) #B17.(B1)) #B18.((#B19.(#B20.(B19)) (#B21.(B21) ((B1 #B22.(#B23.(B22))) #B24.(#B25.(#B26.((#B27.(B25) B25))))))))))'
t = '(#B1.((#B2.((#B3.(B2) B2)) (((#B4.(#B5.(#B6.(#B7.(#B8.(#B9.(B9)))))) #B10.(#B11.(B11))) (#B12.(#B13.(#B14.(B13))) ((#B15.(#B16.((#B17.(#B18.(B16)) #B19.(B19)))) #B20.((#B21.(#B22.(#B23.(#B24.(#B25.(B1))))) B1))) B1))) B1))) (((#B26.(#B27.(#B28.(#B29.(#B30.(B28))))) #B31.(#B32.(B32))) #B33.(#B34.(#B35.(#B36.(#B37.(#B38.((B36 B34)))))))) (#B39.((#B40.(#B41.(B40)) (((B39 #B42.(B42)) (#B43.(#B44.(#B45.(B39))) #B46.(B39))) (#B47.(#B48.((B47 B47))) #B49.(#B50.(#B51.(#B52.(B39)))))))) (#B53.(((#B54.(#B55.(#B56.(B55))) (#B57.(#B58.(B53)) B53)) (#B59.((#B60.(#B61.(#B62.(B59))) #B63.(#B64.(B64)))) #B65.((#B66.((B65 #B67.(#B68.(#B69.(#B70.(B53)))))) #B71.(B53)))))) (#B72.(((#B73.(#B74.(#B75.(B74))) #B76.(B72)) (#B77.(B72) #B78.(#B79.(B72))))) #B80.(((#B81.(#B82.(B81)) #B83.(#B84.(#B85.((B83 (B84 (B85 #B86.(B85)))))))) B80)))))))'
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
	outputtext = "Previous graph\nGeneration: XX\nSomething more"
	outputtextbuffer.set_text(outputtext)
	
def forward(widget):
	if drawing.ready:
		if drawing.forward():
			drawing.graph.update_layout()
			drawing.queue_draw()
	else:
		print "No graph created yet!"
	outputtext = "Next graph\nGeneration: XX\nSomething more"
	outputtextbuffer.set_text(outputtext)

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
	tempterm = termtext.get_text(termtext.get_start_iter(),termtext.get_end_iter())
	try:
		drawing.term = parser.parse(tempterm.replace(u'\u03bb',"#"))
		drawing.mgs = []
		operations.assignvariables(drawing.term)
		drawing.selected = str(algo.get_child().get_text())
		tag = termtext.create_tag(background="White")
		termtext.apply_tag(tag, termtext.get_start_iter(),termtext.get_end_iter())
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
	except:
		tag = termtext.create_tag(background="Red")
		termtext.apply_tag(tag, termtext.get_start_iter(),termtext.get_end_iter())
		#states = [gtk.STATE_NORMAL, gtk.STATE_ACTIVE, gtk.STATE_PRELIGHT, gtk.STATE_SELECTED, gtk.STATE_INSENSITIVE]
		#for state in states:
		#    entry.modify_bg(state, gtk.gdk.color_parse("Red"))
		print "Could not parse term"

def generateTerm(widget):
	drawing.term = randomgraph.randomterm()
	termtext.set_text(str(drawing.term).replace("#",u'\u03bb'))
	entry.set_tooltip_text(str(drawing.term).replace("#",u'\u03bb'))
	
def changed_cb(entry):
	if hasattr(drawing, 'ready') and drawing.ready:
		drawing.selected = entry.get_text()
		drawing.mgs = []
		try:
			#Drawer = algorithms[drawing.selected]
			#for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
			#	drawing.mgs.append(Drawer(g))
			def iterator():
				Drawer = algorithms[drawing.selected]
				for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
					print "Yielding graph"
					yield Drawer(g)
			drawing.iterator = iterator()
		except KeyError:
			pass
		
		# drawing.graph = drawing.mgs[drawing.graphnumber]
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
	x = event.x - 240
	y = event.y
	r = 10
	if drawing.ready:
		for node in drawing.graph.nodes:
			if int(x) in xrange(int(node.x) - r, int(node.x) + r) and int(y) in xrange(int(node.y) - r, int(node.y) + r):
				print "Clicked on node"
				drawing.draggednode = True
				drawing.draggednode = node
				clickedtermtemp = str(node.term).replace("#",u'\u03bb')
				clickedterm.set_text(clickedtermtemp)
				entryclickedterm.set_buffer(clickedterm)
				entryclickedterm.set_tooltip_text(clickedtermtemp)

def button_release_event(widget, event):
	x = event.x - 240
	y = event.y
	r = 10
	if drawing.ready:
		for node in drawing.graph.nodes:
			if int(x) in xrange(int(node.x) - r, int(node.x) + r) and int(y) in xrange(int(node.y) - r, int(node.y) + r):
				if hasattr(node, 'showterm') and node.showterm:
					node.showterm = False
				else:
					node.showterm = True
				for edge in node.children:
					if hasattr(edge, 'selected') and edge.selected:
						edge.selected = False
					else:
						edge.selected = True
				drawing.draggednode = False
				drawing.queue_draw()
			else:
				drawing.draggednode = False
				node.showterm = False
				for edge in node.children:
					edge.selected = False
	
def motion_notify_event(widget, event):
	if drawing.draggednode:
		drawing.draggednode.x = event.x - 240
		drawing.draggednode.y = event.y
		drawing.queue_draw()

if __name__ == "__main__":
	window = gtk.Window()
	window.connect("delete-event", gtk.main_quit)
	window.connect("key_press_event", key_press_event)
	window.connect("button_release_event", button_release_event)
	window.connect("button_press_event", button_press_event)
	window.connect("motion_notify_event", motion_notify_event)
	window.set_events(gtk.gdk.BUTTON_RELEASE_MASK
						| gtk.gdk.BUTTON_PRESS_MASK
						| gtk.gdk.POINTER_MOTION_MASK)
	width = 1024
	height = 768
	window.resize(width, height)
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
	l4 = gtk.Label("Term")
	l4.set_text("Lambda Term:")
	l4.set_alignment(xalign=0, yalign=1)
	l5 = gtk.Label("ClickedTerm")
	l5.set_text("Clicked Term:")
	l5.set_alignment(xalign=0, yalign=1)
	l6 = gtk.Label("Output")
	l6.set_text("Output:")
	l6.set_alignment(xalign=0, yalign=1)
	
	drawing.term = str(t).replace("#",u'\u03bb')
	#t = clickedtermtemp = str(t).replace("#",u'\u03bb')
	termtext = gtk.TextBuffer()
	#termtext.set_text(drawing.term)
	
	entry = gtk.TextView()
	entry.set_justification(False)
	entry.set_left_margin(5)
	entry.set_right_margin(5)
	entry.set_size_request(200, 109)
	entry.set_buffer(termtext)
	#entry.set_tooltip_text(str(drawing.term))
	entry.set_wrap_mode(True)
	entry.set_border_window_size(gtk.TEXT_WINDOW_LEFT,2)
	entry.set_border_window_size(gtk.TEXT_WINDOW_RIGHT,2)
	
	#t = clickedtermtemp = str(t).replace("#",u'\u03bb')
	outputtextbuffer = gtk.TextBuffer()
	outputtextbuffer.set_text("Output text...")
	
	outputtextfield = gtk.TextView()
	outputtextfield.set_justification(False)
	outputtextfield.set_left_margin(5)
	outputtextfield.set_right_margin(5)
	outputtextfield.set_size_request(200, 59)
	outputtextfield.set_buffer(outputtextbuffer)
	outputtextfield.set_tooltip_text("Output text...")
	outputtextfield.set_wrap_mode(True)
	outputtextfield.set_border_window_size(gtk.TEXT_WINDOW_LEFT,2)
	outputtextfield.set_border_window_size(gtk.TEXT_WINDOW_RIGHT,2)
	outputtextfield.set_editable(False)
	
	clickedterm = gtk.TextBuffer()
	clickedterm.set_text("Clicked term...")
	
	entryclickedterm = gtk.TextView()
	entryclickedterm.set_justification(False)
	entryclickedterm.set_left_margin(5)
	entryclickedterm.set_right_margin(5)
	entryclickedterm.set_size_request(200, 109)
	entryclickedterm.set_buffer(clickedterm)
	entryclickedterm.set_tooltip_text(str("Clicked term..."))
	entryclickedterm.set_wrap_mode(True)
	entryclickedterm.set_border_window_size(gtk.TEXT_WINDOW_LEFT,2)
	entryclickedterm.set_border_window_size(gtk.TEXT_WINDOW_RIGHT,2)
	entryclickedterm.set_editable(False)
	
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
	
	widgetboxV.pack_start(l4, False, False, 1)
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
	widgetboxV.pack_start(l5, False, False, 1)
	widgetboxV.pack_start(entryclickedterm, False, False, 1)
	widgetboxV.pack_start(l6, False, False, 1)
	widgetboxV.pack_start(outputtextfield, False, False, 1)
	
	
	widgetboxH.pack_start(widgetboxV, False, False, 5)
	widgetboxH.pack_end(drawing, True, True, 5)

	#window.add(widgetboxV)
	window.add(widgetboxH)

	widgetboxV.show()
	startbox.show()
	endbox.show()
	#algobox.show()
	widgetboxH.show()
	l4.show()
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
	l5.show()
	entryclickedterm.show()
	l6.show()
	outputtextfield.show()
	drawing.show()
	window.present()
	gtk.main()