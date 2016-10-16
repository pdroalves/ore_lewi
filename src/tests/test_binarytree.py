#!/usr/bin/env python
#coding:utf-8

import unittest
from binarytree import BinaryTree
from simplenode import SimpleNode
from random import randint,shuffle
# from ore import ORESMALL as ORE
from oresbig import OREBIG as ORE

RUNS = 80

class BinaryTreeTest(unittest.TestCase):
	def setUp(self):
		"""Setup"""
		self.N = 100

	def test_insert(self):
		"""Test insertion on the tree"""
		for _ in xrange(RUNS):
			elements = range(self.N)
			shuffle(elements)
			root = BinaryTree(elements[0])

			for e in elements[1:]:
				self.assertEqual(root.insert(e).me.value,e)

	def test_find(self):
		"""Verify if elements were really inserted on the tree"""
		for _ in xrange(RUNS):
			elements = range(self.N)
			shuffle(elements)
			root = BinaryTree(elements[0])

			# Insert
			for i,e in enumerate(elements[1:]):
				self.assertEqual(root.insert(e).me.value,e)

			# Verify in
			for i,e in enumerate(elements):
				self.assertIsNotNone(root.find(e))
				self.assertEqual(root.find(e).me.value, e)

			# Verify not in
			for e in range(self.N+1,self.N*2):
				self.assertIsNone(root.find(e))

	def test_encrypt(self):
		"""Verify encryption capabilities"""
		for _ in xrange(RUNS):
			elements = range(1,self.N)
			shuffle(elements)
			root = BinaryTree(elements[0])

			for e in elements[1:]:
				root.insert(e)

			ore = ORE()
			ore.keygen("oi",self.N)
			ore.encrypt(10)
			root.encrypt(ore)

			a = ore.encrypt(elements[0]-1)
			b = ore.encrypt(elements[0])
			c = ore.encrypt(elements[0]+1)

			self.assertEqual(root.me.compare(a),2)
			self.assertEqual(root.me.compare(b),0)
			self.assertEqual(root.me.compare(c),1)

	def test_encrypt_find(self):
		"""Verify encryption capabilities"""
		for _ in xrange(RUNS):
			elements = range(1,self.N)
			shuffle(elements)
			root = BinaryTree(elements[0])

			for e in elements[1:]:
				root.insert(e)

			ore = ORE()
			ore.keygen("oi",self.N)
			root.encrypt(ore)

			for e in elements[1:]:
				self.assertIsNotNone(root.find(ore.encrypt(e)))
				self.assertEqual(root.find(ore.encrypt(e)).mecopy.value, e)

    	
if __name__ == "__main__":
	print "Testing binary tree class"
	unittest.main()