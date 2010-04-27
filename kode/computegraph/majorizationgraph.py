import math
import random
import numpy
import reductiongraph

class MajorizationGraph(reductiongraph.Graph):
	def __init__(self, graph = None, width = 200, height = 200):
		super(reductiongraph.Graph, self).__init__()
		
		self.drawingfunction = None
		self.nodesdict = {}
		self.nodes = []
		
		random.seed()
		
		if not graph is None:
			for (key, node) in graph.nodesdict.iteritems():
				self.nodesdict[key] = node
				self.nodes.append(node)
				node.x = random.randint(1, width)
				node.y = random.randint(1, height)
			
		# self.n = len(self.nodes)
		self.n = 10 # testing
		self.alpha = 2
		self.Lw = self._Lw() # saet den en gang for alle!
		self.L = numpy.linalg.cholesky(self.Lw)
		self.LXt = numpy.mat(numpy.zeros([self.n, self.n]))
		self.dims = 2
		self.Xt = numpy.matrix([[1,2],[1,2],[3,4],[3,5],[5,6],[1,5],[7,5],[9,5],[4,7],[7,3]])
		# self.Xt = numpy.mat(numpy.random.rand(self.n, 2))
		self.Xt[0,:] = [0,0]
		
	def update_layout(self):
		for node in self.nodes:
			pass
	
	def _iter(self):
		solve = numpy.linalg.solve
		
		self.LXt = self._L(self.Xt)
		Xt_new = numpy.mat(numpy.zeros([self.n, self.dims]))
		
		# Ax=b --> Ly=b, L'x=y
		b = self.LXt * self.Xt
		b = b[1:10, :]
		y = solve(self.L, b)
		Xt_new = solve(self.L.T, y)
		
		
		#for a in xrange(self.dims): # two dimensions!
		#	# Ax=b --> Ly=b, L'x=y
		#	b = self.LXt * self.getcolumn(self.Xt, a)
		#	y = solve(self.L.A, b.A)
		#	x = solve(self.L.T.A, y)
		#	for i in xrange(len(Xt_new)):
		#		Xt_new[i, a] = x[i]
		print "Stress: " + str(self.stress())
		self.Xt[1:10, :] = Xt_new
		print self.Xt
	
	def stress(self):
		elms = []
		for i in xrange(self.n):
			for j in xrange(i, self.n):
				elms.append(self._w_ij(i,j) * (self.dist(self.Xt[i], self.Xt[j]) - self._d_ij(i,j))**2)
		return sum(elms)
	
	def dist(self, M1, M2):
		# return numpy.linalg.norm(M1 - M2)
		return math.sqrt((M1[0,0] - M2[0,0])**2 + (M1[0,1] - M2[0,1])**2)

	def inv(self, x):
		if x == 0: return 0
		return 1 / x

	def _L(self, Xt):
		def _L_iks(self, fixpoint):
			Ls = []
			for k in xrange(self.n):
				if k == fixpoint:
					continue
				Ls.append(self.LXt[fixpoint, k]) # TODO er dette rigtigt?
			return Ls
		
		LXt = numpy.mat(numpy.zeros([self.n, self.n]))
		for i in xrange(self.n):
			for j in xrange(self.n):
				if i == j:
					LXt[i, j] = sum(_L_iks(self, i))
				else:
					delta_ij = self._w_ij(i, j) * self._d_ij(i, j)
					LXt[i, j] = delta_ij * self.inv(self.dist(Xt[i], Xt[j]))
		
		# LXt = LXt[1:self.n, 1:self.n]
		return LXt
	
	def _Lw(self):
		def _w_iks(self, fixpoint):
			ws = []
			for k in xrange(self.n):
				if k == fixpoint:
					continue
				ws.append(self._w_ij(fixpoint, k))
			return ws
		
		Lw = numpy.mat(numpy.zeros([self.n, self.n]))
		for i in xrange(self.n):
			for j in xrange(self.n):
				if i == j:
					Lw[i, j] = sum(_w_iks(self, i))
				else:
					w_ij = self._w_ij(i, j)
					Lw[i, j] = -w_ij
		
		Lw = Lw[1:self.n, 1:self.n]
		return Lw
	
	def _w_ij(self, i, j):
		return self._d_ij(i, j)**-self.alpha
	
	def _d_ij(self, i, j):
		# STUB!
		# return 1 + 4 * (1/(i+1) + 1/(j+1))
		return 2 * abs(i-j) + 1
	
	def calc_graph_distances(self):
		pass
		# Compute all-to-all shortest paths and save in a lookup table!
		# Use e.g. Johnson's algorithm (wikipedia)
	
	def iter_done( self ):
		"""
		Placeholder function for calling a screen update
		"""
		if not self.drawingfunction is None:
			self.drawingfunction(self)

		pass
