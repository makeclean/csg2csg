#!/usr/env/python3

import unittest
import sys
import logging

sys.path.append("..")
from csg2csg.MCNPInput import MCNPInput #, explode_macrobody
from csg2csg.MCNPSurfaceCard import MCNPSurfaceCard
from csg2csg.SurfaceCard import SurfaceCard


class TestBlockBreaks(unittest.TestCase):

    def test_SpacesBlockBreaks(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -3\n")
        input_string.append("2 0 3\n")
        input_string.append("    \n")
        input_string.append("3 rpp -1 1 -1 1 -1 1\n")
        input_string.append("    \n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("    1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.file_lines = input_string
        input.total_num_lines = len(input_string)       
        input.process()
        
        # check number of cells found
        self.assertEqual(len(input.cell_list),2)
        
    def test_WhiteSpacesBlockBreaks(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -3\n")
        input_string.append("2 0 3\n")
        input_string.append("  \t   \n")
        input_string.append("3 rpp -1 1 -1 1 -1 1\n")
        input_string.append("   \t \n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("    1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.file_lines = input_string
        input.total_num_lines = len(input_string)       
        input.process()
       
       # check number of cells found
        self.assertEqual(len(input.cell_list),2)
        
    
class TestMCNPInputMethods(unittest.TestCase):

    def test_explode_macrobody(self):
        input = MCNPInput()
        card_string = "1 rpp -1 1 -1 1 -1 1"
        Surface = MCNPSurfaceCard(card_string)
        # explode macrobody into surfaces
        cells, new_surfaces = input.explode_macrobody(Surface)        
        self.assertEqual(cells[0], "( -1 -2 -3 -4 -5 -6 )")
        self.assertEqual(cells[1], "( 1 : 2 : 3 : 4 : 5 : 6)")
        self.assertEqual(len(new_surfaces),6)
        self.assertEqual(new_surfaces[0].surface_type,SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(new_surfaces[0].surface_coefficients[3],1)
        self.assertEqual(new_surfaces[1].surface_type,SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(new_surfaces[1].surface_coefficients[0],-1)
        self.assertEqual(new_surfaces[2].surface_type,SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(new_surfaces[2].surface_coefficients[3],1)
        self.assertEqual(new_surfaces[3].surface_type,SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(new_surfaces[3].surface_coefficients[1],-1)
        self.assertEqual(new_surfaces[4].surface_type,SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(new_surfaces[4].surface_coefficients[3],1)
        self.assertEqual(new_surfaces[5].surface_type,SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(new_surfaces[5].surface_coefficients[2],-1)

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

        self.assertEqual(cell1.text_string, "1 1 -1.0 ( -4 -5 -6 -7 -8 -9 )")
        self.assertEqual(cell2.text_string, "2 0 ( 4 : 5 : 6 : 7 : 8 : 9)")

    # test case for the box macrobody
    def test_flatten_macrobodies(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -3\n")
        input_string.append("2 0 3\n")
        input_string.append("\n")
        input_string.append("3 box -1 -1 -1 2 0 0 0 2 0 0 0 2\n")
        input_string.append("\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("   1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.file_lines = input_string
        input.total_num_lines = len(input_string)       
        input.process()
        
        # cell card
        cell1 = input.cell_list[0] 
        cell2 = input.cell_list[1] 

        self.assertEqual(cell1.text_string, "1 1 -1.0 ( -4 -5 -6 -7 -8 -9 )")
        self.assertEqual(cell2.text_string, "2 0 ( 4 : 5 : 6 : 7 : 8 : 9)")

        # surface card
        surface1 = input.surface_list[0]
        surface2 = input.surface_list[1]
        self.assertEqual(surface1.surface_type,SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(surface1.surface_coefficients,[1,0,0,1])
        self.assertEqual(surface2.surface_type,SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(surface2.surface_coefficients,[-1,0,0,1])
        
    def test_flatten_macrobodies_with_other_surfs(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -7 3\n")
        input_string.append("2 0 -3\n")
        input_string.append("3 0 7\n")
        input_string.append("\n")
        input_string.append("3 rpp -1 1 -1 1 -1 1\n")
        input_string.append("7 so 10.\n")
        input_string.append("\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("      1002 1.0\n")

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
        self.assertEqual(cell3.text_string, "3 0 7")
        self.assertEqual(cell2.text_string, "2 0 ( -8 -9 -10 -11 -12 -13 )")
        self.assertEqual(cell1.text_string, "1 1 -1.0 -7 ( 8 : 9 : 10 : 11 : 12 : 13)")

        # surfaces should be numbered from 7 to 13 contiguously
        for i in range(0,len(input.surface_list)):
            self.assertEqual(input.surface_list[i].surface_id, 7 + i)
            
        # surface 7 should be a sphere
        # self.assertEqual(input.surface_list[0].surface_type, SurfaceCard.SurfaceType["SPHERE_GENERAL"])
        # 8-9 px 10-11 py 12-13 pz
        self.assertEqual(input.surface_list[1].surface_type, SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(input.surface_list[2].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(input.surface_list[3].surface_type, SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(input.surface_list[4].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(input.surface_list[5].surface_type, SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(input.surface_list[6].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])


    def test_flatten_macrobodies_with_multiple_macrobodies(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -3\n")
        input_string.append("2 0 3 -4\n")
        input_string.append("3 0 4 -5\n")
        input_string.append("4 0 5\n")
        input_string.append("\n")
        input_string.append("3 rpp -5 5 -5 5 -5 5\n")
        input_string.append("4 rpp -10 10 -10 10 -10 10\n")
        input_string.append("5 rpp -15 15 -15 15 -15 15\n")
        input_string.append("\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("     1002 1.0\n")
        input_string.append("\n")

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
        cell4 = input.cell_list[3]
        self.assertEqual(len(input.cell_list),4)

        # are surfaces correctly processed
        self.assertEqual(input.surface_list[0].surface_type, SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(input.surface_list[1].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(input.surface_list[2].surface_type, SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(input.surface_list[3].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(input.surface_list[4].surface_type, SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(input.surface_list[5].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])

        self.assertEqual(input.surface_list[6].surface_type, SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(input.surface_list[7].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(input.surface_list[8].surface_type, SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(input.surface_list[9].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(input.surface_list[10].surface_type, SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(input.surface_list[11].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])

        self.assertEqual(input.surface_list[12].surface_type, SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(input.surface_list[13].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(input.surface_list[14].surface_type, SurfaceCard.SurfaceType["PLANE_Y"])
        self.assertEqual(input.surface_list[15].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])
        self.assertEqual(input.surface_list[16].surface_type, SurfaceCard.SurfaceType["PLANE_Z"])
        self.assertEqual(input.surface_list[17].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"])


        # surface numbering should start at 6
        self.assertEqual(cell1.text_string, "1 1 -1.0 ( -6 -7 -8 -9 -10 -11 )")
        self.assertEqual(cell2.text_string, "2 0 ( 6 : 7 : 8 : 9 : 10 : 11 ) ( -12 -13 -14 -15 -16 -17 )")
        self.assertEqual(cell3.text_string, "3 0 ( 12 : 13 : 14 : 15 : 16 : 17 ) ( -18 -19 -20 -21 -22 -23 )")

        return

        # surfaces should be numbered from 7 to 13 contiguously
        for i in range(0,len(input.surface_list)):
            self.assertEqual(input.surface_list[i].surface_id, 7 + i)
            
        # surface 7 should be a sphere
        # 8-9 px 10-11 py 12-13 pz
        
if __name__ == '__main__':
    unittest.main()
