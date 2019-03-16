"""
Module used to create and return an API key and a public identifier for that key.
"""
import hashlib
import os
import subprocess

class APIKeyGenerator():
    def __init__(self, api_key_length, id_key_length, req_min_entropy):
        #Constants to define the size of the API secret key and the public identifier.
        self.API_KEY_LENGTH = api_key_length
        self.ID_KEY_LENGTH = id_key_length
        self.REQUIRED_MIN_ENTROPY = req_min_entropy

    #Generate a new API key. Bits is an int defining the number of random bits
    # to request from the underlying source of entropy. 
    def create_api_key(self, bits):
        random_bits = os.urandom(bits)
        #TODO: strategy pattern opportunity here when I convert this to OOP
        # option of using different secure ciphers
        sha = hashlib.sha256()
        sha.update(random_bits)
        sha_output = sha.hexdigest()
        #Impose constrains on size of API key in case API_KEY_SIZE is modified
        # What happens if this assert fails?
        assert(self.API_KEY_LENGTH <= len(sha_output) and self.API_KEY_LENGTH > 10)
        key = sha_output[:self.API_KEY_LENGTH]
        #What happens if the function call fails before this return statement?
        return key

    #Change this approach => hash the api key and modify it? Rather than drawing on entropy pool more
    def create_api_key_identifier(self, bits):
        random_bits = os.urandom(bits)
        #TODO: replace this implementation. Keep interface the same.
        md = hashlib.md5()
        md.update(random_bits)
        output = md.hexdigest()[:self.ID_KEY_LENGTH]
        key = output.upper()
        return key

    def create_key_pair(self):
        #TODO: replace this magic numbers with configuration
        #TODO: add exception handling
        api_key = create_api_key(20)
        identifier = create_api_key_identifier(10)
        #Why return a tuple? why not JSONify the keys?
        return (api_key, identifier)

    def entropy_health_check(self):
        #This appraoch seems like a bad one - reading from kernel space. How else could the entropy pool's status be evaluated?
        # How about moving to Python3.6 and using GRND_NONBLOCK flag?
    
        #Read from entropy_avail will only work on Linux
        #TODO: Exception handling for the assertion
        assert(os.uname().sysname == "Linux")
        pool = subprocess.call(['cat', '/proc/sys/kernel/random/entropy_avail'], stdout=subprocess.PIPE)
        available_entropy = int(pool.stdout)
        return available_entropy >= self.REQUIRED_MIN_ENTROPY

