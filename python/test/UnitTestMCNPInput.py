#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
from MCNPInput import MCNPInput #, explode_macrobody
from MCNPSurfaceCard import MCNPSurfaceCard
from SurfaceCard import SurfaceCard

class TestMCNPInputMethods(unittest.TestCase):

    def test_explode_macrobody(self):
        input = MCNPInput()
        card_string = "1 rpp -1 1 -1 1 -1 1"
        Surface = MCNPSurfaceCard(card_string)
        # explode macrobody into surfaces
        cells, new_surfaces = input.explode_macrobody(Surface)        
        self.assertEqual(cells[0], "( 1 -2  3 -4  5 -6 )")
        self.assertEqual(cells[1], "(-1:2:-3:4:-5:6)")
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

    def test_flatten_macrobodies(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -3\n")
        input_string.append("2 0 3\n")
        input_string.append("\n")
        input_string.append("3 rpp -1 1 -1 1 -1 1\n")
        input_string.append("\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("    1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.file_lines = input_string
        input.total_num_lines = len(input_string)       
        input.process()
        
        # cell card
        cell1 = input.cell_list[0] 
        cell2 = input.cell_list[1] 

        self.assertEqual(cell1.text_string, "1 1 -1.0 ( 4 -5  6 -7  8 -9 )")
        self.assertEqual(cell2.text_string, "2 0 (-4:5:-6:7:-8:9)")

    def test_flatten_macrobodies_with_other_surfs(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -7 3\n")
        input_string.append("2 0 -3\n")
        input_string.append("3 0 7\n")
        input_string.append("\n")
        input_string.append("3 rpp -1 1 -1 1 -1 1\n")
        input_string.append("7 so 10\n")
        input_string.append("\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("    1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.surface_list = []
        input.material_list = {}
        input.transform_list = {}

        self.assertEqual(len(input.cell_list),0)
        input.file_lines = input_string
        input.total_num_lines = len(input_string)       
        input.process()
        
        # cell card
        cell1 = input.cell_list[0] 
        cell2 = input.cell_list[1] 
        cell3 = input.cell_list[2] 
        self.assertEqual(len(input.cell_list),3)

        # surface numbering should start at 7
        self.assertEqual(cell3.text_string, "3 0 7\n")
        self.assertEqual(cell2.text_string, "2 0 ( 8 -9  10 -11  12 -13 )")
        self.assertEqual(cell1.text_string, "1 1 -1.0 -7 (-8:9:-10:11:-12:13)")

        # surfaces should be numbered from 7 to 13 contiguously
        for i in range(0,len(input.surface_list)):
            self.assertEqual(input.surface_list[i].surface_id, 7 + i)
            
        # surface 7 should be a sphere
        self.assertEqual(input.surface_list[0].surface_type, SurfaceCard.SurfaceType["SPHERE_GENERAL"])
        # 8-9 px 10-11 py 12-13 pz
        self.assertEqual(input.surface_list[1].surface_type, SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(input.surface_list[2].surface_type, SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(input.surface_list[3].surface_type, SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(input.surface_list[4].surface_type, SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(input.surface_list[5].surface_type, SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(input.surface_list[6].surface_type, SurfaceCard.SurfaceType["PLANE_Z"])
        
if __name__ == '__main__':
    unittest.main()
