from unittest import TestCase

from tensorfree import Tensorfree
from tensorfree.model import pretrain


class BuildTests(TestCase):
    """Test cases for Tensorfree.py"""
    def setUp(self) -> None:
        self.model = Tensorfree.build('VGG19')

    def test_build(self):
        self.assertEqual(type(self.model), type(pretrain.factory.create('VGG19')))
