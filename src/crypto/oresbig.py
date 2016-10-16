#!/usr/bin/env python
#coding:utf-8
import base64
import hashlib
import numpy
import os,binascii
from random import randint
from random import Random
from operator import xor
from aesdet import AESDet as PRF
from urpint import URPINT as URP
from math import log
from multiprocessing import Pool
from Crypto.Random import atfork

# F  => PRF: AES-128
# pi => PRP: IntPerm 
# H  =>HASH: SHA256

H = lambda x,y: int(hashlib.sha256(x+y).hexdigest(),16) % 3
to_int = lambda x: int(hashlib.sha256(x).hexdigest(),16)
orecmp = lambda a,b: (-1)*(a < b) + (1)*(a > b)

PRP = lambda a,b,d: a*b % d
PRPInv = lambda a,b,d: pow(a,d-2)*b % d

def innerEncryptR(args):
    atfork()

    j = int(args[0])
    f2enc_seqs = args[1][0]
    d = int(args[1][1])
    k1 = args[1][2]
    y = args[1][3]
    seqs = str(args[1][4])
    r = args[1][5]

    F1 = PRF()
    F1.add_to_private_key("key",k1)

    jstar = PRPInv(to_int(f2enc_seqs), j, d)
    zij = (orecmp(jstar, ord(y)) + H( F1.encrypt(seqs + str(j)), r )) % 3
    return zij

class OREBIG():
    d = None
    n = None


    # Generates two keys using a PRF
    # message space size N > 0
    # d-ary strings x = x_1x_2x_3...x_n
    def keygen( self, passphrase,d = 71, n = 30 , N = 70):
        self.n = n
        # keys
        k1 = PRF.keygen(passphrase+"1")
    	k2 = PRF.keygen(passphrase+"2")

        # PRP
        pi = URP(n=d,seed=42) # pi(a,b) = PRP(a)*b

        #sk
        sk = (k1,k2,pi)
        self.d = d
        self.n = n
        assert pow(d,n) >= N

    	return sk

    def encryptL( self, sk, x ):
        assert type(x) in (str,unicode)
        assert len(x) == self.n

        # Load keys and the PRP
        k1,k2,pi = sk
        pi.refresh()

        # Load the master secret key
        F1 = PRF()
        F1.add_to_private_key("key",k1)
        F2 = PRF()
        F2.add_to_private_key("key",k2)

        #
        u = [None]*self.n

        # import pdb;pdb.set_trace()
        # for each i in [n]
        for i in range(self.n):

            # x_{|i-1}
            seqs = x[:i] if i > 0 else ""
            f2enc_seqs = F2.encrypt(seqs)

            # pi.map_to \equiv \pi
            # pi.map_from \equiv \pi^{-1}
            # xhat  = pi.map_to  ( (to_int(f2enc_seqs) +ord(x[i])) % self.d ) % self.d
            xhat = PRP(to_int(f2enc_seqs), ord(x[i]), self.d)
            u[i] = F1.encrypt(seqs + str(xhat)), xhat

    	return u

    def encryptR( self, sk, y ):
        assert type(y) in (str,unicode)
        assert len(y) == self.n

        # Load keys and the PRP
        k1,k2,pi = sk
        pi.refresh()

        # Nonce sampling
        r = binascii.b2a_hex(os.urandom(128))

        # Load the master secret key
        F1 = PRF()
        F1.add_to_private_key("key",k1)
        F2 = PRF()
        F2.add_to_private_key("key",k2)

        #
    	v = [None]*self.n
        p = Pool()

        # import pdb;pdb.set_trace()
        # for each i in [n]
        for i in range(self.n):
            u = [None]*self.d
            # y_{|i-1}
            seqs = y[:i] if i > 0 else ""
            f2enc_seqs = F2.encrypt(seqs)
            # import pdb;pdb.set_trace()
            args = zip(range(self.d),[[f2enc_seqs,self.d,k1,y[i],seqs,r]]*self.d)
            v[i] = p.map(innerEncryptR,args)
    	return [r] + v

    def encrypt( self, y, sk):
        assert len(y) == self.n
        return (self.encryptL(sk, y), self.encryptR(sk, y))

    @staticmethod
    def compare( ctL, ctR ):
        global H

        u = ctL
        r,v = ctR[0],ctR[1:]

        # import pdb;pdb.set_trace()
        n = len(u)
        # for i in [n]
        for i in range(n):
            kli,hi = u[i]
            vi = v[i]

            # import pdb;pdb.set_trace()
            result = (vi[hi] - H(kli, r)) % 3
            if result != 0:
                return result % 3
        return 0

ore = OREBIG()
sk = ore.keygen("oi")

for i in range(10000):
    print i
    s1 = "".join([chr(randint(65,71)) for _ in range(30)])
    s2 = "".join([chr(randint(65,71)) for _ in range(30)])

    r = (0 if s1 == s2 else (2 if s1 < s2 else 1))
    # import pdb; pdb.set_trace()
    ctS1 = ore.encrypt(s1,sk)
    ctS2 = ore.encrypt(s2,sk)

    print "Expected: %d. Received: %d" % (r,OREBIG.compare(ctS1[0],ctS2[1]))
    # assert r == OREBIG.compare(ctS1[0],ctS2[1])

print "%d failure rate" % (fail)
if fail == 0:
    print "All tests passed!"