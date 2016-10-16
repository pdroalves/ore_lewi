#!/usr/bin/env python
#coding:utf-8
import base64
from cipher import Cipher
from Crypto import Cipher as CryptoCipher
from Crypto import Random
# from Crypto.Hash import SHA256
import hashlib

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class SHA256PRF(Cipher):
    __map = {}

    # Generates a key using a hash of some passphrase
    @staticmethod
    def keygen(passphrase, secure=128):
        # if secure == 256:
        #     h = SHA256.new()
        # elif secure == 512:
        #     h = SHA256.new()
        # else:
        #     raise Exception("Unsupported security level")
        # h.update(passphrase)
        # return h.hexdigest()
        return hashlib.sha256(passphrase).digest()

    def encrypt( self, raw ):
        return hashlib.sha256(raw).digest()
