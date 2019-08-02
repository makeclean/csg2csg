#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
 
from csg2csg.OpenMCMaterial import zaid_to_name

class TestOpenMCMaterial(unittest.TestCase):

    def test_zaid_name_conversion(self):
        name = "1001"
        self.assertEqual(zaid_to_name(name),"H1")
        name = "26056"
        print (name[0:0],name[1:1])
        self.assertEqual(zaid_to_name(name),"Fe56")
        name = "53133"
        self.assertEqual(zaid_to_name(name),"I133")
        name = "56133"
        self.assertEqual(zaid_to_name(name),"Ba133")
        name = "118294"
        self.assertEqual(zaid_to_name(name),"Og294")
        
if __name__ == '__main__':
    unittest.main()
