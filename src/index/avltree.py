#!/usr/bin/env python
#coding:utf-8

# About this class:
# 
# - It has two pointers: left and right
# 	* left points to AVLTree elements compared as lower than the root
# 	* right points to AVLTree elements compared as bigger than the root
# - The element "me" is the real content of this node
# - This doesn't build a balanced tree
#
from index.simplenode import SimpleNode
from index.encryptednode import EncryptedNode
from index.indexnode import IndexNode
from crypto.ore import ORESMALL as ORE

class AVLTree:
	left = None
	right = None
	me = None
	mecopy = None
	nodeclass = None
	balance = 0
	parent = None

	def __init__(self,me,nodeclass=SimpleNode):
		self.me = nodeclass(me[0],me[1])
		self.mecopy = nodeclass(me[0],me[1])
		self.nodeclass = nodeclass
		parent = None

	def is_leaf(self):
		if self.left == None and self.right == None:
			return True
		else:
			return False
	def which_child(self,x):
		# Returns -1 if x is the left child		
		# Returns 1 if x is the right child		
		# Returns 0 if x is not a child
		
		if x == self.left:
			return -1
		elif x == self.right:
			return 1
		else:
			return 0

	# Receives an element comparable to "me"
	def find(self, x):
		r = self.me.compare(x)
		if self.is_leaf() and r != 0:
			# There is no element compatible to x in this tree
			return None
		elif r == 0:
			# This is the element we look for
			return self
		elif r == 2 and self.left is not None:
			# This element is bigger than x
			# x < self
			return self.left.find(x)
		elif r == 1  and self.right is not None:
			# This element is lower than x
			# x > self
			return self.right.find(x)
		else:
			return None

	# Receives an element comparable to "me"
	def insert(self,x):
		r = self.me.compare(x)
		if r == 0:
			# The element already exists in the tree
			if self.nodeclass == IndexNode:
				self.me._id = [x[1]] + self.me._id
			return self.get_root()
		elif r == 2:
			# This element is bigger than x
			# x < self
			if self.left is None:
				# This is a leaf. Elevates it to a subtree and 
				# add x to the left pointer
				self.left = AVLTree(x,nodeclass=self.nodeclass)
				self.left.parent = self
				self.left.update_balance()
				return self.left.get_root()
			else:
				return self.left.insert(x)
		elif r == 1:
			# This element is lower than x
			# x > self
			if self.right is None:
				# This is a leaf. Elevates it to a subtree and 
				# add x to the right pointer
				self.right = AVLTree(x,nodeclass=self.nodeclass)
				self.right.parent = self
				self.right.update_balance()
				return self.right.get_root()
			else:
				return self.right.insert(x)

	def get_root(self):
		if self.parent is not None:
			return self.parent.get_root()
		return self

	def encrypt(self,ore):
		ct = ore.encrypt(self.me.value)
		self.me = EncryptedNode(ct,self.me._id)

		if self.left is not None:
			self.left.encrypt(ore)
		if self.right is not None:
			self.right.encrypt(ore)

	def get_height(self):
		if self.is_leaf():
			return 0
		if self.left is not None:
			left_height = self.left.get_height()+1
		else:
			left_height = 0
		if self.right is not None:
			right_height = self.right.get_height()+1
		else:
			right_height = 0

		return left_height-right_height

	def is_balanced(self):
		return True if self.get_height() in (-1,0,1) else False

	def update_balance(self):
		# if not self.is_balanced():
		if self.balance > 1 or self.balance < -1:
			self.rebalance()
			return

		if self.parent is not None:
			if self.parent.which_child(self) == -1:
				# This is a left child
				self.parent.balance = self.parent.balance + 1 
			elif self.parent.which_child(self) == 1:
				# This is a right child
				self.parent.balance = self.parent.balance - 1

			if self.parent.balance != 0:
				self.parent.update_balance()

	def rebalance(self):
		if self.balance < 0:
			if self.right and self.right.balance >  0:
				self.right.right_rotation()
				self.left_rotation()
			else:
				self.left_rotation()
		elif self.balance > 0:
			if self.left and self.left.balance < 0:
				self.left.left_rotation()
				self.right_rotation()
			else:
				self.right_rotation()

	def left_rotation(self):
		# the right child becomes the parent, 
		# the old parent becomes the left child
		if self.right is None:
			print "This should not happen"
			return

		side = self.parent.which_child(self) if self.parent else 0
		parent = self.parent
		self.parent = self.right
		self.parent.parent = parent
		if side == -1:
			# left
			self.parent.parent.left = self.parent
		elif side == 1:
			# right
			self.parent.parent.right = self.parent

		aux = self.parent.left
		self.parent.left = self
		self.right = aux

		self.balance = self.balance + 1 - min(self.parent.balance,0)
		self.parent.balance = self.parent.balance + 1 + max(self.balance,0)


	def right_rotation(self):		
		# the left child becomes the parent, 
		# the old parent becomes the right child
		if self.left is None:
			print "This should not happen"
			# import pdb;pdb.set_trace()
			return

		side = self.parent.which_child(self) if self.parent else 0
		parent = self.parent
		self.parent = self.left
		self.parent.parent = parent
		if side == -1:
			# left
			self.parent.parent.left = self.parent
		elif side == 1:
			# right
			self.parent.parent.right = self.parent

		aux = self.parent.right
		self.parent.right = self
		self.left = aux

		self.balance = self.balance + 1 - min(self.parent.balance,0)
		self.parent.balance = self.parent.balance + 1 + max(self.balance,0)

	def count_nodes(self):
		count = 1
		if self.left:
			count = count + self.left.count_nodes()
		if self.right:
			count = count + self.right.count_nodes() 		
		return count