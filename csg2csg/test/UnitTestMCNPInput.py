#!/usr/env/python3

import unittest
import sys
import logging

sys.path.append("..")
from csg2csg.MCNPInput import MCNPInput  # , explode_macrobody
from csg2csg.MCNPSurfaceCard import MCNPSurfaceCard
from csg2csg.SurfaceCard import SurfaceCard


class TestBlockBreaks(unittest.TestCase):
    def test_spaces_block_breaks(self):
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
        self.assertEqual(len(input.cell_list), 2)

    def test_white_spaces_block_breaks(self):
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
        self.assertEqual(len(input.cell_list), 2)

    def test_comment_lines(self):
        input_string = ["this is a title\n"]
        input_string.append(
            "4980  130 0.06026342    8085  -8086   8654  -4684  27  100 -200 imp:n=1\n"
        )
        input_string.append(
            "4985  130 0.06000038     8011  -8086   4684  -4682  27  100 -200 imp:n=1\n"
        )
        input_string.append(
            "4995  130 0.099591    8011  -8086   4682  -53    27  100 -200 imp:n=1\n"
        )
        input_string.append("c\n")
        input_string.append(
            "c      Comment line sandwiched by two blank comment lines\n"
        )
        input_string.append("c\n")
        input_string.append(
            "5001  130 0.099591    7511  -7586   -67 7602  -53  100 -200 imp:n=1\n"
        )
        input_string.append(
            "5002  130 0.06000038    7511  -7586   -7602  7604  -53  100 -200 imp:n=1 \n"
        )
        input_string.append("   \t \n")
        input_string.append("8085 so 10.\n")
        input_string.append("8086 so 11.\n")
        input_string.append("8654 so 12.\n")
        input_string.append("4684 so 13.\n")
        input_string.append("27 so 14.\n")
        input_string.append("100 so 15.\n")
        input_string.append("200 so 16.\n")
        input_string.append("   \t \n")
        input_string.append("m130 1001 1.0\n")
        input_string.append("    1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.surface_list = []
        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.process()

        # check number of cells found is 5 and does not include the c
        self.assertEqual(len(input.cell_list), 5)

        # checks the number of surfaces found is 7
        self.assertEqual(len(input.surface_list), 7)


class TestMCNPInputMethods(unittest.TestCase):
    def test_explode_macrobody(self):
        input = MCNPInput()
        card_string = "1 rpp -1 1 -1 1 -1 1"
        Surface = MCNPSurfaceCard(card_string)
        # explode macrobody into surfaces
        cells, new_surfaces = input.explode_macrobody(Surface)
        self.assertEqual(cells[0], "( -1 -2 -3 -4 -5 -6 )")
        self.assertEqual(cells[1], "( 1 : 2 : 3 : 4 : 5 : 6)")
        self.assertEqual(len(new_surfaces), 6)
        self.assertEqual(
            new_surfaces[0].surface_type, SurfaceCard.SurfaceType["PLANE_X"]
        )
        self.assertEqual(new_surfaces[0].surface_coefficients[3], 1)
        self.assertEqual(
            new_surfaces[1].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(new_surfaces[1].surface_coefficients[0], -1)
        self.assertEqual(
            new_surfaces[2].surface_type, SurfaceCard.SurfaceType["PLANE_Y"]
        )
        self.assertEqual(new_surfaces[2].surface_coefficients[3], 1)
        self.assertEqual(
            new_surfaces[3].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(new_surfaces[3].surface_coefficients[1], -1)
        self.assertEqual(
            new_surfaces[4].surface_type, SurfaceCard.SurfaceType["PLANE_Z"]
        )
        self.assertEqual(new_surfaces[4].surface_coefficients[3], 1)
        self.assertEqual(
            new_surfaces[5].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(new_surfaces[5].surface_coefficients[2], -1)

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
        self.assertEqual(surface1.surface_type, SurfaceCard.SurfaceType["PLANE_X"])
        self.assertEqual(surface1.surface_coefficients, [1, 0, 0, 1])
        self.assertEqual(
            surface2.surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(surface2.surface_coefficients, [-1, 0, 0, 1])

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

        self.assertEqual(len(input.cell_list), 0)
        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.process()

        # cell card
        cell1 = input.cell_list[0]
        cell2 = input.cell_list[1]
        cell3 = input.cell_list[2]
        self.assertEqual(len(input.cell_list), 3)

        # surface numbering should start at 7
        self.assertEqual(cell3.text_string, "3 0 7")
        self.assertEqual(cell2.text_string, "2 0 ( -8 -9 -10 -11 -12 -13 )")
        self.assertEqual(cell1.text_string, "1 1 -1.0 -7 ( 8 : 9 : 10 : 11 : 12 : 13)")

        # surfaces should be numbered from 7 to 13 contiguously
        for i in range(0, len(input.surface_list)):
            self.assertEqual(input.surface_list[i].surface_id, 7 + i)

        # surface 7 should be a sphere
        # self.assertEqual(input.surface_list[0].surface_type, SurfaceCard.SurfaceType["SPHERE_GENERAL"])
        # 8-9 px 10-11 py 12-13 pz
        self.assertEqual(
            input.surface_list[1].surface_type, SurfaceCard.SurfaceType["PLANE_X"]
        )
        self.assertEqual(
            input.surface_list[2].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(
            input.surface_list[3].surface_type, SurfaceCard.SurfaceType["PLANE_Y"]
        )
        self.assertEqual(
            input.surface_list[4].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(
            input.surface_list[5].surface_type, SurfaceCard.SurfaceType["PLANE_Z"]
        )
        self.assertEqual(
            input.surface_list[6].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )

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

        self.assertEqual(len(input.cell_list), 0)
        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.process()

        # cell card
        cell1 = input.cell_list[0]
        cell2 = input.cell_list[1]
        cell3 = input.cell_list[2]
        cell4 = input.cell_list[3]
        self.assertEqual(len(input.cell_list), 4)

        # are surfaces correctly processed
        self.assertEqual(
            input.surface_list[0].surface_type, SurfaceCard.SurfaceType["PLANE_X"]
        )
        self.assertEqual(
            input.surface_list[1].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(
            input.surface_list[2].surface_type, SurfaceCard.SurfaceType["PLANE_Y"]
        )
        self.assertEqual(
            input.surface_list[3].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(
            input.surface_list[4].surface_type, SurfaceCard.SurfaceType["PLANE_Z"]
        )
        self.assertEqual(
            input.surface_list[5].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )

        self.assertEqual(
            input.surface_list[6].surface_type, SurfaceCard.SurfaceType["PLANE_X"]
        )
        self.assertEqual(
            input.surface_list[7].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(
            input.surface_list[8].surface_type, SurfaceCard.SurfaceType["PLANE_Y"]
        )
        self.assertEqual(
            input.surface_list[9].surface_type, SurfaceCard.SurfaceType["PLANE_GENERAL"]
        )
        self.assertEqual(
            input.surface_list[10].surface_type, SurfaceCard.SurfaceType["PLANE_Z"]
        )
        self.assertEqual(
            input.surface_list[11].surface_type,
            SurfaceCard.SurfaceType["PLANE_GENERAL"],
        )

        self.assertEqual(
            input.surface_list[12].surface_type, SurfaceCard.SurfaceType["PLANE_X"]
        )
        self.assertEqual(
            input.surface_list[13].surface_type,
            SurfaceCard.SurfaceType["PLANE_GENERAL"],
        )
        self.assertEqual(
            input.surface_list[14].surface_type, SurfaceCard.SurfaceType["PLANE_Y"]
        )
        self.assertEqual(
            input.surface_list[15].surface_type,
            SurfaceCard.SurfaceType["PLANE_GENERAL"],
        )
        self.assertEqual(
            input.surface_list[16].surface_type, SurfaceCard.SurfaceType["PLANE_Z"]
        )
        self.assertEqual(
            input.surface_list[17].surface_type,
            SurfaceCard.SurfaceType["PLANE_GENERAL"],
        )

        # surface numbering should start at 6
        self.assertEqual(cell1.text_string, "1 1 -1.0 ( -6 -7 -8 -9 -10 -11 )")
        self.assertEqual(
            cell2.text_string,
            "2 0 ( 6 : 7 : 8 : 9 : 10 : 11 ) ( -12 -13 -14 -15 -16 -17 )",
        )
        self.assertEqual(
            cell3.text_string,
            "3 0 ( 12 : 13 : 14 : 15 : 16 : 17 ) ( -18 -19 -20 -21 -22 -23 )",
        )

        return

        # surfaces should be numbered from 7 to 13 contiguously
        for i in range(0, len(input.surface_list)):
            self.assertEqual(input.surface_list[i].surface_id, 7 + i)

        # surface 7 should be a sphere
        # 8-9 px 10-11 py 12-13 pz

    def test_cone_expansion(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -1\n")
        input_string.append("2 0       1\n")
        input_string.append("\n")
        input_string.append("1 k/z 0 0 5 0.5 -1\n")
        input_string.append("\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("   1002 1.0\n")
        input_string.append("\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.surface_list = []
        input.material_list = {}
        input.transform_list = {}

        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.process()

        # are surfaces correctly processed
        self.assertEqual(
            input.surface_list[0].surface_type, SurfaceCard.SurfaceType["CONE_Z"]
        )

        # surface numbering should start at 6
        cell1 = input.cell_list[0]
        cell2 = input.cell_list[1]
        self.assertEqual(cell1.text_string, "1 1 -1.0 ( -1 -2 )")
        self.assertEqual(cell2.text_string, "2 0 (  1 -2 : 2)")

        return


class TestMCNPInputRegressions(unittest.TestCase):
    def test_parenthesis_bug(self):
        input_string = ["this is a title\n"]
        input_string.append("1 0 (3) \n")
        input_string.append("2 0 (#1)\n")
        input_string.append(" \n")
        input_string.append("3 cz 300\n")
        input_string.append(" \n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("    1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.process()

        # check number of cells found
        self.assertEqual(len(input.cell_list), 2)
        self.assertEqual(input.cell_list[0].text_string, "1 0 (3) \n")
        self.assertEqual(input.cell_list[1].text_string, "2 0 (#1)\n")

        del input

    def test_parenthesis_plane_bug(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -1\n")
        input_string.append("2 0  1\n")
        input_string.append(" \n")
        input_string.append("1 1 px 2.0\n")
        input_string.append(" \n")
        input_string.append("*tr1 0 0.15 0 45 90 45 90 0 90 135 90 45\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("   1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.process()

        # check number of cells found
        self.assertEqual(len(input.cell_list), 2)
        self.assertEqual(len(input.surface_list), 1)
        self.assertEqual(len(input.surface_list[0].surface_coefficients), 4)
        self.assertEqual(
            input.surface_list[0].surface_coefficients[0], 0.7071067811865476
        )
        self.assertEqual(
            input.surface_list[0].surface_coefficients[1], 6.123233995736766e-17
        )
        self.assertEqual(
            input.surface_list[0].surface_coefficients[2], 0.7071067811865476
        )
        self.assertEqual(input.surface_list[0].surface_coefficients[3], 2.0)

        del input

    def test_duplicate_surface_without_rot(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -1\n")
        input_string.append("2 1 -1.0  2\n")
        input_string.append(" \n")
        input_string.append("1 px 2.0\n")
        input_string.append("2 px 2.0\n")
        input_string.append(" \n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("   1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.quick_process = False
        input.process()

        self.assertEqual(len(input.surface_list), 1)

    def test_duplicate_surface_with_rot(self):
        input_string = ["this is a title\n"]
        input_string.append("1 1 -1.0 -1\n")
        input_string.append("2 1 -1.0  2\n")
        input_string.append(" \n")
        input_string.append("1 1 px 2.0\n")
        input_string.append("2 1 px 2.0\n")
        input_string.append(" \n")
        input_string.append("*tr1 0 0.15 0 45 90 45 90 0 90 135 90 45\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("   1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.process()

        self.assertEqual(len(input.surface_list), 1)

    def test_duplicate_surface_with_macro(self):
        input_string = ["this is a title\n"]
        input_string.append("1 0  -1\n")
        input_string.append("2 0  -2\n")
        input_string.append(" \n")
        input_string.append("1 px 2.0\n")
        input_string.append("2 rpp -2 2 -2 2 -2 2\n")
        input_string.append(" \n")
        input_string.append("*tr1 0 0.15 0 45 90 45 90 0 90 135 90 45\n")
        input_string.append("m1 1001 1.0\n")
        input_string.append("   1002 1.0\n")

        # setup input
        input = MCNPInput()
        input.cell_list = []
        input.file_lines = input_string
        input.total_num_lines = len(input_string)
        input.process()

        self.assertEqual(len(input.surface_list), 6)


if __name__ == "__main__":
    unittest.main()
