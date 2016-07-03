#!/usr/bin/env python
#coding:utf-8

from node import Node

class IndexNode(Node):
	value = None
	_id = []

	def __init__(self,value,_id):
		# super(SimpleNode,self).__init__(x)
		self.value = value
		self._id = self._id + (_id if _id in (list,tuple) else [_id])
		
	def compare(self,other):
		if type(other) in (list,tuple):
			x = other[0] # gambiarra
		else:
			x = other # gambiarra
		# Compares x with self
		# if super(SimpleNode,self).value == x:
		if self.value == x:
			return 0
		# elif super(SimpleNode,self).value < x:
		elif self.value < x:
			return 1
		# elif super(SimpleNode,self).value > x:
		elif self.value > x:
			return 2