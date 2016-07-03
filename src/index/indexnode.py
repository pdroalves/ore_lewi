#!/usr/bin/env python
#coding:utf-8

from node import Node

class IndexNode(Node):
	value = None
	index = None

	def __init__(self,value,index):
		# super(SimpleNode,self).__init__(x)
		self.value = value
		self.index = index
		
	def compare(self,x):
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