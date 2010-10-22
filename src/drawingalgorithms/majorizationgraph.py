import pdb
import math
import numpy
import computegraph.shortestpath as SP
from copy import deepcopy
import time
from drawingalgorithm import DrawingAlgorithm

class MajorizationGraph(DrawingAlgorithm):
	'''
	Implementation of Gansner2004-approach.
	'''
	
	# Nodes are draggable, and will update layout
	draggable = True
	draggableupdate = True
	
	def __init__(self, graph, width = 200, height = 200, epsilon = 10**-3):
		# Make sure we inherit all attributes from the graph.
		for name, value in vars(graph).iteritems():
			setattr(self, name, value)
		
		self.calc_epsilon_interval = 10
		
		numpy.random.seed()
		
		# The epsilon value that controls when the node positions are "good".
		self.epsilon = epsilon
		
		self.width = width
		self.height = height
		
		# If self.chol is set to True, the equation system is solved 
		# using a Cholesky decomposition. This makes the algorithm more
		# "robust", removing a lot of cases of NaN-errors and singular matrix
		# situations.
		self.chol = False
		self.current_stress = None
		self.hasBeenInitialized = False
		self.n = len(self.nodes)
		self.drawingfunction = None
		
		# The ratio between weight types used when calculating the D-matrix.
		# Must be between 0 and 1.
		self.alpha = 0.2
		
		# Make the identity once and for all for efficiency.
		self.I = numpy.identity(self.n)
		
		# The matrices needed for the position calculations.
		self.D = self._get_D_matrix()
		self.W = self._get_W_matrix()
		self.Lw = self._laplace(None, lambda x:self.W)
		# Use the Cholesky decomposition!
		self._makechol()
		
		# The delta values needed to compute the Laplacian matrix for the 
		# node positions.
		self.deltas = numpy.multiply(self.W, self.D)
		
		# Save the previous (x,y)-coordinates in Xt_old and the new, current
		# coordinates in Xt. Xt is calculated based on Xt_old.
		self.Xt_old = numpy.mat(numpy.zeros([self.n, 2]))
		self.Xt = numpy.mat(numpy.zeros([self.n, 2]))
		
		# print "Size is " + str(self.n)
	
	def dragnodes(self):		
		# If node is dragged new position will be put into GraphViz graph
		self.calc_epsilon_interval = 1
		self.epsilon = 1
		if hasattr(self, 'dragnode') and self.dragnode:
			normX = self.norm.getA()[0][0]
			normY = self.norm.getA()[0][1]
			
			nodepos = self.nodes.index(self.dragnodenode)
			
			self.Xt[nodepos, 0] = self.dragnodex - normX
			self.Xt[nodepos, 1] = self.dragnodey - normY
		
		self.update_layout()
		
	def reset(self, f = 0):
		if f == 0:
			self.Xt[:, 0] = self.width * numpy.random.random([self.n, 1])
			self.Xt[:, 1] = self.height * numpy.random.random([self.n, 1])
		elif type(f) is list:
			r = numpy.random.random([len(f), 2])
			r[:,0] = self.width * r[:,0]
			r[:,1] = self.height * r[:,1]
			self.Xt[f] = r
		self.hasBeenInitialized = True
	
	def initwith(self, othergraph):
		m = len(othergraph.nodes)
		names = [n.name for n in self.nodes]
		new = range(self.n)
		for i, n in enumerate(othergraph.nodes):
			try:
				j = names.index(n.name)
				self.Xt[j] = othergraph.Xt[i]
				new.remove(j)
			except ValueError:
				pass
		
		self.reset(new)
		self._assignnodepositions()
		self.hasBeenInitialized = True
	
	# Scales the node positions to fit the GTK GraphArea
	def scale(self, width, height):
		Xs = [node.x for node in self.nodes]
		Ys = [node.y for node in self.nodes]
		scaling = [max(Xs) / (width - 50), max(Ys) / (height - 50)]
		self.scaling = scaling
		
		for node in self.nodes:
			node.x = (float(node.x) / scaling[0])
			node.y = (float(node.y) / scaling[1])
			
			if not hasattr(self, 'bezier') or not self.bezier:
				continue
			
			for edge in node.children:
				for i, point in enumerate(edge.ipoints):
					edge.ipoints[i] = map(lambda x:float(x[0]) / x[1], zip(point, scaling))
					
		return scaling
	
	def update_layout(self):
		if not self.hasBeenInitialized:
			self.reset()
		
		e = 1000
		numits = 0
		
		while e > self.epsilon:
			self._iter()
			self._iter_done()
			numits += 1
			if numits % self.calc_epsilon_interval == 0:
				e = self._calc_epsilon()
				if math.isnan(e):
					# When the graph is small, with one node, the cholesky 
					# decomposition cannot be performed. In this case we run 
					# the risk of seeing singular matrices. If that happens,
					# we just lay the nodes randomly out.
					self.reset()
		self._assignnodepositions()
		
	def update_layout_animated(self, f):
		self.drawingfunction = f
		self.update_layout()
	
	def _makechol(self):
		'''
		Compute the node positions using a Cholesky decomposition.
		'''
		if self.n == 1:
			self.chol = False
			return
		self.Lw = self.Lw[1:, 1:]
		self.Lw = numpy.linalg.cholesky(self.Lw)
		self.chol = True
	
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
		self.norm = abs(self.Xt.min(0))
		X = deepcopy(self.Xt + self.norm)
		return X
	
	def _iter(self):
		solve = numpy.linalg.solve
		Xt_new = numpy.mat(numpy.zeros([self.n, 2]))
		
		LXt = self._get_L(self.Xt)
		
		b = LXt * self.Xt
		if self.chol:
			b = b[1:]
		try:
			if self.chol:
				y = solve(self.Lw, b)
				x = solve(self.Lw.T, y)
				a = numpy.mat(numpy.zeros([self.n, 2]))
				a[1:] = x
				x = a
			else:
				x = solve(self.Lw, b)
			Xt_new = x
			self.Xt_old = deepcopy(self.Xt)
			self.Xt = Xt_new
		except Exception as e:
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
		meshgrid = numpy.meshgrid
		M1, M2 = meshgrid(X[:,0], X[:,0])
		M3, M4 = meshgrid(X[:,1], X[:,1])
		return numpy.sqrt(squared(M1 - M2) + squared(M3 - M4))
	
	def _stress(self, X):
		dists = self._ata_dists(X)
		E = numpy.multiply(self.W, numpy.power(dists - self.D, 2))
		return E.sum() / 2 # Because we only look at those elms. with i>j we divide by two
	
	def _get_L(self, Z):
		def func(M):
			dists = self._ata_dists(M)
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
		(D, A) = self._get_graph_distances()
		W = numpy.mat(numpy.zeros([self.n, self.n]))
		#print self.n
		if not self._compute_distances():
			self.alpha = 1
		else:
			if self.alpha > 0.0:
				for i in xrange(self.n):
					for j in xrange(i + 1, self.n):
						Ni = set(self.nodes[i].parents + self.nodes[i].children)
						Nj = set(self.nodes[j].parents + self.nodes[j].children)
						W[i,j] = W[j,i] = 1 + (len(Ni.union(Nj)) - len(Ni.intersection(Nj)))
			else:
				self.alpha = 0.0
		return ((1 - self.alpha) * D) + (self.alpha * W)
	
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
			self.drawingfunction()