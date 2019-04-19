#!/usr/bin/python3
"""Classes for validating a previously generated API key."""

from abc import ABC, abstractmethod

class _KeyValidatorABC(ABC):
    """Base class for KeyValidator implementations."""

    @abstractmethod
    def validate_api_key(self, api_key):
        """Validate provided api key for well-formedness."""

    @abstractmethod
    def create_request_signature(self, api_key, request):
        """For more complex signature scheme, resign request."""


class BasicKeyValidator(_KeyValidatorABC):
    """Most basic KeyValidator implementation. Only checks key length."""

    def __init__(self, cipher, key_length):
        """
        Cipher not strictly necessary for this basic implementation.

        Parameter cipher - string name of cipher used to generate key.
        Parameter key_length - int length of key length for cipher..
        """
        self.cipher = cipher
        self.key_length = key_length

    def validate_api_key(self, api_key):
        """Check the length of provided api key."""
        return len(api_key) == self.key_length

    def create_request_signature(self, api_key, request):
        """Validate key sig. Method is not needed for basic validator."""
        raise NotImplementedError
