#!/usr/bin/env python

"""Tests for `carol_pdf_generator` package."""


import unittest

from carol_pdf_generator import carol_pdf_generator
from urllib import request
from io import BytesIO


class TestCarol_pdf_generator(unittest.TestCase):
    """Tests for `carol_pdf_generator` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.base64_jpg = request.urlopen(
            'https://pastebin.com/raw/k3VZeNHW').read().decode('latin1')
        self.base64_png = request.urlopen(
            'https://pastebin.com/raw/7Asb2iMJ').read().decode('latin1')
        self.base64_images = [self.base64_png, request.urlopen(
            'https://pastebin.com/raw/CaZJ7n6s').read().decode('latin1')]
        self.base64_images.append(self.base64_jpg)

        self.random_str = "data:plain/text,wefneo;fnwepfiowenf"

        self.file_list = [
            'tests/jpgfile.jpg',
            'tests/pngfile.png'
        ]

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get_image_data(self):
        """Test get_image_data."""
        image_data = carol_pdf_generator.get_image_data(self.base64_jpg)
        self.assertIsInstance(image_data, BytesIO)

    def test_image_supported(self):
        """Test image_supported"""

        self.assertTrue(carol_pdf_generator.image_supported(self.base64_jpg))
        self.assertTrue(carol_pdf_generator.image_supported(self.base64_png))
        self.assertFalse(carol_pdf_generator.image_supported(self.random_str))

    def test_get_image_type(self):
        """Test get_image_type"""
        self.assertEqual(
            carol_pdf_generator.get_image_type(
                self.base64_jpg), 'jpeg')
        self.assertEqual(
            carol_pdf_generator.get_image_type(
                self.base64_png), 'png')

    def test_get_from_base64_list(self):
        """Test get_from_base64_list"""
        base64 = carol_pdf_generator.get_from_base64_list(
            self.base64_images, remove_encoding=False)
        self.assertIsInstance(base64, str)
        self.assertIn(
            "data:application/pdf;charset=latin1;base64,JVBERi0xLjQKMyAwIG9",
            base64)
        self.assertEqual(len(base64), 134515)

    def test_get_from_file_list(self):
        """Test get_from_file_list"""
        from_file = carol_pdf_generator.get_from_file_list(
            self.file_list, remove_encoding=False)
        self.assertIsInstance(from_file, str)
        self.assertIn(
            "data:application/pdf;charset=latin1;base64,JVBERi0xLjQKMyA",
            from_file)
        self.assertEqual(len(from_file), 1598279)
