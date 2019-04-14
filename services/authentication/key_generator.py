#!/usr/bin/python3
"""API key generators."""

from abc import ABC, abstractmethod
import hashlib
import os

class KeyGeneratorABC(ABC):
    """Base class for key generator implementations."""

    @abstractmethod
    def check_generator_health(self):
        """Check status of underlying entropy pool."""
        return

    @abstractmethod
    def generate_api_key(self):
        """Interface for single initial method of abc class."""
        return

class BasicKeyGenerator(KeyGeneratorABC):
    """Simplest key generator. Returns 40 char unique key."""

    def __init__(self):
        """Set reasonable defaults. No config for now."""
        self.key_length = 40
        self.random_bits = 20
        self.cipher = hashlib.new("sha256")
        self.entropy_pool = False
        self.check_generator_health()

    def generate_api_key(self):
        """Generate a single 40 char key. No choice for cipher yet."""
        assert self.entropy_pool
        try:
            random_bits = os.urandom(self.random_bits)
            self.cipher.update(random_bits)
            output = self.cipher.hexdigest()
            output = output[:self.key_length]
            return output
        finally:
            self._reset_cipher()

    def check_generator_health(self):
        """Check for a randomness source."""
        try:
            os.urandom(self.random_bits)
            self.entropy_pool = True
        except NotImplementedError:
            self.entropy_pool = False

    def _reset_cipher(self):
        """Reset sha256 so bits not used twice."""
        self.cipher = hashlib.new("sha256")
