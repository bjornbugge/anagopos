import gtk
import cairo
import math
import time

class GraphArea(gtk.DrawingArea):
	__gsignals__ = {
		"expose-event": "override",
		"configure_event": "override",
	}
	
	# Init
	def __init__ ( self, mgs ):
		gtk.DrawingArea.__init__(self)
		self.graphlist = []
		self.graphnumber = 0
		self.graph = None
		self.small_radius = 5
		self.medium_radius = 10
		self.large_radius = 15
		self.arrow_color = (1.0, 36.0 / 255.0, 0.0)
		self.newest_edge_color = (34.0/255.0,139.0/255.0,34.0/255.0)
		self.normal_edge_color = (0/255.0, 100.0/255.0, 245.0/255.0)
		self.first_node_color = (0, 100.0, 127.0/255.0)
		self.newest_edge_width = 3
		self.normal_edge_width = 1
		self.selected_edge_width = 5
		self.normal_form_color = (0xa4/255.0, 0, 0)
		self.newest_node_color = (34.0/255.0,139.0/255.0,34.0/255.0)
		self.normal_node_color = (0, 0, 0)
		self.scaling = None
	
	# gtk function
	def do_configure_event ( self, event ):
		self.__width, self.__height = self.window.get_size()
		self.queue_draw()
	
	# gtk function
	def do_expose_event ( self, event ):
		self.__cr = self.window.cairo_create()
		self.__render()
	
	# cairo render function
	def __render( self ):
		if not self.graph:
			return
		
		self.scaling = self.graph.scale(self.__width, self.__height)
		self.__cr.rectangle(0,0,self.__width, self.__height)
		self.__cr.set_source_rgb(1,1,1)
		self.__cr.fill()
		
		# drawing edges
		noEdges = 0
		for node in self.graph.nodes:
			for edge in node.children:
				
				noEdges = noEdges + 1
				if (node is self.graph.newest) and self.shownewestedget:
					w = self.newest_edge_width 
					c = self.newest_edge_color
				else:
					w = self.normal_edge_width
					c = self.normal_edge_color
				self.__cr.set_line_width(w)
				self.__cr.set_source_rgb(c[0], c[1], c[2])
				
				if hasattr(edge, 'selected') and edge.selected:
					self.__cr.set_line_width(self.selected_edge_width)
				
				far_node = edge.get_far(node)
				
				if hasattr(self.graph, 'bezier') and self.graph.bezier:
					# Draw a bezier line
					
					# Don't draw a bezier curve if it's going to the same node as it came from.
					if edge.destination == node:
						continue
					
					destX = edge.destination.x
					destY = edge.destination.y
					
					lastX = edge.ipoints[len(edge.ipoints) - 1][0]
					lastY = edge.ipoints[len(edge.ipoints) - 1][1]
					
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
					
					x1 = edge.ipoints[len(edge.ipoints)-1][0]
					y1 = edge.ipoints[len(edge.ipoints)-1][1]
					x2 = far_node.x
					y2 = far_node.y
				else:
					# Draw a straight line
					self.__cr.move_to(node.x, node.y)
					self.__cr.line_to(far_node.x, far_node.y)
					self.__cr.stroke()
					
					x1 = node.x
					y1 = node.y
					x2 = far_node.x
					y2 = far_node.y
				
				# different node sizes
				if len(far_node.term.redexpositions) == 0:
					radius = self.large_radius
				elif node is self.graph.newest:
					radius = self.medium_radius
				else:
					radius = self.small_radius
				
				# arrowheads
				if node != edge.get_far(node):
					self.draw_arrowhead(x1, y1, x2, y2, radius)
				
		# drawing nodes
		for node in self.graph.nodes:
			if len(node.term.redexpositions) == 0:
				radius = self.large_radius
				color = self.normal_form_color
			elif (node is self.graph.newest) and self.shownewestedget:
				radius = self.medium_radius
				color = self.newest_node_color
			elif node.name == "N0":
				radius = self.medium_radius
				color = self.first_node_color
			else:
				radius = self.small_radius
				color = self.normal_node_color
			
			
			self.__cr.arc(node.x, node.y, radius, 0, math.pi*2)
			self.__cr.set_source_rgb(color[0], color[1], color[2])
			self.__cr.fill_preserve()
			self.__cr.set_source_rgb(0, 0, 0)
			self.__cr.stroke()
			
			for edge in node.children:
				if node == edge.get_far(node):
					
					size = 5
					ac = self.arrow_color
					self.__cr.set_line_width(1)
					self.__cr.set_source_rgb(ac[0], ac[1], ac[2])
					self.__cr.move_to(node.x-size,node.y-size)
					self.__cr.line_to(node.x+size,node.y-size)
					self.__cr.stroke_preserve()
					self.__cr.line_to(node.x+size,node.y+size)
					self.__cr.stroke_preserve()
					self.__cr.line_to(node.x-size,node.y+size)
					self.__cr.stroke_preserve()
					self.__cr.line_to(node.x-size,node.y-size)
					self.__cr.stroke_preserve()
					self.__cr.fill()
			
			if hasattr(node, 'showterm') and node.showterm:
				parsedtermlist = str(node.term).split('#')
				parsedterm = ""
				lambdaletter = u'\u03bb'
		self.nomoregraphs = False
	
	# arrowhead drawing function
	def draw_arrowhead(self, x1, y1, x2, y2, noderadius):
		'''
		Draws an arrow head on the line segment between the coordinate pairs
		(x1,y1) and (x2,y2). The arrow head is placed in the (x2,y2)-end.
		'''
		arrowwidth = 10
		Pi = math.pi
		angle = 20
		
		if x1 - x2 == 0:
			if y2 <= y1:
				LineAngle = Pi / 2
			else:
				LineAngle = 3 * Pi / 2
		else:
			LineAngle = math.atan((y2 - y1) / (x2 - x1))
	
		EndAngle1 = LineAngle + angle * Pi/180
		EndAngle2 = LineAngle - angle * Pi/180
	
		xOffset = noderadius * math.cos(LineAngle)
		yOffset = noderadius * math.sin(LineAngle)
		if x1 < x2:
			Y3 = y2 - arrowwidth * math.sin(EndAngle1)
			Y4 = y2 - arrowwidth * math.sin(EndAngle2)
			X3 = x2 - arrowwidth * math.cos(EndAngle1)
			X4 = x2 - arrowwidth * math.cos(EndAngle2)
			
			x2 -= xOffset
			y2 -= yOffset
			Y3 -= yOffset
			Y4 -= yOffset
			X3 -= xOffset
			X4 -= xOffset
		else:
			Y3 = y2 + arrowwidth * math.sin(EndAngle1)
			Y4 = y2 + arrowwidth * math.sin(EndAngle2)
			X3 = x2 + arrowwidth * math.cos(EndAngle1)
			X4 = x2 + arrowwidth * math.cos(EndAngle2)
			x2 += xOffset
			y2 += yOffset
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
	
# calculates the binomial coefficient
def binomial(n, i):
	bin = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
	return bin

# calculated the bezier lines
def drawBezierGen(t, l, ipoints):
	n = l - 1
	fun = lambda a, b:a + b
	x = reduce(fun, (binomial(n, i) * pow((1 - t), n - i) * pow(t, i) * ipoints[i][0] for i in xrange(l)))
	y = reduce(fun, (binomial(n, i) * pow((1 - t), n - i) * pow(t, i) * ipoints[i][1] for i in xrange(l)))
	return [x, y]