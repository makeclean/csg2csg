#!/usr/env/python3

import unittest
import sys
sys.path.append("..")

from Vector import add,cross,subtract

class TestVectorMethods(unittest.TestCase):

    def test_subtract(self):
        a = [1,0,0]
        b = [1,0,0]
        c = subtract(a,b)

        self.assertEqual(c[0], 0.0)
        self.assertEqual(c[1], 0.0)
        self.assertEqual(c[2], 0.0)
        

    def test_add(self):
        a = [1,0,0]
        b = [0,1,0]
        c = add(a,b)

        self.assertEqual(c[0],1.0)
        self.assertEqual(c[1],1.0)
        self.assertEqual(c[2],0.0)

    def test_cross(self):
        a = [1,0,0]
        b = [0,1,0]
        c = cross(a,b)

        self.assertEqual(c[0],0.0)
        self.assertEqual(c[1],0.0)
        self.assertEqual(c[2],1.0)
        
if __name__ == '__main__':
    unittest.main()
