#!/usr/env/python

import unittest
import subprocess


def cleanup():
    subprocess.call("rm -rf mcnp fluka openmc serpent file.mcnp", shell=True)


class TestWindowsLineEndings(unittest.TestCase):
    def test_windows_line_endings(self):

        return_code = subprocess.call(
            "csg2csg -i files/spheres.i -f mcnp -o all", shell=True
        )
        self.assertEqual(return_code, 0)
        return_code = subprocess.call(
            "sed -e 's/$/\r/' files/spheres.i > spheres_win.i                # UNIX to DOS  (adding CRs)",
            shell=True,
        )
        return_code = subprocess.call(
            "csg2csg -i spheres_win.i -f mcnp -o all", shell=True
        )
        self.assertEqual(return_code, 0)
        cleanup()

    # round trip the MCNP file produced from the line above - it should be
    # identical
    def test_round_trip(self):
        cleanup()
        return_code = subprocess.call(
            "csg2csg -i files/spheres.i -f mcnp -o mcnp", shell=True
        )
        self.assertEqual(return_code, 0)

        return_code = subprocess.call("mv mcnp/file.mcnp . ", shell=True)
        self.assertEqual(return_code, 0)
        return_code = subprocess.call("rm -rf mcnp fluka openmc serpent", shell=True)
        self.assertEqual(return_code, 0)

        return_code = subprocess.call(
            "csg2csg -i file.mcnp -f mcnp -o mcnp", shell=True
        )
        self.assertEqual(return_code, 0)
        return_code = subprocess.call("diff file.mcnp mcnp/file.mcnp", shell=True)
        self.assertEqual(return_code, 0)
        cleanup()


if __name__ == "__main__":
    unittest.main()
