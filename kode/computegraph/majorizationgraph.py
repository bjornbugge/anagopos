import pdb
import sys
import math
import random
import numpy
import reductiongraph
import shortestpath as SP
from copy import deepcopy

class MajorizationGraph(reductiongraph.Graph):
	def __init__(self, graph = None, width = 200, height = 200):
		super(reductiongraph.Graph, self).__init__()
		
		self.drawingfunction = None
		self.nodesdict = graph.nodesdict
		self.nodes = graph.nodes
		self.width = width
		self.height = height
		random.seed()
		
		if not graph is None:
			for (key, node) in graph.nodesdict.iteritems():
				node.x = random.randint(1, width)
				node.y = random.randint(1, height)
		
		self.n = len(self.nodes)
		
		self.I = numpy.identity(self.n)
		self.D = self._get_D_matrix()
		self.W = self._get_W_matrix()
		self.deltas = numpy.multiply(self.W, self.D)
		
		self.Lw = self.laplace(None, lambda x:self.W)
		self.Xt_old = numpy.mat(numpy.zeros([self.n, 2]))
		self.Xt = numpy.mat(numpy.zeros([self.n, 2]))
		for i in xrange(self.n):
			self.Xt[i,0] = self.nodes[i].x
			self.Xt[i,1] = self.nodes[i].y
		self.epsilon = 10**-3
		self.current_stress = None
	
	def update_layout(self):
		e = 1000
		numits = 0
		while e > self.epsilon:
			self._iter()
			if numits % 50 == 0:
				e = self.calc_epsilon()
				print "Epsilon: " + str(e)
				print "Stress:  " + str(self.current_stress)
				self.iter_done()
			numits += 1
		print "Number of iterations: " + str(numits)
		self.normalize()
		# Assign calculated positions to nodes
		for (i, node) in enumerate(self.nodes):
			node.x = self.Xt[i, 0]
			node.y = self.Xt[i, 1]
	
	def update_layout_animated(self, f):
		self.drawingfunction = f
		self.update_layout()
	
	def calc_epsilon(self):
		self.current_stress = self.stress(self.Xt)
		s = self.stress(self.Xt_old)
		return (s - self.current_stress) / s
	
	def normalize(self):
		# Translate
		self.Xt += abs(self.Xt.min(0))
		# Scale
		norm = self.Xt / self.Xt.max(0)
		self.Xt[:, 0] = norm[:, 0] * self.width
		self.Xt[:, 1] = norm[:, 1] * self.height
	
	def _iter(self):
		solve = numpy.linalg.solve
		Xt_new = numpy.mat(numpy.zeros([self.n, 2]))
		
		LXt = self._get_L(self.Xt)
		
		b = LXt * self.Xt
		x = solve(self.Lw, b)
		Xt_new = x
				
		self.Xt_old = deepcopy(self.Xt)
		self.Xt = Xt_new
	
	def ata_dists(self, X):
		squared = lambda x:numpy.power(x, 2)
		M1, M2 = numpy.meshgrid(X[:,0], X[:,0])
		M3, M4 = numpy.meshgrid(X[:,1], X[:,1])
		return numpy.sqrt(squared(M1 - M2) + squared(M3 - M4))
			
	def stress(self, X):
		squared = lambda x:numpy.power(x, 2)
		dists = self.ata_dists(X)
		E = numpy.multiply(self.W, squared(dists - self.D))
		return E.sum() / 2 # Because we only look at those elms. with i<j we divide by two
	
	def _get_L(self, Z):
		def func(M):
			dists = self.ata_dists(M)
			dists = (1 / (dists + self.I)) - self.I # Perform inversion
			return numpy.multiply(self.deltas, dists)
		
		return self.laplace(Z, func)
		
	def laplace(self, M, f):
		L = f(M)
		D = numpy.multiply(self.I, numpy.sum(L, axis=0))
		return D - L
	
	def _get_W_matrix(self):
		k = 1
		W = k / (numpy.power(self.D + self.I, 2)) - (k * self.I)
		return W
	
	def _get_D_matrix(self):
		D = self._get_graph_distances()
		W = numpy.mat(numpy.zeros([self.n, self.n]))
		N = numpy.mat(numpy.zeros([self.n, self.n])) # Neighbour?
		isn = 1
		isnn = 5
		k = 0.8
		for i in xrange(self.n):
			for j in xrange(i, self.n):
				Ni = set(self.nodes[i].parents + self.nodes[i].children)
				Nj = set(self.nodes[j].parents + self.nodes[j].children)
				W[i,j] = k * (len(Ni.union(Nj)) - len(Ni.intersection(Nj)))
				W[j,i] = k * (len(Ni.union(Nj)) - len(Ni.intersection(Nj)))
				#or e in Ni:
				#   if e.get_far(self.nodes[i]) == self.nodes[j]:
				#   	# print "is neighbour"
				#   	N[i,j] = isn
				#   	N[j,i] = isn
				#   else:
				#   	# print "is not neighbour"
				#   	N[i,j] = isnn
				#   	N[j,i] = isnn
		return numpy.multiply(D, W)
		# return W
		# return numpy.multiply(N, W)
		# return D
		
	def _get_graph_distances(self):
		'''
		Computes the all-to-all shortest distances and returns them in a 
		lookup table.
		'''
		alltoalldistances = numpy.mat(numpy.zeros([self.n, self.n]))
		atadists = SP.alltoall_shortest(self)
		print "Converting distances to matrix form..."
		for ((v, w), dist) in atadists.iteritems():
			i = self.nodes.index(v)
			j = self.nodes.index(w)
			alltoalldistances[i, j] = dist
		return alltoalldistances
	
	def iter_done(self):
		'''
		Placeholder function for calling a screen update
		'''
		if not self.drawingfunction is None:
			self.drawingfunction(self)
