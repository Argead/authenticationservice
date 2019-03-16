"""
Module used to create and return an API key and a public identifier for that key.
"""
import hashlib
import os
import subprocess

class APIKeyGenerator():
    def __init__(self, random_bits=20, api_key_length=40, id_key_length=20, req_min_entropy=100, min_api_key_length=10, max_api_key_length=60):
        #Constants to define the size of the API secret key and the public identifier.
        #Impose constraints on the size of the API key in case API_KEY_SIZE is modified
        #TODO: clean up these constants
        #TODO: add validation for initialization. Need to bracket possible values, and note those limits in documentation.
        self.RANDOM_BITS = random_bits
        self.API_KEY_LENGTH = api_key_length
        self.ID_KEY_LENGTH = id_key_length
        self.REQUIRED_MIN_ENTROPY = req_min_entropy
        self.MIN_API_KEY_LENGTH = MIN_API_KEY_LENGTH
        self.MAX_API_KEY_LENGTH = MAX_API_KEY_LENGTH
        #Assume entropy pool is not ready by default. Only update with explicit check.
        self.entropy_pool_ready = False

    #Internal method used to create and return a new API key.
    #Returns a tuple of (key, error). error is None if function call succeeds.
    #In case an exception occurs, returns a tuple of ('', error) where error is an Exception instance.
    def _create_API_key(self):
        key = ''
        error = None
        try:
            self._entropy_health_check()
            if self.entropy_pool_ready:

                #check for random bits first
                bit_valid = self._validate_random_bits()
                if bit_valid[0] == False or bit_valid[1] != None:
                    raise bit_valid[1]
                    
                #check for key length
                key_valid = self._validate_api_key_length()
                if key_valid[0] == False or key_valid[1] != None:
                    raise key_valid[1]

                #if checks pass, create new API key
                bits = os.urandom(self.RANDOM_BITS)
                sha = hashlib.sha256()
                sha.update(bits)
                sha_output = sha.hexdigest()
                key = sha_output[:self.API_KEY_LENGTH]
            else:
                raise Exception("The entropy pool is not ready")
        except Exception as e:
            error = e
        finally:
            return (key, error)

    #Helper method to validate RANDOM_BITS member
    #TODO: replace magic numbers. Why these specific constraints?
    def _validate_random_bits(self):
        is_valid = False
        error = None
        try:
            assert(self.RANDOM_BITS)
            assert(type(self.RANDOM_BITS) == int)
            assert(self.RANDOM_BITS > 10 and self.RANDOM_BITS < 100)
            is_valid = True
        except Exception as e:
            error = Exception("Invalid value for RANDOM_BITS member")
        finally:
            return (is_valid, error)


    #Helper method to validate API_KEY_LENGTH member
    #TODO: Exception: what if self.API_KEY_LENGTH does not exist? what about general exceptions?
    def _validate_api_key_length(self):
        is_valid = False
        error = None
        try:
            assert(self.API_KEY_LENGTH)
            assert(type(self.API_KEY_LENGTH) == int)
            assert(self.API_KEY_LENGTH >= self.MIN_API_KEY_LENGTH)
            assert(self.API_KEY_LENGTH <= self.MAX_API_KEY_LENGTH)
            is_valid = True
        except Exception as e:
            error = Exception("Invalid value for API_KEY_LENGTH member")
        finally:
            return (is_valid, error)





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

