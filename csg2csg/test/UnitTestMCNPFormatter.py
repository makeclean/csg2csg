#!/usr/env/python3

import unittest
import sys
sys.path.append("..")

from csg2csg.MCNPFormatter import get_fortran_formatted_number

class TestFortranReadMethods(unittest.TestCase):

    def test_fortran_format(self):
        string = "-1.0-1"
        number = get_fortran_formatted_number(string)
        self.assertEqual(number,-1.e-1)
        
        string = "-1.0+1"
        number = get_fortran_formatted_number(string)
        self.assertEqual(number,-1.e1)

        string = "1.0+1"
        number = get_fortran_formatted_number(string)
        self.assertEqual(number,1.e1)

        string = "15.0-100"
        number = get_fortran_formatted_number(string)
        self.assertEqual(number,1.5e-99)

        string = "-15.0+39"
        number = get_fortran_formatted_number(string)
        self.assertEqual(number,-1.5e40)

        string = "-15.0+309"
        number = get_fortran_formatted_number(string)
        self.assertEqual(number,-1.5e310)

        string = "6.1000"
        number = get_fortran_formatted_number(string)
        self.assertEqual(number,6.1000)

        string = "-6.1000"
        number = get_fortran_formatted_number(string)
        self.assertEqual(number,-6.1000)

if __name__ == '__main__':
    unittest.main()
