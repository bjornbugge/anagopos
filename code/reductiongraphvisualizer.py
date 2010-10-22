#! /usr/bin/env python
import os
import gtk
import math
import random
import time
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
	
def redraw(widget):
	if drawing.ready:
		drawing.graph.reset()
		drawing.graph.update_layout_animated(iter_animated)
		drawing.queue_draw()
	else:
		print "No graph created yet!"
	
def optimize(widget):
	if drawing.ready:
		drawing.graph.update_layout_animated(iter_animated)
		drawing.queue_draw()
	else:
		print "No graph created yet!"

def initgraph():
	try:
		if hasattr(drawing, 'iterator') and drawing.iterator is not None:
			Drawer = algorithms[drawing.selected]
			rg = drawing.iterator.next()
			g = Drawer(rg)
			drawing.reductiongraphlist = [rg]
			drawing.graph = g
			drawing.graphlist = [g]
			drawing.starttobig = False
	except:
		drawing.starttobig = True

# Going back to the previous graph
def back(widget):
	Drawer = algorithms[drawing.selected]
	drawing.nomoregraphs = False
	if drawing.graphnumber == 0:
		outputtext()
		drawing.firstgraph = True
	else:
		drawing.firstgraph = False
		if hasattr(drawing, 'selectedhaschanged') and drawing.selectedhaschanged:
			drawing.graphnumber -= 1
			rg = drawing.reductiongraphlist[drawing.graphnumber]
			g = Drawer(rg)
			drawing.graphlist[drawing.graphnumber] = g
			drawing.graph = g
			drawing.graph.initwith(drawing.graphlist[drawing.graphnumber + 1])
			outputtext()
			drawing.graph.update_layout_animated(iter_animated)
			drawing.queue_draw()
			# drawing.selectedhaschanged = False
		else:
			drawing.graphnumber -= 1
			drawing.graph = drawing.graphlist[drawing.graphnumber]
			outputtext()
			drawing.graph.update_layout_animated(iter_animated)
			# drawing.queue_draw()
	outputtext()

# Going forward to the next graph
def forward(widget):
	Drawer = algorithms[drawing.selected]
	drawing.firstgraph = False
	if drawing.graphnumber + 2 <= len(drawing.graphlist):
		if hasattr(drawing, 'selectedhaschanged') and drawing.selectedhaschanged:
			drawing.graphnumber += 1
			rg = drawing.reductiongraphlist[drawing.graphnumber]
			g = Drawer(rg)
			drawing.graphlist[drawing.graphnumber] = g
			drawing.graph = g
			drawing.graph.initwith(drawing.graphlist[drawing.graphnumber - 1])
			outputtext()
			drawing.graph.update_layout_animated(iter_animated)
			# drawing.selectedhaschanged = False
		else:
			drawing.graphnumber += 1
			drawing.graph = drawing.graphlist[drawing.graphnumber]
			drawing.graph.initwith(drawing.graphlist[drawing.graphnumber - 1])
			outputtext()
			drawing.graph.update_layout_animated(iter_animated)
	else:
		try:
			rg = drawing.iterator.next()
			g = Drawer(rg)
			drawing.reductiongraphlist.append(rg)
			drawing.graphlist.append(g)
			drawing.graphnumber += 1
			drawing.graph = drawing.graphlist[drawing.graphnumber]
			if type(drawing.graph) is type(drawing.graphlist[drawing.graphnumber - 1]):
				drawing.graph.initwith(drawing.graphlist[drawing.graphnumber - 1])
			outputtext()
			drawing.graph.update_layout_animated(iter_animated)
		except StopIteration:
			drawing.nomoregraphs = True
			outputtext()

# Dictionary with algorithms
algorithms = {'Neato' : NeatoGraph,
			'Neato Animated' : MajorizationGraph,
			'Dot' : DotGraph,
			'TwoPi' : TwopiGraph,
			'Circo' : CircoGraph,
			'Fdp' : FdpGraph}

