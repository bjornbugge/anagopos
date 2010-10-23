# Reduction Visualizer. A tool for visualization of reduction graphs.
# Copyright (C) 2010 Niels Bjoern Bugge Grathwohl and Jens Duelund Pallesen
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as NP

def adjacencymatrix(G):
	'''
	Compute and return the adjacency matrix for the graph G.
	'''
	n = len(G.nodes)
	A = NP.zeros([n, n])
	for (i, v) in enumerate(G.nodes):
		for e in v.parents + v.children:
			j = G.nodes.index(e.get_far(v))
			A[i, j] = 1
	return A

def floydwarshal(G):
	'''
	Computes the all-pairs shortest paths D and the adjacency matrix A and
	returns them in a tuple (D, A) as NumPy-arrays.
	'''
	# Initialise the estimates from nodes and edges.
	n = len(G.nodes)
	A = adjacencymatrix(G)
	# Set all distances to "infinite", except those between adjacent nodes.
	D = NP.ones([n, n]) * (2 * n + 1)
	D[A == 1] = 1
	# Run the main loop of the algorithm.
	for k in xrange(n):
		for i in xrange(n):
			for j in xrange(i, n):
				D[i, j] = min(D[i, j], D[i, k] + D[k, j])
	
	# Set the diagonal to zeros.
	D = D - D.diagonal() * NP.identity(n)
	# Copy the upper triangle matrix to the lower.
	T = NP.tri(n)
	D = NP.multiply(D, T.T) + NP.multiply(D.T, T)
	return (D, A)

def seidel(G):
	'''
	Implementation of the algorithm from 
	"On the All-Pairs-Shortest-Path Problem"
	by Raimund Seidel, (1992) (24th ANNUAL ACM STOC)
	Returns (D, A) where D is the all-pairs-distances and A the adjacency
	matrix of the graph G.
	@inproceedings{129784,
	 author = {Seidel, Raimund},
	 title = {On the all-pairs-shortest-path problem},
	 booktitle = {STOC '92: Proceedings of the twenty-fourth annual ACM symposium on Theory of computing},
	 year = {1992},
	 isbn = {0-89791-511-9},
	 pages = {745--749},
	 location = {Victoria, British Columbia, Canada},
	 doi = {http://doi.acm.org/10.1145/129712.129784},
	 publisher = {ACM},
	 address = {New York, NY, USA},
	 }
	'''
	I = NP.identity(len(G.nodes))
	def _APD(A):
		n = len(A)
		Z = NP.dot(A, A)
		B = NP.zeros([n, n])
		
		# (a_ij == 1 or z_ij > 0) ==> b_ij = 1
		B[A == 1] = 1
		B[Z > 0] = 1
		
		# Set diagonal to zeros
		B = B - B.diagonal() * I
		
		# If b_ij == 1, i different than j then return.
		if (B + I).all():
			return 2 * B - A
		T = _APD(B)
		X = NP.dot(T, A)
		
		degrees = NP.sum(A, axis=1)
		
		# If x_ij >= t_ij * d_j
		# then d_ij = 2 * t_ij
		# else d_ij = 2 * t_ij - 1
		S = NP.ones([n, n])
		S[X >= T * NP.transpose(degrees)] = 0
		D = 2 * T - S
		
		return D
	
	A = adjacencymatrix(G)
	return (_APD(A), A)




if __name__ == '__main__':
	def testtime(numits):
		from timeit import Timer
		t1 = Timer("seidel(g)", "from shortestpath import *")
		t2 = Timer("floydwarshal(g)", "from shortestpath import *")
		print "With seidel():\t\t %.2f usec/pass" % (numits * t1.timeit(number=numits)/numits)
		print "With floydwarshal():\t %.2f usec/pass" % (numits * t2.timeit(number=numits)/numits)
	
	import reductiongraph as RG
	import lambda_dag as LD
	g = RG.Graph()
	t1 = LD.Application()
	t1.add(LD.Variable('v0'))
	t1.add(LD.Variable('v1'))
	t2 = LD.Abstraction()
	t2.add(LD.Variable('v0'))
	t3 = LD.Abstraction()
	t3_1 = LD.Application()
	t3_1.add(LD.Variable('v0'))
	t3_1.add(LD.Variable('v1'))
	t3.add(t3_1)
	t4 = LD.Application()
	t4_1 = LD.Abstraction()
	t4_1.add(LD.Variable('v0'))
	t4_1.add(LD.Variable('v1'))
	t4.add(t4_1)
	t4.add(LD.Variable('v3'))
	
	n1=g.addnode(t1)
	n2=g.addnode(t2)
	n3=g.addnode(t3)
	n4=g.addnode(t4)
	n1.addchild(n2)
	n2.addchild(n3)
	n1.addchild(n4)
	
	v0 = g.nodes[0]