#!/usr/bin/env python
#coding:utf-8

from node import Node
from ore import ORESMALL as ORE

class EncryptedNode(Node):
	value = None
	def __init__(self,x):
		# super(SimpleNode,self).__init__(x)
		self.value = x
		
	def compare(self,x):
		# Compares x with self
		# if super(SimpleNode,self).value == x:
		return ORE.compare(x[0], self.value[1])