# Iteration over gtk events making sure the drawing is done animated
def iter_animated():
	sleeptime = 0.00
	if hasattr(drawing, 'selected') and drawing.selected == "Neato Animated":
		while gtk.events_pending():
			gtk.main_iteration(True)
	drawing.queue_draw()
	time.sleep(sleeptime)

# Draw graph function
# Yield function with graphs
def applyiterator(widget):
	try:
		drawing.startnum = int(start.get_text())
		drawing.endnum = 1000000
		tempterm = termtext.get_text(termtext.get_start_iter(),termtext.get_end_iter())
		drawing.term = parser.parse(tempterm.replace(u'\u03bb',"#"))
		drawing.mgs = []
		operations.assignvariables(drawing.term)
		drawing.selected = str(algo.get_child().get_text())
		drawing.startnumber = int(start.get_text())
		try:
			def iterator():
				Drawer = algorithms[drawing.selected]
				for (i,g) in enumerate(operations.reductiongraphiter(drawing.term, drawing.startnum, drawing.endnum)):
					yield g
			drawing.iterator = iterator()
		except KeyError:
			pass
		drawing.graphnumber = 0
		initgraph()
		outputtext()
		drawing.graph.update_layout_animated(iter_animated)
		drawing.ready = True
		if hasattr(drawing, 'starttobig') and drawing.starttobig:
			start.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
		else:
			start.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
		entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
	except NameError as e:
		if hasattr(drawing, 'starttobig') and drawing.starttobig:
			start.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
		elif start.get_text() == "" or termtext.get_text(termtext.get_start_iter(),termtext.get_end_iter()) == "":
			if start.get_text() == "":
				start.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
			else:
				start.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
			if termtext.get_text(termtext.get_start_iter(),termtext.get_end_iter()) == "":
				entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
			else:
				entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
		else:
			print "Syntax error: " + str(e)
			entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))

# Output text for text field in GUI
def outputtext():
	drawing.outputtextstring = ""
	drawing.outputtextstring = drawing.outputtextstring + "Number of nodes: " + str(len(drawing.graph.nodes)) + "\n"
	drawing.outputtextstring = drawing.outputtextstring + "Generation: " + str(drawing.startnumber + drawing.graphnumber) + "\n"
	if hasattr(drawing, 'firstgraph') and drawing.firstgraph:
		drawing.outputtextstring = drawing.outputtextstring + "You are at the first graph" + "\n"
	if hasattr(drawing, 'nomoregraphs') and drawing.nomoregraphs:
		drawing.outputtextstring = drawing.outputtextstring + "No more graphs" + "\n"
	outputtextbuffer.set_text(drawing.outputtextstring)

# Generates pseudo random lambda term
def generateTerm(widget):
	drawing.term = randomgraph.randomterm()
	termtext.set_text(str(drawing.term).replace("#",u'\u03bb'))
	entry.set_tooltip_text(str(drawing.term).replace("#",u'\u03bb'))
	start.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
	entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))

# Listener for drop-down menu when changing drawing algorithm
def changed_cb(entry):
	if hasattr(drawing, 'ready') and drawing.ready:
		try:
			drawing.selectedhaschanged = True
			drawing.selected = entry.get_text()
			Drawer = algorithms[drawing.selected]
			rg = drawing.reductiongraphlist[drawing.graphnumber]
			g = Drawer(rg)
			drawing.graphlist[drawing.graphnumber] = g
			drawing.graph = drawing.graphlist[drawing.graphnumber]
			drawing.graph.update_layout_animated(iter_animated)
			drawing.queue_draw()
		except:
			pass
		drawing.graph.update_layout_animated(iter_animated)
		drawing.queue_draw()

