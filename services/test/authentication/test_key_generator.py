#!/usr/bin/python3
"""Test suite for the KeyGenerator classes."""

import unittest
from .services.authentication import BasicKeyGenerator, BasicKeyValidator

class TestBasicKeyGenerator(unittest.TestCase):
    """Test suite for BasicKeyGenerator class."""

    def test_BasicKeyGenerator_exists(self):
        generator = BasicKeyGenerator()
        print(type(generator))
        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
