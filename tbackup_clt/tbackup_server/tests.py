# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class RegisterTest(TestCase):

    
    
    def test_retrieve(self):
        from django.test.client import Client
        from tbackup_server.models import Destination
        
        Destination.objects.create(name='test1')
        Destination.objects.create(name='test2')
        Destination.objects.create(name='test3')
        Destination.objects.create(name='test4')
        Destination.objects.create(name='test5')
        Destination.objects.create(name='blabla',
                                   islocal=True,
                                   address='tbackup_server/backups/')
        c = Client()
        response = c.get('/server/retrieve/', 
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        #print response
    
    def test_available(self):
        
        from django.test.client import Client
        from tbackup_server.models import Origin
        
        Origin.objects.create(name='client1')
        Origin.objects.create(name='client2')
        Origin.objects.create(name='client3')
        Origin.objects.create(name='client4')
        Origin.objects.create(name='client5')
        
        #data = {'origin_name': 'client5'}
        data = {'origin_name': 'teste'}
        
        c = Client()
        response = c.post('/server/api/name_available/', data,
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        #print response
            
    def test_register(self):
        import bz2
        import base64
        import os
        from Crypto.Cipher import AES
        from Crypto.PublicKey import RSA
        from Crypto import Random
        from Crypto.Random import random
        from django.utils import simplejson as json
        from django.test.client import Client
        from tbackup_server.models import Origin
        
        #try:
        #    origin = Origin.objects.get(name='lorem ipsum')
        #except Origin.DoesNotExist:
            #origin = Origin.objects.create(name='lorem ipsum')
            #origin.pubkey = public.exportKey()
            #origin.save()
            
        private = RSA.generate(1024, Random.new().read)
        pvtkey = private.exportKey()
        #print pvtkey
        public = private.publickey()
        pubkey = public.exportKey()
        #print pubkey
        info = {
                'origin_name' : 'loren ipsum',
                'origin_pubkey' : pubkey,
               }
        
        with open('tbackup_server/secret.txt', 'r') as f:
            shared_key = bz2.decompress(f.read())
        
        BLOCK_SIZE = 32
        PADDING = '{'
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        DecodeRSA = lambda c, e: c.decrypt(base64.b64decode(e))
        
        cipher = AES.new(shared_key, AES.MODE_ECB)
        
        encrypted_request = {'message': EncodeAES(cipher, json.dumps(info)),}
        c = Client()
        response = c.post('/server/register/', encrypted_request)
        #print response.content
        content = json.loads(response.content)
        #print content
        msg = content['message']
        #print msg
        decoded_msg = base64.b64decode(str(msg))
        #print "decoded_msg = " + decoded_msg
        rsa = RSA.importKey(pvtkey)
        deciphered = rsa.decrypt(decoded_msg)
        #deciphered = DecodeRSA(rsa, msg)
        #print "deciphered = " + deciphered
        import hashlib
        md5 = hashlib.md5()
        md5.update(pubkey)
        #print "md5 da public key = " + md5.hexdigest()
        
        #print "testing..."
        word = {"webserver_pubkey": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDT/0gTAqriI/iWmTRGpxAydFuX\ngPt1oApPIVsY6igfT4VPHdr6gn3/qruKyEYLl3KydsWZlYvsjlbBVB5VllpYFNNt\nD/blKoyfYtkibQUqbbvy9rHIIm/qQ6c3aUbGIzrF8Rl1RUfNdt8KJ2+14FwEdtpJ\nIQ7NV9tja1otTUjYTQIDAQAB\n-----END PUBLIC KEY-----"}
        word = json.dumps(word)
        word = '{"TESTESTESTESTESTESTESTESTE": "blahblahblah"}'
        word = '{"TESTESTESTESTESTESTESTESTE": "blahblahblah"}'
        word = '{"wow": "890123456789MIGfMAaGPIVsY6igfT4VPHoyfYtkibQUqbbvy9rHIIm/qQ6c3aUbGIzrF8Rl1RUfNdt8KJ2+14FwEdtpJIQ7NV9tja1otTUjYTQIDAQAB"}'
        #print "word = " + word
        rsa = RSA.importKey(pubkey)
        ciphered = rsa.encrypt(word, 0)[0]
        #print "ciphered = " + ciphered
        cipherb64 = base64.b64encode(ciphered)
        #print "cipherb64 = " + cipherb64
        recipher = base64.b64decode(cipherb64)
        #print "recipher = " + recipher
        rsa = RSA.importKey(pvtkey)
        #deciphered = rsa.decrypt(ciphered)
        deciphered = rsa.decrypt(recipher)
        #print "deciphered = " + deciphered
        
class FileTest(TestCase):
    
    def test_send(self):
        
        #criando base
        from tbackup_server.models import Destination, Origin
        Destination.objects.create(name='Gruyere - LPS',
                                   islocal=True,
                                   address='tbackup_server/backups/'
                                   )
        
        origin_pubkey = 'blablabla'
        Origin.objects.create(name='Hospital_Guadalupe',
                              pubkey= origin_pubkey,
                               )
        
        #islocal = models.BooleanField(verbose_name='local')
        #address = models.CharField(max_length=1024, verbose_name=u'endereço')    
        #port = models.CharField(max_length=5, verbose_name='porta')
        
        from base64 import b64encode
        from Crypto.Hash import SHA
        sha1 = SHA.new()
        with open('dummy_file', 'rb') as f:
            filename = f.name.split('/')[-1]
            raw_data = str()
            encoded_string = str()
            #9KB(9216) block:
            #- multiple of 16 (2bytes) for sha1 to work in chunks
            #- multiple of 24 (3bytes) for b64encode to work in chunks 
            #- near 8KB for optimal sha1 speed
            for data in iter(lambda: f.read(9216), b''):
                raw_data += data
                encoded_string += b64encode(data)
                sha1.update(data)
            sha1sum = sha1.hexdigest()
            #encoded_string = b64encode(raw_data)
        
        #print 'filename = ' + filename
        #print 'raw_data = ' + raw_data[9000:9010]
        #print 'encoded_string = ' + encoded_string[9000:9010]
           
        message = {
                   'destination' : 'Gruyere - LPS',
                   'file' : encoded_string,
                   'filename' : filename,
                   #'sha1sum': self.get_sha1sum(raw_data),
                   'sha1sum': sha1sum,
                   'origin_pubkey' : origin_pubkey
                   }
        #print 'sha1sum = ' + message['sha1sum']
        
        from django.test.client import Client
        c = Client()
        #print 'posting...'
        response = c.post('/server/backup/', message)
        #print response.content
        
    def get_sha1sum(self, string_data):
        #from hashlib import sha1
        #import cStringIO
        from Crypto.Hash import SHA
        sha1 = SHA.new()
        #s.update()
        #sha1 = sha1();
        #if isinstance(large_string, file):
        #    for data in iter(lambda: fileref.read(8192), b''):
        sha1.update(string_data)
        return sha1.hexdigest()  
