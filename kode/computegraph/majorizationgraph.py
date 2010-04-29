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
		self.nodesdict = {}
		self.nodes = []
		self.width = width
		self.height = height
		random.seed() # Fixed
		
		if not graph is None:
			for (key, node) in graph.nodesdict.iteritems():
				self.nodesdict[key] = node
				self.nodes.append(node)
				node.x = random.randint(1, width)
				node.y = random.randint(1, height)
		
		self.n = len(self.nodes)
		
		self.I = numpy.identity(self.n)
		self.alltoalldistances = self._get_graph_distances()
		self.D = self._get_D_matrix()
		self.W = self._get_W_matrix()
		self.deltas = self._get_delta_matrix()

		self.Lw = self.laplace(None, lambda x:self.W)
		self.Xt = numpy.mat(numpy.zeros([self.n, 2]))
		self.Xt_old = numpy.mat(numpy.zeros([self.n, 2]))
		for i in xrange(self.n):
			n = self.nodes[i]
			self.Xt[i,0] = n.x
			self.Xt[i,1] = n.y
		#self.Xt[0,:] = [0,0]
		#self.chol()
		self.epsilon = 10**-3
		self.adjacency = self.adjacencymatrix()
		self.current_stress = None
	
	def chol(self):
		self.L = numpy.linalg.cholesky(self.Lw[1:, 1:])
	
	def adjacencymatrix(self):
		A = numpy.mat(numpy.zeros([self.n, self.n]))
		for (i, v) in enumerate(self.nodes):
			for e in v.children + v.parents:
				w = e.get_far(v)
				j = self.nodes.index(w)
				A[i, j] = 1
		return A
	
	def update_layout(self):
		e = 1000
		numits = 0
		while e > self.epsilon:
			self._iter()
			if numits % 50 == 0:
				e = self.calc_epsilon()
				print "Epsilon: " + str(e)
				print "Stress:  " + str(self.current_stress)
			numits += 1
		print "Number of iterations: " + str(numits)
		self.normalize()
		# Assign calculated positions to nodes
		for (i, node) in enumerate(self.nodes):
			node.x = self.Xt[i, 0]
			node.y = self.Xt[i, 1]
	
	def update_layout_animated(self, f):
		# dummy
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
		
		# Hvorfor er den her metode en lille smule hurtigere end Cholesky-
		# metoden nedenunder?
		b = LXt * self.Xt
		x = solve(self.Lw, b)
		Xt_new = x
		
		# Cholesky-metoden... (?)
		#b = LXt * self.Xt
		#b = b[1:, :]
		#y = solve(self.L.A, b.A)
		#x = solve(self.L.T.A, y)
		#Xt_new[1:, :] = x
		
		self.Xt_old = deepcopy(self.Xt)
		self.Xt = Xt_new
	
	def ata_dists(self, X):
		squared = lambda x:numpy.power(x, 2)
		M1, M2 = numpy.meshgrid(X[:,0], X[:,0])
		M3, M4 = numpy.meshgrid(X[:,1], X[:,1])
		return numpy.sqrt(squared(M1 - M2) + squared(M3 - M4))
			
	def stress(self, X):
		squared = lambda x:numpy.power(x, 2)
		W = self.W
		D = self.D
		dists = self.ata_dists(X)
		E = numpy.multiply(W, squared(dists - D))
		return E.sum() / 2 # Because we only look at those elms. with i<j we divide by two
	
#	def _get_Lw(self):
#		def func(M):
#			return self.W
#		return self.laplace(None, func)
	
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
	
	def _get_delta_matrix(self):
		return numpy.multiply(self.W, self.D)
		
	def _get_W_matrix(self):
		W = numpy.mat(numpy.zeros([self.n, self.n]))
		for i in xrange(self.n):
			for j in xrange(self.n):
				if i == j:
					continue
				k = 1/2
				# k = min(self.width, self.height) / (max(int(self.alltoalldistances.max()), 1))
				# k = 10
				W[i, j] = k / (self.D[i, j]**2)
		return W
	
	def _get_D_matrix(self):
		return self.alltoalldistances
		
	def _get_graph_distances(self):
		'''
		Computes the all-to-all shortest distances and returns them in a 
		lookup table.
		'''
		alltoalldistances = numpy.mat(numpy.zeros([self.n, self.n]))
		atadists = SP.alltoall_shortest(self)
		for ((v, w), dist) in atadists.iteritems():
			i = self.nodes.index(v)
			j = self.nodes.index(w)
			#if not self.alltoalldistances[j, i] == 0:
			#	dist = -1 * dist
			alltoalldistances[i, j] = dist
		return alltoalldistances
	
	def iter_done(self):
		'''
		Placeholder function for calling a screen update
		'''
		if not self.drawingfunction is None:
			self.drawingfunction(self)