# Keyboard listner when pressing down on key
# Keyboard shortcuts
def key_press_event(widget, event):
	
	if event.keyval == 65507:
		drawing.ctrl = True
	
	if hasattr(drawing, 'ctrl') and drawing.ctrl:
		if hasattr(drawing, 'ctrl') and drawing.ctrl and (event.keyval == 102 or event.keyval == 110): 
			forward(widget)
		elif hasattr(drawing, 'ctrl') and drawing.ctrl and event.keyval == 98 or event.keyval == 112: 
			back(widget)
		elif hasattr(drawing, 'ctrl') and drawing.ctrl and event.keyval == 114:
			redraw(widget)
		elif hasattr(drawing, 'ctrl') and drawing.ctrl and event.keyval == 111:
			optimize(widget)

# Keyboard listner when releasing press on a key
# Keyboard shortcuts
def key_release_event(widget, event):
	if event.keyval == 65507:
		drawing.ctrl = False

# Mouse listner when pressing button
# Listnens if a node is clicked on
def button_press_event(widget, event):
	x = event.x
	y = event.y
	r = 10
	
	drawing.dragareax = event.x - 240
	drawing.dragareay = event.y
	
	drawing.setclickterm = True
	
	if drawing.ready:
		
		scalinecounter = 0
		if drawing.scaling[0] != 1 and drawing.scaling[1] != 1:
			drawing.scalingx = drawing.scaling[0]
			drawing.scalingy = drawing.scaling[1]
			scalinecounter = scalinecounter + 1
		
		for node in drawing.graph.nodes:
			if int(x) in xrange(int(node.x) - r, int(node.x) + r) and int(y) in xrange(int(node.y) - r, int(node.y) + r):
				drawing.graph.dragnode = True
				drawing.graph.dragnodename = node.name
				drawing.graph.dragnodex = x
				drawing.graph.dragnodey = y
				drawing.graph.dragnodenode = node

# Mouse listner when releasing button
# Listnens if a node the same or a different place than where it was clicked
# If the same place: Show node information. Else nothing (means node has been dragged)
def button_release_event(widget, event):
	x = event.x
	y = event.y
	r = 10
	if hasattr(drawing.graph, 'dragnode') and drawing.graph.dragnode:
		
		drawing.graph.dragnodex = x * drawing.scaling[0]
		drawing.graph.dragnodey = y * drawing.scaling[1]
		
		if hasattr(drawing, 'dragupdate') and drawing.dragupdate:
			if hasattr(drawing.graph, 'draggableupdate') and drawing.graph.draggableupdate:
				drawing.graph.dragnodes()
				drawing.dragupdate = False
		drawing.queue_draw()
		drawing.graph.dragnode = False
	
	if drawing.ready and drawing.setclickterm:
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
				clickedtermtemp = str(node.term).replace("#",u'\u03bb')
				clickedterm.set_text(clickedtermtemp)
				entryclickedterm.set_buffer(clickedterm)
				entryclickedterm.set_tooltip_text(clickedtermtemp)
			else:
				node.showterm = False
				for edge in node.children:
					edge.selected = False

# Mouse listner for moving mouse around
# If node has been clicked in "button_press_event(widget, event)"
# then update node position and redraw on every motion
def motion_notify_event(widget, event):
	
	if hasattr(drawing.graph, 'draggable') and drawing.graph.draggable:
		if hasattr(drawing.graph, 'dragnode') and drawing.graph.dragnode:
			
			x = event.x
			y = event.y
			drawing.graph.nodenametable[drawing.graph.dragnodename].x = x
			drawing.graph.nodenametable[drawing.graph.dragnodename].y = y
			
			drawing.setclickterm = False
			
			drawing.dragupdate = True
			drawing.queue_draw()

# Checkbox for highlighting the newest edges in graph
def checkbox(widget, event):
	if newestedges.get_active():
		drawing.shownewestedget = True
	else:
		drawing.shownewestedget = False
	drawing.queue_draw()

