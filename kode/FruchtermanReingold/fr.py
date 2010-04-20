class Edge:
	def __init__( self, source, destination ):
		self.source_node = source
		self.destination_node = destination
		random.seed()
		self.weight = 0

	def get_far( self, node ):
			if self.source_node == node:
				return self.destination_node
			else:
				return self.source_node

class Node:
	def __init__( self ):
		random.seed()
		self.x = random.randint(1,200)
		self.y = random.randint(1,200)
		self.parents = []
		self.children = []

	def add_child( self, node ):
			edge = Edge( self, node)
			node.parents.append(edge)
			self.children.append(edge)
# 
# class Graph:
# 	def __init__( self ):
# 		self.nodes = []
# 		self.spring = 1
# 		self.max_passes = 5000
# 		self.min_epsilon = 1
# 		self.updates = 1
# 		self.pad = 10
# 		self.width = 200
# 		self.height = 200