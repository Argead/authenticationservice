"""
Module used to create and return an API key and a public identifier for that key.
"""
import hashlib
import os
import subprocess

class APIKeyGenerator():
    def __init__(self):
        self.RANDOM_BITS = 20
        self.API_KEY_LENGTH = 40
        self.ID_KEY_LENGTH = 20
        self.REQUIRED_MIN_ENTROPY = 100
        self.MIN_API_KEY_LENGTH = 10
        self.MAX_API_KEY_LENGTH = 60
        #Assume underlying OS's entropy pool is not ready by default. Only update with explicit check.
        self.entropy_pool_ready = False

    #Main public method for this class. Creates and returns a secret key to sign API requests, and a public identifier.
    # Returns a tuple of two strings: (api_key, identifier).
    def create_key_pair(self):
        try:
            new_api_key = self.create_one_api_key()
            new_identifier = self.create_api_key_identifier(new_api_key)
            return (new_api_key, new_api_key_identifier)
        except Exception as e:
            raise e

    #Internal method used to check if the underlying source of entropy is ready for usage.
    #No explicit return value. Updates class instance's internal state by manipulating the entropy_pool_ready member.
    def _entropy_health_check(self):
        #This appraoch seems like a bad one - reading from kernel space. How else could the entropy pool's status be evaluated?
        # How about moving to Python3.6 and using GRND_NONBLOCK flag?
        try:
            #Current implementation of this method is designed to work only on nix systems
            #TODO: Implement for other OSs.
            assert(os.uname().sysname == "Linux")
            pool = subprocess.call(['cat', '/proc/sys/kernel/random/entropy_avail'], stdout=subprocess.PIPE)
            available_entropy = int(pool.stdout)
            assert(available_entropy >= self.REQUIRED_MIN_ENTROPY)
            self.entropy_pool_ready = True
        except Exception as e:
            self.entropy_pool_ready = False

    #Internal method used to create and return a new API key.
    #Returns a single valid API key as a string, or raises an Exception
    def _create_one_api_key(self):
        self._entropy_health_check(self)
        try:
            assert(self.entropy_pool_ready)
            bits = os.urandom(self.RANDOM_BITS)
            #TODO: strategy pattern for multiple underlying cypher options
            sha = hashlib.sha256()
            sha.update(bits)
            sha_output = sha.hexdigest()
            key = sha_output[:self.API_KEY_LENGTH]
            return key
        except AssertionError as e:
            raise KeyCreationError("Entropy pool is not ready")
        except Exception as e:
            raise KeyCreationError(e.message)

    #Internal method to generate an identifier for a given API key
    def _create_api_key_identifier(self, api_key):
        try:
            #TODO: implement pattern for multiple underlying cyphers
            md = hashlib.md5()
            md.update(api_key)
            result = md.hexdigest()[:self.ID_KEY_LENGTH]
            identifier = output.upper()
            return identifier
        except Exception as e:
            raise e

#Exception class to make errors in key creation explicit.
class KeyCreationError(Exception):
    def __init__(self, message):
        super().__init__(message)




