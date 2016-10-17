#!/usr/bin/env python
#coding:utf-8
#
# Copyright (C) 2016 - Pedro G. M. R. Alves - pedro.alves at ic.unicamp.br
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
#
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