#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `model` package."""
import os
from pathlib import Path
from PIL import Image
from tempfile import TemporaryDirectory
from unittest import TestCase
import numpy as np

from tensorfree.model import pretrain


class ModelBuildingTests(TestCase):
    """Test cases for both pretrain.py and pretrain_factory.py"""

    def setUp(self) -> None:
        """Create a mobilenet prediction model to test against"""
        self.model = pretrain.factory.create("MobileNetV2")

    def test_register(self):
        """Verify that the factory register created correct model type"""
        self.assertIsInstance(self.model, pretrain.MobileNetBuilder)

    def test_unknown_model(self):
        """Check that an error is raised if user calls an unknown model name"""
        with self.assertRaises(ValueError):
            model = pretrain.factory.create("UnavailableModel")

    def test_photo_get(self):
        """Confirm that calling get_photos sets instance photo_store"""
        self.assertEqual(self.model._photo_store, None)
        print(self.model.get_photos("photodir"))
        self.assertEqual(self.model._photo_store, "photodir")

    def test_photo_save(self):
        """Same test but for photo_save"""
        self.assertEqual(self.model._photo_save, None)
        print(self.model.save_photos("savedir"))
        self.assertEqual(self.model._photo_save, "savedir")


class InternalsTests(TestCase):
    """Test cases for the internal 'hidden' functions of model"""

    def setUp(self) -> None:
        """Create a mobilenet model and fake saved image to test against."""
        self.model = pretrain.factory.create("MobileNetV2")

        self.test_name = "test.jpg"
        test_jpeg = Image.new("RGB", (800, 600), color="blue")
        test_jpeg.save(self.test_name)

    def tearDown(self) -> None:
        """Remove test file"""
        os.remove(self.test_name)

    def test_predict(self):
        """Verify that model was created and is giving predictions on images"""
        fake_image_array = np.ones((224, 224, 3))
        fake_predictions = np.ones((1, 1000))
        predictions = self.model._predict(fake_image_array)
        self.assertEqual(predictions.shape, fake_predictions.shape)

    def test_run_tensorfree(self):
        """Make sure an image is going through the prediction and labeling process"""
        with TemporaryDirectory() as tempdir:
            self.assertTrue(len(os.listdir(tempdir)) == 0)
            self.model._run_tensorfree(self.test_name, tempdir)
            self.assertTrue(len(os.listdir(tempdir)) == 1)

            file = os.listdir(tempdir)[0]
            self.assertEqual(Path(file).suffixes[0], ".jpg")


class DenseLabelTests(TestCase):
    """Tests for densenet.label() feature."""

    def setUp(self) -> None:
        """Create a new model, lets go with DenseNet this time"""
        self.model = pretrain.factory.create("DenseNet")

        self.image1 = Image.new("RGB", (800, 600), color="blue")
        self.image2 = Image.new("RGB", (800, 600), color="yellow")
        self.image3 = Image.new("RGB", (200, 200), color="red")

    def test_label_no_save(self):
        """Label should raise a ValueError if user hasn't set model.save_photos('path') first"""
        with self.assertRaises(ValueError):
            self.model._photo_save = None
            self.model.label()

    def test_label_no_store(self):
        """Label should raise a ValueError if user hasn't set model.get_photos('path') first"""
        with self.assertRaises(ValueError):
            self.model._photo_store = None
            self.model.label()

    def test_label(self):
        """Test that label will run through a directory and process images"""
        with TemporaryDirectory() as tempdir:
            # Add fake images to temp directory
            self.image1.save(tempdir + "/image1.jpg")
            self.image2.save(tempdir + "/image2.jpg")
            self.image3.save(tempdir + "/image3.jpg")

            testdir = os.path.join(tempdir, "tests")
            os.mkdir(testdir)

            # Set model get and save locations, run
            self.model.get_photos(tempdir)
            self.model.save_photos(testdir)
            self.model.label()

            self.assertEqual(len(os.listdir(testdir)), 3)


class NASLabelTests(TestCase):
    """Tests for nasnet.label() feature."""

    def setUp(self) -> None:
        """Create a new model, lets go with DenseNet this time"""
        self.model = pretrain.factory.create("NASNetLarge")

        self.image1 = Image.new("RGB", (800, 600), color="blue")
        self.image2 = Image.new("RGB", (800, 600), color="yellow")
        self.image3 = Image.new("RGB", (200, 200), color="red")

    def test_label(self):
        """Test that label will run through a directory and process images"""
        with TemporaryDirectory() as tempdir:
            # Add fake images to temp directory
            self.image1.save(tempdir + "/image1.jpg")
            self.image2.save(tempdir + "/image2.jpg")
            self.image3.save(tempdir + "/image3.jpg")

            testdir = os.path.join(tempdir, "tests")
            os.mkdir(testdir)

            # Set model get and save locations, run
            self.model.get_photos(tempdir)
            self.model.save_photos(testdir)
            self.model.label()

            self.assertEqual(len(os.listdir(testdir)), 3)


class InceptionLabelTests(TestCase):
    """Tests for InceptionResNetV2.label() feature."""

    def setUp(self) -> None:
        """Create a new model, lets go with DenseNet this time"""
        self.model = pretrain.factory.create("InceptionResNetV2")

        self.image1 = Image.new("RGB", (800, 600), color="blue")
        self.image2 = Image.new("RGB", (800, 600), color="yellow")
        self.image3 = Image.new("RGB", (200, 200), color="red")

    def test_label(self):
        """Test that label will run through a directory and process images"""
        with TemporaryDirectory() as tempdir:
            # Add fake images to temp directory
            self.image1.save(tempdir + "/image1.jpg")
            self.image2.save(tempdir + "/image2.jpg")
            self.image3.save(tempdir + "/image3.jpg")

            testdir = os.path.join(tempdir, "tests")
            os.mkdir(testdir)

            # Set model get and save locations, run
            self.model.get_photos(tempdir)
            self.model.save_photos(testdir)
            self.model.label()

            self.assertEqual(len(os.listdir(testdir)), 3)


class VGGLabelTests(TestCase):
    """Tests for VGG19.label() feature."""

    def setUp(self) -> None:
        """Create a new model, lets go with DenseNet this time"""
        self.model = pretrain.factory.create("VGG19")

        self.image1 = Image.new("RGB", (800, 600), color="blue")
        self.image2 = Image.new("RGB", (800, 600), color="yellow")
        self.image3 = Image.new("RGB", (200, 200), color="red")

    def test_label(self):
        """Test that label will run through a directory and process images"""
        with TemporaryDirectory() as tempdir:
            # Add fake images to temp directory
            self.image1.save(tempdir + "/image1.jpg")
            self.image2.save(tempdir + "/image2.jpg")
            self.image3.save(tempdir + "/image3.jpg")

            testdir = os.path.join(tempdir, "tests")
            os.mkdir(testdir)

            # Set model get and save locations, run
            self.model.get_photos(tempdir)
            self.model.save_photos(testdir)
            self.model.label()

            self.assertEqual(len(os.listdir(testdir)), 3)
