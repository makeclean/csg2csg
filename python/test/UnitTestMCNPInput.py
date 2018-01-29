#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
from MCNPInput import MCNPInput, explode_macrobody
from MCNPSurfaceCard import MCNPSurfaceCard
from SurfaceCard import SurfaceCard

class TestMCNPInputMethods(unittest.TestCase):
    
    def test_explode_macrobody(self):
        card_string = "1 rpp -1 1 -1 1 -1 1"
        Surface = MCNPSurfaceCard(card_string)
        # explode macrobody into surfaces
        new_surfaces = explode_macrobody(Surface)        
        self.assertEqual(len(new_surfaces),6)
        self.assertEqual(new_surfaces[0].surface_type,SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(new_surfaces[0].surface_coefficients[3],-1)
        self.assertEqual(new_surfaces[1].surface_type,SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(new_surfaces[1].surface_coefficients[3],1)
        self.assertEqual(new_surfaces[2].surface_type,SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(new_surfaces[2].surface_coefficients[3],-1)
        self.assertEqual(new_surfaces[3].surface_type,SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(new_surfaces[3].surface_coefficients[3],1)
        self.assertEqual(new_surfaces[4].surface_type,SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(new_surfaces[4].surface_coefficients[3],-1)
        self.assertEqual(new_surfaces[5].surface_type,SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(new_surfaces[5].surface_coefficients[3],1)
        
if __name__ == '__main__':
    unittest.main()
