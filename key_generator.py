"""
Module used to create and return an API key and a public identifier for that key.
"""
import hashlib
import os

#Constants to define the size of the API secret key and the public identifier.
API_KEY_SIZE = 40
ID_KEY_SIZE = 20

#Generate a new private key. Bits is an int defining the number of random bits
# to request from the underlying source of entropy. 
def create_api_key(bits):
    random_bits = os.urandom(bits)
    #TODO: strategy pattern opportunity here when I convert this to OOP
    # option of using different secure ciphers
    sha = hashlib.sha256()
    sha.update(random_bits)
    sha_output = sha.hexdigest()
    #Impose constrains on size of API key in case API_KEY_SIZE is modified
    assert(API_KEY_SIZE <= len(sha_output) and API_KEY_SIZE > 10)
    key = sha_output[:API_KEY_SIZE]
    return key

#Change this approach => hash the api key and modify it? Rather than drawing on entropy pool more
def create_api_key_identifier(bits):
    random_bits = os.urandom(bits)
    #TODO: replace this implementation. Keep interface the same.
    md = hashlib.md5()
    md.update(random_bits)
    output = md.hexdigest()[:ID_KEY_SIZE]
    key = output.upper()
    return key

def entropy_health_check():
    return
