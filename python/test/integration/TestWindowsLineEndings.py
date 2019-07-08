#!/usr/env/python

import unittest
import subprocess

class TestWindowsLineEndings(unittest.TestCase):   
    def test_windows_line_endings(self):
        return_code = subprocess.call("python3 ../../csg2csg.py -f files/spheres.i -o all", shell=True)  
        self.assertEqual(return_code,0)
        return_code = subprocess.call("sed -e 's/$/\r/' files/spheres.i > spheres_win.i                # UNIX to DOS  (adding CRs)", shell=True)
        return_code = subprocess.call("python3 ../../csg2csg.py -f spheres_win.i -o all", shell=True)  
        self.assertEqual(return_code,0)

if __name__ == '__main__':
    unittest.main()
