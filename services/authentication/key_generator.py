#!/usr/bin/python3
"""API key generators."""

from abc import ABC, abstractmethod




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

class KeyGenerator(KeyGeneratorABC):

