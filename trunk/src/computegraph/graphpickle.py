# Reduction Visualizer. A tool for visualization of reduction graphs.
# Copyright (C) 2010 Niels Bjørn Bugge Grathwohl & Jens Duelund Pallesen
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

# Source: http://code.activestate.com/recipes/302535-handling-deeply-nestedrecursive-data/

class TankId(int):
	def __new__(self, i):
		return int.__new__( TankId, i )

class Tank:
	"""
	Temporarily change references to TankId's so as to avoid nesting/recursion.
	Host the client instance and keep track of all reference changes.
	"""
	def __init__(self, root = None):
		" root : client instance to flatten "
		
		self.tankid = TankId(0) # next TankId to use
		
		# map an object's id to a TankId (temporary)
		self.items = {}
		
		# map a TankId to an object
		self.ids = {}
		
		# we are done flattening when this list is empty again
		self.todo = []
		
		if root is not None:
			self.flatten(root)
	
	def __cmp__(self, other):
		if not isinstance(other, Tank):
			return cmp(self, other)
		# all our state is in ids, which is "flat"
		return cmp(self.ids, other.ids)
	
	###########################################
	# before pickle

	def flat_list(self, item):
		for i in xrange(len(item)):
			item[i] = self.queue(item[i])
	
	def flat_set(self, item):
		newitem = set()
		for elem in item:
			newitem.add(self.queue(elem))
		item.clear()
		item.update(newitem)
	
	def flat_dict(self, item):
		for key in item.keys():
			item[key] = self.queue(item[key])
	
	def flat_attrs(self, item):
		for key in item.__dict__.keys():
			item.__dict__[key] = self.queue(item.__dict__[key])
	
	def queue(self, item):
		assert not isinstance(item, TankId)
		if not (isinstance(item, list) or isinstance(item, set) or isinstance(item, dict) or hasattr(item, "__dict__")):
			return item
		if id(item) not in self.items:
			self.todo.append(item)
			tankid = self.tankid
			self.items[id(item)] = tankid
			self.ids[tankid] = item
			self.tankid = TankId(tankid + 1)
		else:
			tankid = self.items[id(item)]
		return tankid
	
	def flatten(self, root):
		'''
		Flatten the root object and all it's references.
		'''
		self.root = root
		self.queue(self.root)
		while self.todo:
			item = self.todo.pop(0)
			if isinstance(item, list):
				self.flat_list(item)
			if isinstance(item, set):
				self.flat_set(item)
			if isinstance(item, dict):
				self.flat_dict(item)
			if hasattr(item, "__dict__"):
				self.flat_attrs(item)
			# tuple ? other immutables ? __set/getstate__ ?
		
		# flush items (do not pickle them)
		self.items = {}
	
	###########################################
	# after pickle
	
	def lift_list(self, item):
		for i in range(len(item)):
			item[i] = self.recover(item[i])
	
	def lift_set(self, item):
		newitem = set()
		for elem in item:
			newitem.add(self.recover(elem))
		item.clear()
		item.update(newitem)
	
	def lift_dict(self, item):
		for key in item.keys():
			item[key] = self.recover(item[key])
	
	def lift_attrs(self, item):
		for key in item.__dict__.keys():
			item.__dict__[key] = self.recover(item.__dict__[key])
	
	def recover(self, item):
		if isinstance(item, TankId):
			item = self.ids[item]
			assert not isinstance(item, TankId)
		return item
	
	def lift(self):
		'''
		Restore the root object to it's un-flattened state.
		'''
		for item in self.ids.values():
			if isinstance(item, list):
				self.lift_list(item)
			if isinstance(item, set):
				self.lift_set(item)
			if isinstance(item, dict):
				self.lift_dict(item)
			if hasattr(item, "__dict__"):
				self.lift_attrs(item)
			# tuple ? other immutables ? __set/getstate__ ?
		
		return self.root