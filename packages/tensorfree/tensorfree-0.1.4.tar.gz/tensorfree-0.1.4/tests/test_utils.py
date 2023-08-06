#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for 'utils' package"""

import os
from PIL import Image
from unittest import TestCase
from hashlib import sha1
import numpy as np
import tensorflow.keras.applications as kapps

from tensorfree.utils.preprocess import image_sizing
from tensorfree.utils.label import label_generator
from tensorfree.utils.wrappers import run_logger


class ImageProcTests(TestCase):
    """Test for preprocess module."""

    def setUp(self) -> None:
        """Generate a series of fake image types for testing"""
        self.image_size = 256
        self.image_shape = (256, 256, 3)

        # Removed use of temporarydirectory because path problems
        long_jpeg = Image.new("RGB", (800, 600), color="blue")
        long_jpeg.save("long.jpg")

        tall_jpeg = Image.new("RGB", (600, 800), color="red")
        tall_jpeg.save("tall.jpg")

        bw_jpeg = Image.new("L", (800, 600), color="white")
        bw_jpeg.save("bw.jpg")

        basic_png = Image.new("RGB", (800, 600), color="yellow")
        basic_png.putalpha(64)
        basic_png.save("basic.png")

        # Test garbage non-image
        with open("trashfile", "wb") as f:
            f.write(os.urandom(128))

    def tearDown(self) -> None:
        """Remove generated images"""
        os.remove("long.jpg")
        os.remove("tall.jpg")
        os.remove("bw.jpg")
        os.remove("basic.png")
        os.remove("trashfile")

    def test_scale_long(self):
        """Check that a long image is scaled to a square"""
        cleaned_image = image_sizing("long.jpg", self.image_size)
        self.assertEqual(cleaned_image.shape, self.image_shape)

    def test_scale_tall(self):
        """Tall image should use different conditional"""
        cleaned_image = image_sizing("tall.jpg", self.image_size)
        self.assertEqual(cleaned_image.shape, self.image_shape)

    def test_scale_png(self):
        """PNGs have four channels, the function should convert to 3 channel jpg"""
        cleaned_image = image_sizing("basic.png", self.image_size)
        self.assertEqual(cleaned_image.shape, self.image_shape)

    def test_scale_bw(self):
        """Black and white images have a single channel, function should adjust to 3 channels"""
        cleaned_image = image_sizing("bw.jpg", self.image_size)
        self.assertEqual(cleaned_image.shape, self.image_shape)

    def test_bad_path(self):
        """FileNotFoundError should be raised if image doesnt exist at path location"""
        fake_file = "this_image_does_not_exist.jpg"
        with self.assertRaises(FileNotFoundError):
            image_sizing(fake_file, self.image_size)

    def test_bad_input(self):
        """TypeError should be raised if file isn't an image"""
        with self.assertRaises(TypeError):
            image_sizing("trashfile", self.image_size)


class LabelTests(TestCase):
    """Test for label module."""

    def test_labeler(self):
        # Create an array that is all zero, except for a single one representing "Goldfish"
        fake_predictions = np.eye(1, 1000, k=1).reshape(1, 1000)
        fake_hash = sha1(fake_predictions).hexdigest()
        fake_label = f"goldfish_{fake_hash}.png"

        generated = label_generator(
            fake_predictions, kapps.mobilenet_v2.decode_predictions, "random.png"
        )
        self.assertEqual(fake_label, generated)


