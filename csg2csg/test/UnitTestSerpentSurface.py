#!/usr/env/python3

import unittest
import sys

sys.path.append("..")

from csg2csg.SurfaceCard import SurfaceCard
from csg2csg.MCNPSurfaceCard import MCNPSurfaceCard
from csg2csg.SerpentSurfaceCard import serpent_cone_x
from math import sqrt


class TestSerpentSurface(unittest.TestCase):
    def test_cone_x_up_write(self):
        card = "1 k/x 0 0 0 0.5 1"
        surfcard = MCNPSurfaceCard(card)
        surfcard.b_box = [0, 10, 0, 0, 0, 0]
        serp_string = serpent_cone_x(surfcard)
        self.assertEqual(
            serp_string, " ckx 0.000000 0.000000 0.000000 0.500000 1.000000\n"
        )

    def test_cone_x_down_write(self):
        card = "1 k/x 0 0 0 0.5 -1"
        surfcard = MCNPSurfaceCard(card)
        surfcard.b_box = [0, 0, 0, 0, 0, 0]
        surfcard.b_box = [-10, 0, 0, 0, 0, 0]
        serp_string = serpent_cone_x(surfcard)
        self.assertEqual(
            serp_string, " ckx 0.000000 0.000000 0.000000 0.500000 -1.000000\n"
        )


if __name__ == "__main__":
    unittest.main()
