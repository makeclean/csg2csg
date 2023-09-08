from csg2csg.MCNPInput import MCNPInput  # , explode_macrobody
from csg2csg.MCNPSurfaceCard import MCNPSurfaceCard
from csg2csg.SurfaceCard import SurfaceCard


def test_spaces_block_breaks():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -3\n",
        "2 0 3\n",
        "    \n",
        "3 rpp -1 1 -1 1 -1 1\n",
        "    \n",
        "m1 1001 1.0\n",
        "    1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.file_lines = input_string
    # TODO: why is this being set, it doesn't seem to be used anywhere
    input.total_num_lines = len(input_string)
    input.process()

    # check number of cells found
    assert len(input.cell_list) == 2


def test_white_spaces_block_breaks():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -3\n",
        "2 0 3\n",
        "  \t   \n",
        "3 rpp -1 1 -1 1 -1 1\n",
        "   \t \n",
        "m1 1001 1.0\n",
        "    1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    # check number of cells found
    assert len(input.cell_list) == 2


def test_comment_lines():
    input_string = [
        "this is a title\n",
        "4980  130 0.06026342    8085  -8086   8654  -4684  27  100 -200 imp:n=1\n",
        "4985  130 0.06000038     8011  -8086   4684  -4682  27  100 -200 imp:n=1\n",
        "4995  130 0.099591    8011  -8086   4682  -53    27  100 -200 imp:n=1\n",
        "c\n",
        "c      Comment line sandwiched by two blank comment lines\n",
        "c\n",
        "5001  130 0.099591    7511  -7586   -67 7602  -53  100 -200 imp:n=1\n",
        "5002  130 0.06000038    7511  -7586   -7602  7604  -53  100 -200 imp:n=1 \n",
        "   \t \n",
        "8085 so 10.\n",
        "8086 so 11.\n",
        "8654 so 12.\n",
        "4684 so 13.\n",
        "27 so 14.\n",
        "100 so 15.\n",
        "200 so 16.\n",
        "   \t \n",
        "m130 1001 1.0\n",
        "    1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.surface_list = []
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    # check number of cells found is 5 and does not include the c
    assert len(input.cell_list) == 5

    # checks the number of surfaces found is 7
    assert len(input.surface_list) == 7


def test_explode_macrobody():
    input = MCNPInput()
    card_string = "1 rpp -1 1 -1 1 -1 1"
    Surface = MCNPSurfaceCard(card_string)
    # explode macrobody into surfaces
    cells, new_surfaces = input.explode_macrobody(Surface)
    assert cells[0] == "( -1 -2 -3 -4 -5 -6 )"
    assert cells[1] == "( 1 : 2 : 3 : 4 : 5 : 6)"
    assert len(new_surfaces) == 6
    assert new_surfaces[0].surface_type == SurfaceCard.SurfaceType["PLANE_X"]
    assert new_surfaces[0].surface_coefficients[3] == 1
    assert new_surfaces[1].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert new_surfaces[1].surface_coefficients[0] == -1
    assert new_surfaces[2].surface_type == SurfaceCard.SurfaceType["PLANE_Y"]
    assert new_surfaces[2].surface_coefficients[3] == 1
    assert new_surfaces[3].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert new_surfaces[3].surface_coefficients[1] == -1
    assert new_surfaces[4].surface_type == SurfaceCard.SurfaceType["PLANE_Z"]
    assert new_surfaces[4].surface_coefficients[3] == 1
    assert new_surfaces[5].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert new_surfaces[5].surface_coefficients[2] == -1


def test_flatten_macrobodies():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -3\n",
        "2 0 3\n",
        "\n",
        "3 rpp -1 1 -1 1 -1 1\n",
        "\n",
        "m1 1001 1.0\n",
        "    1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    # cell card
    cell1 = input.cell_list[0]
    cell2 = input.cell_list[1]

    assert cell1.text_string == "1 1 -1.0 ( -4 -5 -6 -7 -8 -9 )"
    assert cell2.text_string == "2 0 ( 4 : 5 : 6 : 7 : 8 : 9)"


# test case for the box macrobody
def test_box_macrobody():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -3\n",
        "2 0 3\n",
        "\n",
        "3 box -1 -1 -1 2 0 0 0 2 0 0 0 2\n",
        "\n",
        "m1 1001 1.0\n",
        "   1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    # cell card
    cell1 = input.cell_list[0]
    cell2 = input.cell_list[1]

    assert cell1.text_string == "1 1 -1.0 ( -4 -5 -6 -7 -8 -9 )"
    assert cell2.text_string == "2 0 ( 4 : 5 : 6 : 7 : 8 : 9)"

    # surface card
    surface1 = input.surface_list[0]
    surface2 = input.surface_list[1]
    assert surface1.surface_type == SurfaceCard.SurfaceType["PLANE_X"]
    assert surface1.surface_coefficients == [1, 0, 0, 1]
    assert surface2.surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert surface2.surface_coefficients == [-1, 0, 0, 1]


def test_flatten_macrobodies_with_other_surfs():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -7 3\n",
        "2 0 -3\n",
        "3 0 7\n",
        "\n",
        "3 rpp -1 1 -1 1 -1 1\n",
        "7 so 10.\n",
        "\n",
        "m1 1001 1.0\n",
        "      1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()

    input.cell_list = []
    input.surface_list = []
    input.material_list = {}
    input.transform_list = {}

    assert len(input.cell_list) == 0
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    # cell card
    cell1 = input.cell_list[0]
    cell2 = input.cell_list[1]
    cell3 = input.cell_list[2]
    assert len(input.cell_list) == 3

    # surface numbering should start at 7
    assert cell3.text_string == "3 0 7"
    assert cell2.text_string == "2 0 ( -8 -9 -10 -11 -12 -13 )"
    assert cell1.text_string == "1 1 -1.0 -7 ( 8 : 9 : 10 : 11 : 12 : 13)"

    # surfaces should be numbered from 7 to 13 contiguously
    for i in range(0, len(input.surface_list)):
        assert input.surface_list[i].surface_id == 7 + i

    # surface 7 should be a sphere
    # assert input.surface_list[0].surface_type == SurfaceCard.SurfaceType["SPHERE_GENERAL"]
    # 8-9 px 10-11 py 12-13 pz
    assert input.surface_list[1].surface_type == SurfaceCard.SurfaceType["PLANE_X"]
    assert input.surface_list[2].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert input.surface_list[3].surface_type == SurfaceCard.SurfaceType["PLANE_Y"]
    assert input.surface_list[4].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert input.surface_list[5].surface_type == SurfaceCard.SurfaceType["PLANE_Z"]
    assert input.surface_list[6].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]


