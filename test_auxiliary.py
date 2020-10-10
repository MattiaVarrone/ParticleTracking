# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 20:04:43 2020

@author: MattiaV
"""

import unittest
from auxiliary import rotate, margins_image
import math

class RotateTest(unittest.TestCase):
    def test1(self):
        origin = 0, 0
        point = 1, 0
        angle = 45
        self.assertAlmostEqual(rotate(origin, point, angle)[0], math.sqrt(0.5))
        self.assertAlmostEqual(rotate(origin, point, angle)[1], math.sqrt(0.5))
        
    def test2(self):
        origin = 2, 1
        point = 2, -1
        angle = 90
        self.assertAlmostEqual(rotate(origin, point, angle)[0], 4)
        self.assertAlmostEqual(rotate(origin, point, angle)[1], 1)
        
class MarginsTest(unittest.TestCase):
    def test(self):
        vertices = [(27,43),(34,33),(53,102),(66,102),(93,38),(105,45)]
        self.assertEqual(margins_image(vertices)[0][0], 27)
        self.assertEqual(margins_image(vertices)[0][1], 105)
        self.assertEqual(margins_image(vertices)[1][0], 33)
        self.assertEqual(margins_image(vertices)[1][1], 102)
        
        
if __name__ == '__main__':
    unittest.main()