#!/usr/bin/env python
#coding:utf-8

from node import Node
from crypto.ore import ORESMALL as ORE

class EncryptedNode(Node):
	value = None
	_id = None
	def __init__(self,value,_id=None):
		# super(SimpleNode,self).__init__(x)
		self.value = value
		self._id = _id
		
	def compare(self,x):
		# Compares x with self
		# if super(SimpleNode,self).value == x:
		return ORE.compare(x, self.value)