def test_flatten_macrobodies_with_multiple_macrobodies():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -3\n",
        "2 0 3 -4\n",
        "3 0 4 -5\n",
        "4 0 5\n",
        "\n",
        "3 rpp -5 5 -5 5 -5 5\n",
        "4 rpp -10 10 -10 10 -10 10\n",
        "5 rpp -15 15 -15 15 -15 15\n",
        "\n",
        "m1 1001 1.0\n",
        "     1002 1.0\n",
        "\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.surface_list = []
    input.material_list = {}
    input.transform_list = {}

    assert len(input.cell_list) == 0
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    # cell card
    cell1 = input.cell_list[0]
    cell2 = input.cell_list[1]
    cell3 = input.cell_list[2]
    cell4 = input.cell_list[3]
    assert len(input.cell_list) == 4

    # are surfaces correctly processed
    assert input.surface_list[0].surface_type == SurfaceCard.SurfaceType["PLANE_X"]
    assert input.surface_list[1].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert input.surface_list[2].surface_type == SurfaceCard.SurfaceType["PLANE_Y"]
    assert input.surface_list[3].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert input.surface_list[4].surface_type == SurfaceCard.SurfaceType["PLANE_Z"]
    assert input.surface_list[5].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]

    assert input.surface_list[6].surface_type == SurfaceCard.SurfaceType["PLANE_X"]
    assert input.surface_list[7].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert input.surface_list[8].surface_type == SurfaceCard.SurfaceType["PLANE_Y"]
    assert input.surface_list[9].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert input.surface_list[10].surface_type == SurfaceCard.SurfaceType["PLANE_Z"]
    assert input.surface_list[11].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]

    assert input.surface_list[12].surface_type == SurfaceCard.SurfaceType["PLANE_X"]
    assert input.surface_list[13].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert input.surface_list[14].surface_type == SurfaceCard.SurfaceType["PLANE_Y"]
    assert input.surface_list[15].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert input.surface_list[16].surface_type == SurfaceCard.SurfaceType["PLANE_Z"]
    assert input.surface_list[17].surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]

    # surface numbering should start at 6
    assert cell1.text_string == "1 1 -1.0 ( -6 -7 -8 -9 -10 -11 )"
    assert cell2.text_string == "2 0 ( 6 : 7 : 8 : 9 : 10 : 11 ) ( -12 -13 -14 -15 -16 -17 )"
    assert cell3.text_string == "3 0 ( 12 : 13 : 14 : 15 : 16 : 17 ) ( -18 -19 -20 -21 -22 -23 )"
    # TODO: check that this is correct, previously wasn't being tested
    assert cell4.text_string == "4 0 ( 18 : 19 : 20 : 21 : 22 : 23)"

    # TODO: why was this test returning here
    return

    # surfaces should be numbered from 7 to 13 contiguously
    for i in range(0, len(input.surface_list)):
        assert input.surface_list[i].surface_id == 7 + i

    # surface 7 should be a sphere
    # 8-9 px 10-11 py 12-13 pz