# Main function
if __name__ == "__main__":
	window = gtk.Window()
	window.connect("delete-event", gtk.main_quit)
	window.connect("key_press_event", key_press_event)
	window.connect("key_release_event", key_release_event)
	window.resize(1024, 768)
	
	# Graph
	graph = None
	
	# GraphArea
	drawing = GraphArea(graph)
	drawing.ready = False
	drawing.shownewestedget = False
	# Listners for the GraphArea
	drawing.connect("button_release_event", button_release_event)
	drawing.connect("button_press_event", button_press_event)
	drawing.connect("motion_notify_event", motion_notify_event)
	drawing.set_events(gtk.gdk.BUTTON_RELEASE_MASK
						| gtk.gdk.BUTTON_PRESS_MASK
						| gtk.gdk.POINTER_MOTION_MASK)
	
	# Widget boxes
	widgetboxH = gtk.HBox(False, 10)
	widgetboxV = gtk.VBox(False, 10)
	
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
	
	# Text buffer for text view field (for the lambda term)
	termtext = gtk.TextBuffer()
	# Text view field (for the lambda term)
	entry = gtk.TextView()
	entry.set_justification(False)
	entry.set_left_margin(5)
	entry.set_right_margin(5)
	entry.set_size_request(200, 109)
	entry.set_buffer(termtext)
	entry.set_wrap_mode(True)
	entry.set_border_window_size(gtk.TEXT_WINDOW_LEFT,2)
	entry.set_border_window_size(gtk.TEXT_WINDOW_RIGHT,2)
	
	# Text buffer for text view field (output text field)
	outputtextbuffer = gtk.TextBuffer()
	outputtextbuffer.set_text("Output text...")
	# Text view field (output text field)
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
	
	# Text buffer for text view field (clicked term field)
	clickedterm = gtk.TextBuffer()
	clickedterm.set_text("Clicked term...")
	# Text view field (clicked term field)
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
	
	# Text fiels for start generation
	start = gtk.Entry()
	start.set_text("0")
	
	# Checkbox for showing newest edges
	newestedges = gtk.CheckButton(label="Show newest: ")
	newestedges.set_direction(gtk.TEXT_DIR_RTL)
	newestedges.connect("toggled", checkbox, "showstages")
	
	# Drop down for selecting drawing algorithm
	algo = gtk.ComboBoxEntry()
	liststore = gtk.ListStore(str)
	algo.set_model(liststore)
	[liststore.append([k]) for k in algorithms.keys()]
	algo.set_text_column(0)
	algo.set_active(0)
	algo.child.connect('changed', changed_cb)
	
	# Buttons
	b1.connect("clicked", generateTerm)
	b2.connect("clicked", applyiterator)
	b3.connect("clicked", forward)
	b4.connect("clicked", back)
	b5.connect("clicked", redraw)
	b6.connect("clicked", optimize)
	
	# Widget box
	startbox = gtk.HBox(False, 10)
	startbox.pack_start(l1, False, False, 1)
	startbox.pack_start(start, False, False, 1)
	
	# Widget box
	widgetboxV.pack_start(l4, False, False, 1)
	widgetboxV.pack_start(entry, False, False, 1)
	widgetboxV.pack_start(algo, False, False, 1)
	widgetboxV.pack_start(startbox, False, False, 1)
	widgetboxV.pack_start(newestedges, False, False, 1)
	widgetboxV.pack_start(b2, False, False, 1)
	widgetboxV.pack_start(b1, False, False, 1)
	widgetboxV.pack_start(b3, False, False, 1)
	widgetboxV.pack_start(b4, False, False, 1)
	widgetboxV.pack_start(b5, False, False, 1)
	widgetboxV.pack_start(b6, False, False, 1)
	widgetboxV.pack_start(l5, False, False, 1)
	widgetboxV.pack_start(entryclickedterm, False, False, 1)
	widgetboxV.pack_start(l6, False, False, 1)
	widgetboxV.pack_start(outputtextfield, False, False, 1)
	
	# Widget box
	widgetboxH.pack_start(widgetboxV, False, False, 5)
	widgetboxH.pack_end(drawing, True, True, 5)
	
	# Adds widgetboxes to window
	window.add(widgetboxH)
	
	# Shows widgets
	widgetboxV.show()
	startbox.show()
	widgetboxH.show()
	l4.show()
	entry.show()
	b1.show()
	algo.show()
	l1.show()
	start.show()
	newestedges.show()
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