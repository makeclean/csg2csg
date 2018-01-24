#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
from MCNPSurfaceCard import MCNPSurfaceCard, surface_has_transform
from SurfaceCard import SurfaceCard

class TestMCNPSurfaceMethods(unittest.TestCase):

    def test_plane_x(self):
        card_string = "1 px 12.0"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.text_string, card_string)
        self.assertEqual(card.surface_type,SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(card.surface_coefficients[0], 1.0)
        self.assertEqual(card.surface_coefficients[1], 0.0)
        self.assertEqual(card.surface_coefficients[2], 0.0)
        self.assertEqual(card.surface_coefficients[3], 12.0)

    def test_plane_y(self):
        card_string = "1 py 12.0"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.text_string, card_string)
        self.assertEqual(card.surface_type,SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(card.surface_coefficients[0], 0.0)
        self.assertEqual(card.surface_coefficients[1], 1.0)
        self.assertEqual(card.surface_coefficients[2], 0.0)
        self.assertEqual(card.surface_coefficients[3], 12.0)

    def test_plane_z(self):
        card_string = "1 pz 12.0"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.text_string, card_string)
        self.assertEqual(card.surface_type,SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(card.surface_coefficients[0], 0.0)
        self.assertEqual(card.surface_coefficients[1], 0.0)
        self.assertEqual(card.surface_coefficients[2], 1.0)
        self.assertEqual(card.surface_coefficients[3], 12.0)

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


    def test_gq(self):
        card_string = "15000 gq 1 1 0 0 0 0 1 1 1 1"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.surface_type, SurfaceCard.SurfaceType["GENERAL_QUADRATIC"])
        self.assertEqual(card.surface_id, 15000)
        self.assertEqual(card.surface_coefficients[0], 1.0)
        self.assertEqual(card.surface_coefficients[1], 1.0)
        self.assertEqual(card.surface_coefficients[2], 0.0)
        self.assertEqual(card.surface_coefficients[3], 0.0)
        self.assertEqual(card.surface_coefficients[4], 0.0)
        self.assertEqual(card.surface_coefficients[5], 0.0)
        self.assertEqual(card.surface_coefficients[6], 1.0)
        self.assertEqual(card.surface_coefficients[7], 1.0)
        self.assertEqual(card.surface_coefficients[8], 1.0)
        self.assertEqual(card.surface_coefficients[9], 1.0)

    def test_so(self):
        card_string = "15000 so 2.5"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.surface_type, SurfaceCard.SurfaceType["SPHERE_GENERAL"])
        self.assertEqual(card.surface_id, 15000)
        self.assertEqual(card.surface_coefficients[0], 0.0)
        self.assertEqual(card.surface_coefficients[1], 0.0)
        self.assertEqual(card.surface_coefficients[2], 0.0)
        self.assertEqual(card.surface_coefficients[3], 2.5)

    def test_sx(self):
        card_string = "15000 sx 3.0 2.5"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.surface_type, SurfaceCard.SurfaceType["SPHERE_GENERAL"])
        self.assertEqual(card.surface_id, 15000)
        self.assertEqual(card.surface_coefficients[0], 3.0)
        self.assertEqual(card.surface_coefficients[1], 0.0)
        self.assertEqual(card.surface_coefficients[2], 0.0)
        self.assertEqual(card.surface_coefficients[3], 2.5)

    def test_sy(self):
        card_string = "15000 sy 3.0 2.5"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.surface_type, SurfaceCard.SurfaceType["SPHERE_GENERAL"])
        self.assertEqual(card.surface_id, 15000)
        self.assertEqual(card.surface_coefficients[0], 0.0)
        self.assertEqual(card.surface_coefficients[1], 3.0)
        self.assertEqual(card.surface_coefficients[2], 0.0)
        self.assertEqual(card.surface_coefficients[3], 2.5)

    def test_sx(self):
        card_string = "15000 sz 3.0 2.5"
        card = MCNPSurfaceCard(card_string)
        self.assertEqual(card.surface_type, SurfaceCard.SurfaceType["SPHERE_GENERAL"])
        self.assertEqual(card.surface_id, 15000)
        self.assertEqual(card.surface_coefficients[0], 0.0)
        self.assertEqual(card.surface_coefficients[1], 0.0)
        self.assertEqual(card.surface_coefficients[2], 3.0)
        self.assertEqual(card.surface_coefficients[3], 2.5)

        
    def test_surfacetransform_detect(self):
        card = "1 2 px 3"
        self.assertEqual(surface_has_transform(card),True)
        card = "1 PX 3"
        self.assertEqual(surface_has_transform(card),False)
        

if __name__ == '__main__':
    unittest.main()
