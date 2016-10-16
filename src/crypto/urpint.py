#!/usr/bin/env python
#coding:utf-8
from Crypto import Random
import random

class URPINT:
	def __init__(self,n=16, state=None,seed=42):
		self.n = n
		if state is None:
			random.seed(seed)
			self.rndstate = random.getstate()
		else:
			random.setstate(state)

		self.perm_indexes = [None]*n
		self.inv_perm_indexes = [None]*n
		original_indexes = range(n)
		# This guarantee we will build a new index map with unique values and 
		# different from the original map
		while 1 == 1:
			for i in range(self.n):
				new_index = random.randint(0,self.n-1)
				while new_index in self.perm_indexes:
					new_index = random.randint(0,self.n-1)
				self.perm_indexes[i] = new_index
			if self.perm_indexes != original_indexes:
				break
			else:
				perm_indexes = [None]*self.n

		# Build the inverse map
		for i,v in enumerate(self.perm_indexes):
			self.inv_perm_indexes[v] = i

	def get_int(self,start,end):
		return random.randint(start,end)

	def get_initial_state(self):
		return self.rndstate
	
	def get_state(self):
		return random.getstate()
	
	def set_state(self,state):
		random.setstate(state)

	def refresh(self):
		self.set_state(self.get_initial_state())

	def map_to(self,x):
		return self.perm_indexes[x]
		#return x

	def map_from(self,y):
		return self.inv_perm_indexes[y]
		#return y

if __name__ == "__main__":

	urp = URPINT()
	for i in range(1,16):
		print i
		y = urp.map_to(i)
		assert urp.map_from(y) == i

	print "Test passed!"