def test_cone_expansion():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -1\n",
        "2 0       1\n",
        "\n",
        "1 k/z 0 0 5 0.5 -1\n",
        "\n",
        "m1 1001 1.0\n",
        "   1002 1.0\n",
        "\n",
    ]

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
    assert input.surface_list[0].surface_type == SurfaceCard.SurfaceType["CONE_Z"]

    # surface numbering should start at 6
    cell1 = input.cell_list[0]
    cell2 = input.cell_list[1]
    assert cell1.text_string == "1 1 -1.0 ( -1 -2 )"
    assert cell2.text_string == "2 0 (  1 -2 : 2)"


def test_parenthesis_bug():
    input_string = [
        "this is a title\n",
        "1 0 (3) \n",
        "2 0 (#1)\n",
        " \n",
        "3 cz 300\n",
        " \n",
        "m1 1001 1.0\n",
        "    1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    # check number of cells found
    assert len(input.cell_list) == 2
    assert input.cell_list[0].text_string == "1 0 (3) \n"
    assert input.cell_list[1].text_string == "2 0 (#1)\n"


def test_parenthesis_plane_bug():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -1\n",
        "2 0  1\n",
        " \n",
        "1 1 px 2.0\n",
        " \n",
        "*tr1 0 0.15 0 45 90 45 90 0 90 135 90 45\n",
        "m1 1001 1.0\n",
        "   1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    # check number of cells found
    assert len(input.cell_list) == 2
    assert len(input.surface_list) == 1
    assert len(input.surface_list[0].surface_coefficients) == 4
    assert input.surface_list[0].surface_coefficients[0] == 0.7071067811865476
    assert input.surface_list[0].surface_coefficients[1] == 6.123233995736766e-17
    assert input.surface_list[0].surface_coefficients[2] == 0.7071067811865476
    assert input.surface_list[0].surface_coefficients[3] == 2.0


def test_duplicate_surface_without_rot():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -1\n",
        "2 1 -1.0  2\n",
        " \n",
        "1 px 2.0\n",
        "2 px 2.0\n",
        " \n",
        "m1 1001 1.0\n",
        "   1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.quick_process = False
    input.process()

    assert len(input.surface_list) == 1


def test_duplicate_surface_with_rot():
    input_string = [
        "this is a title\n",
        "1 1 -1.0 -1\n",
        "2 1 -1.0  2\n",
        " \n",
        "1 1 px 2.0\n",
        "2 1 px 2.0\n",
        " \n",
        "*tr1 0 0.15 0 45 90 45 90 0 90 135 90 45\n",
        "m1 1001 1.0\n",
        "   1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    assert len(input.surface_list) == 1


def test_duplicate_surface_with_macro():
    input_string = [
        "this is a title\n",
        "1 0  -1\n",
        "2 0  -2\n",
        " \n",
        "1 px 2.0\n",
        "2 rpp -2 2 -2 2 -2 2\n",
        " \n",
        "*tr1 0 0.15 0 45 90 45 90 0 90 135 90 45\n",
        "m1 1001 1.0\n",
        "   1002 1.0\n",
    ]

    # setup input
    input = MCNPInput()
    input.cell_list = []
    input.file_lines = input_string
    input.total_num_lines = len(input_string)
    input.process()

    assert len(input.surface_list) == 6
