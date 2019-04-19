#!/usr/bin/python3
"""Test suite for the KeyValidator classes."""

import unittest
from ...authentication.key_generator import BasicKeyGenerator, _KeyGeneratorABC
from ...authentication.key_validator import BasicKeyValidator, _KeyValidatorABC

class TestBasicKeyValidator(unittest.TestCase):
    """Test cases for BasicKeyValidator class."""

    def test_BasicKeyValidator_exists(self):
        """Test if the BasicKeyValidator can be created."""
        basic_key_length = 40
        basic_cipher = "sha256"
        validator = BasicKeyValidator(basic_cipher, basic_key_length)
        self.assertIsInstance(validator, BasicKeyValidator)
        self.assertIsInstance(validator, _KeyValidatorABC)

    def test_BasicKeyGenerator_exists(self):
        """Test if the BasicKeyGenerator can be created."""
        generator = BasicKeyGenerator()
        self.assertIsInstance(generator, BasicKeyGenerator)
        self.assertIsInstance(generator, _KeyGeneratorABC)

    def test_basic_validate_api_key_method(self):
        """Test if the basic validation method works."""
        generator = BasicKeyGenerator()
        key_length = generator.key_length
        cipher = generator.cipher.name
        validator = BasicKeyValidator(cipher, key_length)
        new_key = generator.generate_api_key()
        self.assertEqual(generator.cipher.name, validator.cipher)
        self.assertEqual(generator.key_length, validator.key_length)
        self.assertEqual(len(new_key), validator.key_length)
        self.assertEqual(True, validator.validate_api_key(new_key))

    def test_create_request_signature_method_fails(self):
        """Test if this method raises a NotImplementedError."""
        try:
            cipher = "sha256"
            key_length = 40
            fake_key = "abc124"
            fake_request = "request"
            validator = BasicKeyValidator(cipher, key_length)
            res = validator.create_request_signature(fake_key, fake_request)
        except NotImplementedError as error:
            self.assertIsInstance(error, NotImplementedError)
