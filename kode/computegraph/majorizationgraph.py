import pdb
import math
import numpy
import reductiongraph as RG
import shortestpath as SP
from copy import deepcopy
import time
from drawingalgorithm import DrawingAlgorithm

class MajorizationGraph(DrawingAlgorithm, RG.Graph):
	'''
	Implementation of Gansner2004-approach.
	'''
	def __init__(self, graph, width = 200, height = 200, epsilon = 10**-3):
		for name, value in vars(graph).iteritems():
			setattr(self, name, value)
		
		self.drawingfunction = None
		self.width = width
		self.height = height
		numpy.random.seed()
		
		self.n = len(self.nodes)
		print "Size is " + str(self.n)
		self.I = numpy.identity(self.n)
		self.D = self._get_D_matrix()
		self.W = self._get_W_matrix()
		self.deltas = numpy.multiply(self.W, self.D)
		self.chol = False
		self.Lw = self._laplace(None, lambda x:self.W)
		self.Xt_old = numpy.mat(numpy.zeros([self.n, 2]))
		self.Xt = numpy.mat(numpy.zeros([self.n, 2]))
		self.reset()
		# self._makechol()
		self.epsilon = epsilon
		self.current_stress = None


	
	def _makechol(self):
		self.Lw = self.Lw[1:, 1:]
		self.Lw = numpy.linalg.cholesky(self.Lw)
		# self.W = self.W[1:, 1:]
		# self.D = self.D[1:, 1:]
		self.chol = True
	
	def reset(self, f = 0):
		self.Xt[f:, 0] = self.width * numpy.random.random([self.n - f, 1])
		self.Xt[f:, 1] = self.height * numpy.random.random([self.n - f, 1])
		if self.chol:
			self.Xt[0,:] = [0, 0]
	
	def initwith(self, othergraph):
		m = len(othergraph.nodes)
		self.Xt[0:m, :] = othergraph.Xt
		self.reset(m)
		self._assignnodepositions()
	
	def scale(self, width, height):
		pass
	
	def update_layout(self):
		e = 1000
		numits = 0
		while e > self.epsilon:
			self._iter()
			self._iter_done()
			numits += 1
			if numits % 10 == 0:
				e = self._calc_epsilon()
				if math.isnan(e):
					print "OHHH SHIIIITTT!"
					self.reset(clearstate = False)
				
		#print "Epsilon: " + str(e)
		#print "Stress:  " + str(self.current_stress)
		#print "Number of iterations: " + str(numits)
		self._assignnodepositions()
		
	def update_layout_animated(self, f):
		self.drawingfunction = f
		self.update_layout()
	
	def _assignnodepositions(self):
		X = self._normalize()
		# Assign calculated positions to nodes
		for (i, node) in enumerate(self.nodes):
			node.x = X[i, 0]
			node.y = X[i, 1]
	
	def _calc_epsilon(self):
		self.current_stress = self._stress(self.Xt)
		s = self._stress(self.Xt_old)
		return (s - self.current_stress) / s
	
	def _normalize(self):
		# Translate
		X = deepcopy(self.Xt + abs(self.Xt.min(0)))
		# Scale
		norm = X / X.max(0)
		X[:, 0] = norm[:, 0] * self.width
		X[:, 1] = norm[:, 1] * self.height
		return X
	
	def _iter(self):
		solve = numpy.linalg.solve
		Xt_new = numpy.mat(numpy.zeros([self.n, 2]))
		
		LXt = self._get_L(self.Xt)
		
		#print str(LXt.shape)
		#print str(self.Xt.shape)
		b = LXt * self.Xt
		if self.chol:
			b = b[1:]
		try:
			if self.chol:
				y = solve(self.Lw, b)
				x = solve(self.Lw.T, y)
				a = numpy.mat(numpy.zeros([self.n, self.n]))
				a[1:, 1:] = x
				x = a
			else:
				x = solve(self.Lw, b)
			Xt_new = x
			self.Xt_old = deepcopy(self.Xt)
			self.Xt = Xt_new
		except:
			print b
			print self.Lw
			print self.D
			print "SINGULAR MATRIX!!!"
		
	
	def _ata_dists(self, X):
		'''
		Computes the all-to-all distances in a N*2 matrix of (x,y)-coordinates.
		Returns a N*N matrix with (Euclidean) distances.
		'''
		squared = lambda x:numpy.power(x, 2)
		M1, M2 = numpy.meshgrid(X[:,0], X[:,0])
		M3, M4 = numpy.meshgrid(X[:,1], X[:,1])
		return numpy.sqrt(squared(M1 - M2) + squared(M3 - M4))
	
	def _stress(self, X):
		dists = self._ata_dists(X)
		if self.chol:
			pass
			
		E = numpy.multiply(self.W, numpy.power(dists - self.D, 2))
		return E.sum() / 2 # Because we only look at those elms. with i>j we divide by two
	
	def _get_L(self, Z):
		def func(M):
			dists = self._ata_dists(M)
			#print str(dists.shape)
			#print str(self.I.shape)
			#print str(self.deltas.shape)
			dists = (1 / (dists + self.I)) - self.I # Perform inversion
			
			return numpy.multiply(self.deltas, dists)
		
		return self._laplace(Z, func)
	
	def _laplace(self, M, f):
		L = f(M)
		D = numpy.multiply(self.I, numpy.sum(L, axis=0))
		return D - L
	
	def _get_W_matrix(self):
		A = SP.adjacencymatrix(self)
		k = A.sum(axis=0).max()
		W = k / (numpy.power(self.D + self.I, 2)) - (k * self.I)
		return W
	
	def _get_D_matrix(self):
		t = time.time()
		(D, A) = self._get_graph_distances()
		print "D took: " + str(time.time() - t)
		W = numpy.mat(numpy.zeros([self.n, self.n]))
		if not self._compute_distances():
			alpha = 1
		else:
			if self.n > 180:
				alpha = 0.3
				t = time.time()
				for i in xrange(self.n):
					for j in xrange(i + 1, self.n):
						Ni = set(self.nodes[i].parents + self.nodes[i].children)
						Nj = set(self.nodes[j].parents + self.nodes[j].children)
						W[i,j] = W[j,i] = 1 + (len(Ni.union(Nj)) - len(Ni.intersection(Nj)))

				print "W took: " + str(time.time() - t)
			else:
				alpha = 0.0
		
		# return numpy.multiply(D, W)
		# return D
		# D = numpy.power(D, 2)
		return ((1 - alpha) * D) + (alpha * W)
		# return D
		# return 1 / D.max() * D
	
	def _get_graph_distances(self):
		if not self._compute_distances():
			# A = SP.adjacencymatrix(self)
			A = 0
			return (A, numpy.mat(numpy.ones([self.n, self.n])))
		return SP.seidel(self)
	
	def _compute_distances(self):
		return True
	
	def _iter_done(self):
		'''
		Placeholder function for calling a screen update
		'''
		if not self.drawingfunction is None:
			self._assignnodepositions()
			self.drawingfunction(self)
