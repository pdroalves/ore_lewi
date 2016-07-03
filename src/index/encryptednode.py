#!/usr/bin/env python
#coding:utf-8

from node import Node
from crypto.ore import ORESMALL as ORE

class EncryptedNode(Node):
	value = None
	index = None
	def __init__(self,value,index=None):
		# super(SimpleNode,self).__init__(x)
		self.value = value
		self.index = index
		
	def compare(self,x):
		# Compares x with self
		# if super(SimpleNode,self).value == x:
		return ORE.compare(x, self.value)