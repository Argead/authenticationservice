#!/usr/bin/python3
"""Test suite for the KeyGenerator classes."""

import os
import unittest
import unittest.mock
from ...authentication.key_generator import BasicKeyGenerator, _KeyGeneratorABC

class TestBasicKeyGenerator(unittest.TestCase):
    """Test suite for BasicKeyGenerator class."""

    def test_BasicKeyGenerator_exists(self):
        """Test if the BasicKeyGenerator can be created."""
        generator = BasicKeyGenerator()
        self.assertIsInstance(generator, BasicKeyGenerator)
        self.assertIsInstance(generator, _KeyGeneratorABC)

    def test_check_generator_health_method(self):
        """Test if the health_check method succeeds."""
        generator = BasicKeyGenerator()
        generator.check_generator_health()
        self.assertTrue(generator.entropy_pool)

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

    def test_BasicKeyGenerator_generates_new_keys_each_run(self):
        """Test if any key is duplicated."""
        seen_keys = []
        generator = BasicKeyGenerator()
        for _ in range(1000):
            new_key = generator.generate_api_key()
            self.assertFalse(new_key in seen_keys)
            seen_keys.append(new_key)
        seen_keys_set = set(seen_keys)
        self.assertEqual(len(seen_keys_set), len(seen_keys))

    def test_BasicKeyGenerator_can_handle_many_requests(self):
        """Test if the key generator works with 100K requests."""
        seen_keys = []
        generator = BasicKeyGenerator()
        for _ in range(100000):
            new_key = generator.generate_api_key()
            seen_keys.append(new_key)
        seen_keys_set = set(seen_keys)
        self.assertEqual(len(seen_keys), len(seen_keys_set))

class TestFailingScenariosForBasicKeyGenerator(unittest.TestCase):
    """Test cases for scenarios where key generator fails."""

    def setUp(self):
        """Remove access to underlying source of entropy."""
        self.holder = os.urandom
        os.urandom = unittest.mock.Mock(side_effect=NotImplementedError)

    def tearDown(self):
        """Restore normal functionality to os.urandom."""
        os.urandom = self.holder

    def helper_call_to_os_urandom(self):
        """Helper method to call os.urandom."""
        try:
            os.urandom()
        except NotImplementedError as err:
            return err

    def test_os_urandom_can_fail_using_a_mock(self):
        """Test that os.urandom can be mocked to fail."""
        failing_urandom = self.helper_call_to_os_urandom()
        self.assertIsInstance(failing_urandom, NotImplementedError)

    def test_key_generation_fails_without_os_urandom(self):
        """Test that key generation fails without os.urandom."""
        try:
            generator = BasicKeyGenerator()
            generator.generate_api_key()
        except AssertionError as err:
            err = str(err)
            self.assertEqual(err, "No entropy source available.")
