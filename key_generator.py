"""
Module used to create and return an API key and a public identifier for that key.
"""
import hashlib
import os
import subprocess

class APIKeyGenerator():
    def __init__(self, api_key_length, id_key_length, req_min_entropy, min_key_length):
        #Constants to define the size of the API secret key and the public identifier.
        #TODO: clean up these constants
        self.API_KEY_LENGTH = api_key_length
        self.ID_KEY_LENGTH = id_key_length
        self.REQUIRED_MIN_ENTROPY = req_min_entropy
        self.MIN_KEY_LENGTH = min_key_length
        #Assume entropy pool is not ready by default. Only update with explicit check.
        self.entropy_pool_ready = False

    #Internal method used to create and return a new API key.
    # random_bits is an int describing the number of bits to take from os.urandom()
    # returns a tuple of (key, error). error is None if function call succeeds.
    def _create_API_key(self, random_bits):
        #TODO: clean up this method. Too long, too complex, too many return statements.
        #      divide up into multiple functions
        self._entropy_health_check()
        if self.entropy_pool_ready:
            bits = os.urandom(random_bits)
            #TODO: develop more options than just SHA256. Strategy pattern (?)
            sha = hashlib.sha256()
            sha.update(bits)
            sha_output = sha.hexdigest()

            #Impose constraints on the size of the API key in case API_KEY_SIZE is modified
            try:
                assert(type(self.API_KEY_LENGTH == int))
                assert(self.API_KEY_LENGTH <= len(sha_output) and self.API_KEY_LENGTH > self.MIN_KEY_LENGTH)
                key = sha_output[:self.API_KEY_LENGTH]
                return (key, None)
            except AssertionError:
                error = Exception("API Key Length parameters are invalid.")
                return ('', error)
        else:
            error = Exception("The entropy pool is not ready")
            return ('', error)







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

