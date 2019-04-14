#!/usr/bin/python3
"""Classes for validating a previously generated API key."""

from abc import ABC, abstractmethod

class KeyValidatorABC(ABC):
    """Base class for KeyValidator implementations."""

    @abstractmethod
    def __init__(self, cipher, key_length):
        """Provide cipher type to validate against."""
        return

    @abstractmethod
    def validate_api_key(self, api_key):
        """Validate provided api key for well-formedness."""
        return

    @abstractmethod
    def create_request_signature(self, api_key, request):
        """For more complex signature scheme, resign request."""
        return
