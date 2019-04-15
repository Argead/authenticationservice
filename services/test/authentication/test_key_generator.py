#!/usr/bin/python3
"""Test suite for the KeyGenerator classes."""

import unittest
from ...authentication.key_generator import BasicKeyGenerator, _KeyGeneratorABC

class TestBasicKeyGenerator(unittest.TestCase):
    """Test suite for BasicKeyGenerator class."""

    def test_BasicKeyGenerator_exists(self):
        """Test if the BasicKeyGenerator can be created."""
        generator = BasicKeyGenerator()
        self.assertIsInstance(generator, BasicKeyGenerator)
        self.assertIsInstance(generator, _KeyGeneratorABC)

    def test_BasicKeyGenerator_can_create_api_keys(self):
        """Test if the generate_api_key method produces output."""
        generator = BasicKeyGenerator()
        new_key = ''
        new_key = generator.generate_api_key()
        self.assertIsNot(new_key, '')

    def test_BasicKeyGenerator_creates_well_formed_api_keys(self):
        """Test if the generate_api_key method produces right output."""
        generator = BasicKeyGenerator()
        new_key = ''
        new_key = generator.generate_api_key()
        self.assertEqual(len(new_key), generator.key_length)


if __name__ == "__main__":
    unittest.main()
