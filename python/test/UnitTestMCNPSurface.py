#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
from MCNPSurfaceCard import MCNPSurfaceCard, surface_has_transform
from SurfaceCard import SurfaceCard

class TestMCNPSurfaceMethods(unittest.TestCase):

    def test_plane(self):
        card_string = "1 px 12.0"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.text_string, card_string)
        self.assertEqual(card.surface_type,SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(card.surface_coefficients[0], 12.0)
        self.assertEqual(card.surface_coefficients[1], 0.0)
        self.assertEqual(card.surface_coefficients[2], 0.0)

    def test_plane_general(self):
        card_string = "1 p 0 0 1 15"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.text_string, card_string)
        self.assertEqual(card.surface_type,SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(card.surface_coefficients[0], 0.0)
        self.assertEqual(card.surface_coefficients[1], 0.0)
        self.assertEqual(card.surface_coefficients[2], 1.0)
        self.assertEqual(card.surface_coefficients[3],15.0)
        
    def test_sphere(self):
        card_string = "15 s 0 0 1 15"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.text_string, card_string)
        self.assertEqual(card.surface_type,SurfaceCard.SurfaceType["SPHERE_GENERAL"])
        self.assertEqual(card.surface_coefficients[0], 0.0)
        self.assertEqual(card.surface_coefficients[1], 0.0)
        self.assertEqual(card.surface_coefficients[2], 1.0)
        self.assertEqual(card.surface_coefficients[3],15.0)


    def test_surfacetransform_detect(self):
        card = "1 2 px 3"
        self.assertEqual(surface_has_transform(card),True)
        card = "1 PX 3"
        self.assertEqual(surface_has_transform(card),False)
        

if __name__ == '__main__':
    unittest.main()
