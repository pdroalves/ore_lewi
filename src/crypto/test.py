#!/usr/bin/env python

# import sys
# sys.setrecursionlimit(100000)
from binarytree import BinaryTree
from simplenode import SimpleNode
from encryptednode import EncryptedNode
from random import randint,shuffle
from ore import ORESMALL as ORE
N = 1000
elements = range(1,N)
# shuffle(elements)
root = BinaryTree(elements[0])

print "Insertion..."
for i,e in enumerate(elements[1:]):
	# %timeit root.insert(e)
	root = root.insert(e)
# print "The tree has %d elements and is %s" % (root.count_nodes(), "balanced" if root.is_balanced() else "not balanced")
# print "Searching..."
# for i in elements[1:]:
# 	# print i
# 	assert root.find(i)
# print "It passed!"
# %timeit root.find(30)

print "Time to test encryption..."
elements = range(1,N)
# shuffle(elements)
ore = ORE()
ore.keygen("oi",N)
print "keygen ok"
root.encrypt(ore)
print "The tree is encrypted"

print "Searching..."
root.find(ore.encrypt(99))
print "Done"


see = lambda x: "%s => %s %s" % (x.me.value, x.left.me.value if x.left else None, x.right.me.value if x.right else None)
# (self.me.value, self.left.me.value if self.left else None, self.right.me.value if self.right else None)