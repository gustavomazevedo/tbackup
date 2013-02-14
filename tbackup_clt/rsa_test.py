from Crypto import Random
from Crypto.PublicKey import RSA

private = RSA.generate(1024, Random.new().read)
public = private.publickey()
print private.exportKey().replace('\n','\\n')
print public.exportKey().replace('\n','\\n')
