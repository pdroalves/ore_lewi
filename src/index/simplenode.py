#!/usr/bin/env python
#coding:utf-8

from node import Node

class SimpleNode(Node):
	value = None
	balance = 0
	parent = None
	
	def __init__(self,x):
		# super(SimpleNode,self).__init__(x)
		self.value = x
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