#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
from SurfaceCard import SurfaceCard

class SurfaceMethods(unittest.TestCase):

    def test_simplify_plane_to_plane(self):
        surface = SurfaceCard('')
        surface_coefficients = [1.0,1.0,0.0,10.]
        transform_id = 0
        surface_type = surface.SurfaceType['PLANE_GENERAL']
        surface_id = 1
        surface.set_type(surface_id,transform_id,surface_type,surface_coefficients)
        surface.simplify()
        self.assertEqual(surface.surface_type, surface.SurfaceType['PLANE_GENERAL'])

    def test_simplify_gq_to_plane(self):
        surface = SurfaceCard('')
        surface_coefficients = [0,0,0,0,0,0,1.0,1.0,0.0,-10.]
        transform_id = 0
        surface_type = surface.SurfaceType['GENERAL_QUADRATIC']
        surface_id = 1
        surface.set_type(surface_id,transform_id,surface_type,surface_coefficients)
        surface.simplify()
        self.assertEqual(surface.surface_type, surface.SurfaceType['PLANE_GENERAL'])

    def test_generalise(self):
        surface = SurfaceCard('')
        surface_coefficients = [1.0,1.0,0.0,-10.]
        transform_id = 0
        surface_type = surface.SurfaceType['PLANE_GENERAL']
        surface_id = 1
        surface.set_type(surface_id,transform_id,surface_type,surface_coefficients)
        surface.generalise()
        self.assertEqual(surface.surface_type, surface.SurfaceType['GENERAL_QUADRATIC'])
        for i in range(6):
            self.assertEqual(surface.surface_coefficients[i],0.0)

    def test_generalise_simplify_general_plane(self):
        surface = SurfaceCard('')
        surface_coefficients = [1.0,1.0,0.0,-10.]
        transform_id = 0
        surface_type = surface.SurfaceType['PLANE_GENERAL']
        surface_id = 1
        surface.set_type(surface_id,transform_id,surface_type,surface_coefficients)
        surface.generalise()
        self.assertEqual(surface.surface_type, surface.SurfaceType['GENERAL_QUADRATIC'])
        for i in range(6):
            self.assertEqual(surface.surface_coefficients[i],0.0)
        surface.simplify()
        # make sure we get a general plane back
        self.assertEqual(surface.surface_type, surface.SurfaceType['PLANE_GENERAL'])
        self.assertEqual(surface.surface_coefficients[0],1.0)
        self.assertEqual(surface.surface_coefficients[1],1.0)
        self.assertEqual(surface.surface_coefficients[2],0.0)
        self.assertEqual(surface.surface_coefficients[3],-10.0)

    # test the surface.generalise() function
    def test_surface_reverse(self):
        # first surface
        surface1 = SurfaceCard('')
        surface_coefficients = [1.0,0.0,0.0,-10.]
        transform_id = 0
        surface_type = surface1.SurfaceType['PLANE_GENERAL']
        surface_id = 1
        surface1.set_type(surface_id,transform_id,surface_type,surface_coefficients)
        surface1.generalise()
        self.assertEqual(surface1.surface_coefficients[6],-1.0)
        self.assertEqual(surface1.surface_coefficients[9],-10.0)
    
    # test the surface.reverse() function
    def test_surface_reverse(self):
        # first surface
        surface1 = SurfaceCard('')
        surface_coefficients = [1.0,0.0,0.0,-10.]
        transform_id = 0
        surface_type = surface1.SurfaceType['PLANE_GENERAL']
        surface_id = 1
        surface1.set_type(surface_id,transform_id,surface_type,surface_coefficients)
        surface1.generalise()
        surface1.reverse()
        self.assertEqual(surface1.surface_coefficients[6],-1.0)
        self.assertEqual(surface1.surface_coefficients[9],-10.0)
        
    def test_surface_two_planes_compare(self):
        # first surface
        surface1 = SurfaceCard('')
        surface_coefficients = [1.0,0.0,0.0,10.]
        transform_id = 0
        surface_type = surface1.SurfaceType['PLANE_GENERAL']
        surface_id = 1
        surface1.set_type(surface_id,transform_id,surface_type,surface_coefficients)

        # second surface
        surface2 = SurfaceCard('')
        surface_coefficients = [-1.0,0.0,0.0,-10.]
        transform_id = 0
        surface_type = surface2.SurfaceType['PLANE_GENERAL']
        surface_id = 2
        surface2.set_type(surface_id,transform_id,surface_type,surface_coefficients)

        self.assertEqual(surface1.diff(surface2,False),(False,False))
        self.assertEqual(surface1.diff(surface2),(True,True))
    
if __name__ == '__main__':
    unittest.main()
