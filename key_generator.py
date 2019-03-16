"""
Module used to create and return an API key and a public identifier for that key.
"""
import hashlib
import os

#Constants to define the size of the API secret key and the public identifier.
API_KEY_LENGTH = 40
ID_KEY_LENGTH = 20

def create_key_pair():
    #TODO: replace this magic numbers with configuration
    #TODO: add exception handling
    api_key = create_api_key(20)
    identifier = create_api_key_identifier(10)
    #Why return a tuple? why not JSONify the keys?
    return (api_key, identifier)

#Generate a new API key. Bits is an int defining the number of random bits
# to request from the underlying source of entropy. 
def create_api_key(bits):
    random_bits = os.urandom(bits)
    #TODO: strategy pattern opportunity here when I convert this to OOP
    # option of using different secure ciphers
    sha = hashlib.sha256()
    sha.update(random_bits)
    sha_output = sha.hexdigest()
    #Impose constrains on size of API key in case API_KEY_SIZE is modified
    # What happens if this assert fails?
    assert(API_KEY_SIZE <= len(sha_output) and API_KEY_LENGTH > 10)
    key = sha_output[:API_KEY_LENGTH]
    #What happens if the function call fails before this return statement?
    return key

#Change this approach => hash the api key and modify it? Rather than drawing on entropy pool more
def create_api_key_identifier(bits):
    random_bits = os.urandom(bits)
    #TODO: replace this implementation. Keep interface the same.
    md = hashlib.md5()
    md.update(random_bits)
    output = md.hexdigest()[:ID_KEY_LENGTH]
    key = output.upper()
    return key
    
    


def entropy_health_check():
    return
