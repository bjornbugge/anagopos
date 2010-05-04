import numpy as NP

def dijkstra(G, v0):
	def comparison(x, y):
		if x[1] < y[1]: return -1
		if x[1] == y[1]: return 0
		return 1
	def hasmore(D): return max(D.items(), key=lambda x:x[1])[1]
	
	Q = {}
	for n in G.nodes:
		Q[n] = True
	F = []
	L = {}
	for node in Q:
		L[node] = 2 * len(Q) # "Infinity"
	L[v0] = 0
	
	while hasmore(Q):
		v = None
		l = L.items()
		list.sort(l, cmp=comparison)
		for (v, label) in l:
			if Q[v]: break
		F.append((v, L[v]))
		Q[v] = False
		for edge in v.children + v.parents:
			w = edge.get_far(v)
			weight = 1 # Fixed weights
			if Q[w]:
				L[w] = min(L[w], L[v] + weight)
	return F

def alltoall_shortest(G):
	distances = {}
	V = G.nodes
	for v in V:
		d = dijkstra(G, v)
		# d.remove((v, 0))
		for (w, dist) in d:
			if w == v:
				continue
			distances[(v, w)] = dist
	return distances


if __name__ == '__main__':
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