#!/usr/bin/env python
#coding: utf-8
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
import base64
import hashlib
import numpy
import os,binascii
from numpy.random import randint
from random import Random
from operator import xor
from math import log
from multiprocessing import Pool
from Crypto.Random import atfork
import time

FAST = True
if FAST:
    from sha256prf import SHA256PRF as PRF
else:
    from aesdet import AESDet as PRF

to_int = lambda x: int(hashlib.sha256(x).hexdigest(),16)

# F  => PRF: AES-128
# pi => PRP: IntPerm 
# H  =>HASH: SHA256

# cmp
orecmp = lambda a,b: (-1)*(a < b) + (1)*(a > b)

# Hash
H = lambda x,y: int(hashlib.sha256(x+y).hexdigest(),16) % 3
# PRP
PRP = lambda a,b,d: a*b % d
PRPInv = lambda a,b,d: pow(a,d-2)*b % d

class OREBIG():
    d = None
    n = None
    F1 = PRF()
    F2 = PRF()

    def __init__(self,sk=None):
        if sk is not None:
            # Load keys and the PRP
            k1,k2 = sk

            # Load the master secret key
            self.F1 = PRF()
            self.F1.add_to_private_key("key",k1)
            self.F2 = PRF()
            self.F2.add_to_private_key("key",k2)


    # Generates two keys using a PRF
    # message space size N > 0
    # d-ary strings x = x_1x_2x_3...x_n
    def keygen( self, passphrase,d = 71, n = 30 , N = 70):
        self.n = n
        # keys
        k1 = PRF.keygen(passphrase+"1")
    	k2 = PRF.keygen(passphrase+"2")

        #sk
        sk = (k1,k2)
        self.d = d
        self.n = n
        assert pow(d,n) >= N

        # Load the master secret key
        self.F1 = PRF()
        self.F1.add_to_private_key("key",k1)
        self.F2 = PRF()
        self.F2.add_to_private_key("key",k2)

    	return sk

    def encryptL( self, x ):
        assert type(x) in (str,unicode)
        assert len(x) == self.n

        #
        u = [None]*self.n
        # for each i in [n]
        for i in range(self.n):
            # x_{|i-1}
            seqs = x[:i] if i > 0 else ""
            f2enc_seqs = self.F2.encrypt(seqs)

            # pi.map_to \equiv \pi
            # pi.map_from \equiv \pi^{-1}
            xhat = PRP(to_int(f2enc_seqs), ord(x[i]), self.d)
            u[i] = self.F1.encrypt(seqs + str(xhat)), xhat
    	return u

    def encryptR( self, y ):
        assert type(y) in (str,unicode)
        assert len(y) == self.n

        # Nonce sampling
        r = binascii.b2a_hex(os.urandom(128))

        #
    	v = [None]*self.n

        # for each i in [n]
        for i in range(self.n):
            u = [None]*self.d

            # y_{|i-1}
            seqs = y[:i] if i > 0 else ""
            f2enc_seqs = self.F2.encrypt(seqs)
            for j in range(self.d):
                jstar = PRPInv(to_int(f2enc_seqs), j, self.d)
                zij = (orecmp(jstar, ord(y[i])) + H( self.F1.encrypt(seqs + str(j)), r )) % 3
                u[j] = zij
            v[i] = u
    	return [r] + v

    def encrypt( self, y):
        assert len(y) == self.n
        return (self.encryptL(y), self.encryptR(y))

    @staticmethod
    def compare( ctL, ctR ):
        global H

        u = ctL
        r,v = ctR[0],ctR[1:]

        n = len(u)
        # for i in [n]
        for i in range(n):
            kli,hi = u[i]
            vi = v[i]

            result = (vi[hi] - H(kli, r)) % 3
            if result != 0:
                return result % 3
        return 0

def main():

    ore = OREBIG()
    ore.keygen("oi",d=127,n=5)

    # Generating test dataset
    k = 100
    dataset = ["".join([chr(randint(65,127)) for _ in range(5)]) for _ in range(k)]
    fail = 0

    print "Starting...",
    for i,s in enumerate(zip(dataset[::2],dataset[1::2])):
        print i
        s1 = s[0]
        s2 = s[1]
        print "s1: %s\ns2: %s" % (s1,s2)

        r = (0 if s1 == s2 else (2 if s1 < s2 else 1))
        # import pdb; pdb.set_trace()
        start =time.time()
        ctS1 = ore.encrypt(s1)
        ctS2 = ore.encrypt(s2)
        end = time.time()
        print "%f seconds to encrypt" % ((end-start)/2)

        start =time.time()
        ret = OREBIG.compare(ctS1[0],ctS2[1])
        end = time.time()
        print "%f seconds to compare" % ((end-start)/2)
        print "Expected: %d. Received: %d\n" % (r,ret)
        if r != ret:
            fail = fail + 1

    print "Done"

    print "%d failure rate" % (fail)
    if fail == 0:
        print "All tests passed!"

if __name__ == "__main__":
    main()