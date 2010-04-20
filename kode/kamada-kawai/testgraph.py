import gtk
import math
import cairo
import time
from graph import Graph
from graph import Node

class TestGraph(gtk.DrawingArea, Graph):
	__gsignals__ = {
		"expose-event": "override",
		"configure_event": "override",
	}

	def __init__ ( self ):
		gtk.DrawingArea.__init__(self)
		Graph.__init__(self)
		node1 = Node()
		node2 = Node()
		node3 = Node()
		node4 = Node()
		node5 = Node()
		node6 = Node()
		node7 = Node()
		node1.add_child(node2)
		node2.add_child(node3)
		node3.add_child(node1)
		node2.add_child(node7)
		node7.add_child(node6)
		node7.add_child(node5)
		node2.add_child(node4)
		node4.add_child(node6)
		node5.add_child(node2)
		node6.add_child(node5)
		self.nodes.append(node1)
		self.nodes.append(node2)
		self.nodes.append(node3)
		self.nodes.append(node4)
		self.nodes.append(node5)
		self.nodes.append(node6)
		self.nodes.append(node7)

	def do_configure_event ( self, event ):
		(self.__width, self.__height) = self.window.get_size()
		self.queue_draw()
		
	def do_expose_event ( self, event ):
		print "exposing"
		self.__cr = self.window.cairo_create()
		self.__render()

	def iter_done( self ):
		print "drawing" 
		while gtk.events_pending():
			gtk.main_iteration(False)		
		self.queue_draw()
		time.sleep(0.03)

	def __render( self ):
		self.__cr.rectangle(0,0,self.__width, self.__height)
		self.__cr.set_source_rgb(1,1,1)
		self.__cr.fill()

		self.__cr.save()
		self.__cr.set_source_rgb(0,0,0)
		for node in self.nodes:
			for edge in node.children:
				far_node = edge.get_far(node)
				self.__cr.move_to(node.x, node.y)
				self.__cr.line_to(far_node.x, far_node.y)
				self.__cr.stroke()
		self.__cr.restore()

		self.__cr.save()
		for node in self.nodes:
			print node.x
			self.__cr.arc(node.x, node.y, 5, 0, math.pi*2)
			self.__cr.set_source_rgb(0xcc/255.0, 0, 0)
			self.__cr.fill_preserve()
			self.__cr.set_source_rgb(0xa4/255.0, 0, 0)
			self.__cr.stroke()
		self.__cr.restore()

def update_layout( widget, testgraph ):
	testgraph.update_layout()

if __name__ == "__main__":
	window = gtk.Window()
	window.connect("delete-event", gtk.main_quit)
	width = 500
	height = 500
	window.resize(width, height)

	testgraph = TestGraph()

	update_button = gtk.Button("Organise graph")
	update_button.connect("clicked", update_layout, testgraph)

	vbox = gtk.VBox(False, 10)
	vbox.pack_start(testgraph, True, True, 0)
	vbox.pack_start(update_button, False, False, 0)

	window.add(vbox)

	testgraph.show()
	vbox.show()
	update_button.show()
	window.present()
	gtk.main()

