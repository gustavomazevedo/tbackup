# -*- coding: utf-8 -*-

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


#class sha1(SHA):
#    pass
#
#class aes(AES):
#    pass
#
#class rsa(RSA):
#    pass


def generate_rsa_keys(size):
    private = RSA.generate(size, Random.new().read)
    return private.exportKey(), private.publickey().exportKey()
