"""
Unitary tests for pyxpiral.py.

:author: elcodedocle
:contact: gael.abadin@gmail.com

"""

# pylint:disable=C0103,C0111,W0212,W0611

import logging
import unittest

from .. import __main__ as pyxpiral


class TestPyxpiral(unittest.TestCase):
    """
    Unitary tests for Pyxpiral.
    """

    @classmethod
    def setUpClass(cls):
        '''
        Global setUp.
        '''

        logging.basicConfig(level=logging.INFO)

    def setUp(self):
        '''
        Test setUp.
        '''
        self.ppl = pyxpiral.Pyxpiral()
        self.message = \
            "Never go full electro (AKA Keep calm and read bits cycling in squared spirals)."

    def test_encode(self):
        self.ppl.encode(self.message)

    def test_decode(self):
        image = self.ppl.encode(self.message, upscale=1)
        self.assertEqual(self.ppl.decode(image, downscale=1), self.message)

    def test_encode_fractal(self):
        images = self.ppl.encode_fractal(self.message, upscale=1)
        self.assertEqual(self.ppl.decode(images[0], downscale=1), self.message)

    def tearDown(self):
        '''
        Test tearDown.
        '''

    @classmethod
    def tearDownClass(cls):
        '''
        Global tearDown.
        '''
