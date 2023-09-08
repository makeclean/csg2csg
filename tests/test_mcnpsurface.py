from csg2csg.MCNPSurfaceCard import MCNPSurfaceCard, surface_has_transform
from csg2csg.SurfaceCard import SurfaceCard


def test_plane_x():
    card_string = "1 px 12.0"
    card = MCNPSurfaceCard(card_string)
    assert card.text_string == card_string
    assert card.surface_type == SurfaceCard.SurfaceType["PLANE_X"]
    assert card.surface_coefficients[0] == 1.0
    assert card.surface_coefficients[1] == 0.0
    assert card.surface_coefficients[2] == 0.0
    assert card.surface_coefficients[3] == 12.0


def test_plane_y():
    card_string = "1 py 12.0"
    card = MCNPSurfaceCard(card_string)
    assert card.text_string == card_string
    assert card.surface_type == SurfaceCard.SurfaceType["PLANE_Y"]
    assert card.surface_coefficients[0] == 0.0
    assert card.surface_coefficients[1] == 1.0
    assert card.surface_coefficients[2] == 0.0
    assert card.surface_coefficients[3] == 12.0


def test_plane_z():
    card_string = "1 pz 12.0"
    card = MCNPSurfaceCard(card_string)
    assert card.text_string == card_string
    assert card.surface_type == SurfaceCard.SurfaceType["PLANE_Z"]
    assert card.surface_coefficients[0] == 0.0
    assert card.surface_coefficients[1] == 0.0
    assert card.surface_coefficients[2] == 1.0
    assert card.surface_coefficients[3] == 12.0


def test_plane_general():
    card_string = "1 p 0 0 1 15"
    card = MCNPSurfaceCard(card_string)
    assert card.text_string == card_string
    assert card.surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]
    assert card.surface_coefficients[0] == 0.0
    assert card.surface_coefficients[1] == 0.0
    assert card.surface_coefficients[2] == 1.0
    assert card.surface_coefficients[3] == 15.0


def test_sphere():
    card_string = "15 s 0 0 1 15"
    card = MCNPSurfaceCard(card_string)
    assert card.text_string == card_string
    assert card.surface_type == SurfaceCard.SurfaceType["SPHERE_GENERAL"]
    assert card.surface_coefficients[0] == 0.0
    assert card.surface_coefficients[1] == 0.0
    assert card.surface_coefficients[2] == 1.0
    assert card.surface_coefficients[3] == 15.0


def test_gq():
    card_string = "15000 gq 1 1 0 0 0 0 1 1 1 1"
    card = MCNPSurfaceCard(card_string)
    assert card.surface_type == SurfaceCard.SurfaceType["GENERAL_QUADRATIC"]
    assert card.surface_id == 15000
    assert card.surface_coefficients[0] == 1.0
    assert card.surface_coefficients[1] == 1.0
    assert card.surface_coefficients[2] == 0.0
    assert card.surface_coefficients[3] == 0.0
    assert card.surface_coefficients[4] == 0.0
    assert card.surface_coefficients[5] == 0.0
    assert card.surface_coefficients[6] == 1.0
    assert card.surface_coefficients[7] == 1.0
    assert card.surface_coefficients[8] == 1.0
    assert card.surface_coefficients[9] == 1.0


def test_so():
    card_string = "15000 so 2.5"
    card = MCNPSurfaceCard(card_string)
    assert card.surface_type == SurfaceCard.SurfaceType["SPHERE_GENERAL"]
    assert card.surface_id == 15000
    assert card.surface_coefficients[0] == 0.0
    assert card.surface_coefficients[1] == 0.0
    assert card.surface_coefficients[2] == 0.0
    assert card.surface_coefficients[3] == 2.5


def test_sx():
    card_string = "15000 sx 3.0 2.5"
    card = MCNPSurfaceCard(card_string)
    assert card.surface_type == SurfaceCard.SurfaceType["SPHERE_GENERAL"]
    assert card.surface_id == 15000
    assert card.surface_coefficients[0] == 3.0
    assert card.surface_coefficients[1] == 0.0
    assert card.surface_coefficients[2] == 0.0
    assert card.surface_coefficients[3] == 2.5


def test_sy():
    card_string = "15000 sy 3.0 2.5"
    card = MCNPSurfaceCard(card_string)
    assert card.surface_type == SurfaceCard.SurfaceType["SPHERE_GENERAL"]
    assert card.surface_id == 15000
    assert card.surface_coefficients[0] == 0.0
    assert card.surface_coefficients[1] == 3.0
    assert card.surface_coefficients[2] == 0.0
    assert card.surface_coefficients[3] == 2.5


def test_cz():
    card_string = "15000 cz 2.5"
    card = MCNPSurfaceCard(card_string)
    assert card.surface_type == SurfaceCard.SurfaceType["CYLINDER_Z"]
    assert card.surface_id == 15000
    assert card.surface_coefficients[0] == 0.0
    assert card.surface_coefficients[1] == 0.0
    assert card.surface_coefficients[2] == 2.5


def test_rpp():
    card_string = "15000 rpp -1 1 -1 1 -1 1"
    card = MCNPSurfaceCard(card_string)
    assert card.surface_type == SurfaceCard.SurfaceType["MACRO_RPP"]
    assert card.surface_id == 15000
    assert card.surface_coefficients[0] == -1.0
    assert card.surface_coefficients[1] == 1.0
    assert card.surface_coefficients[2] == -1.0
    assert card.surface_coefficients[3] == 1.0
    assert card.surface_coefficients[4] == -1.0
    assert card.surface_coefficients[5] == 1.0


def test_box():
    card_string = "15000 box -1 -1 -1 2 0 0 0 2 0 0 0 2"
    card = MCNPSurfaceCard(card_string)
    assert card.surface_type == SurfaceCard.SurfaceType["MACRO_RPP"]
    assert card.surface_id == 15000
    assert card.surface_coefficients[0] == -1.0
    assert card.surface_coefficients[1] == 1.0
    assert card.surface_coefficients[2] == -1.0
    assert card.surface_coefficients[3] == 1.0
    assert card.surface_coefficients[4] == -1.0
    assert card.surface_coefficients[5] == 1.0


def test_surfacetransform_detect():
    card = "1 2 px 3"
    assert surface_has_transform(card)
    card = "1 PX 3"
    assert not surface_has_transform(card)


def test_bounding_box_px():
    card_string = "1 px 3"
    card = MCNPSurfaceCard(card_string)
    box = card.bounding_box()
    assert box[0] == 3
    assert box[1] == 3
    assert box[2] == 0
    assert box[3] == 0
    assert box[4] == 0
    assert box[5] == 0

# generate a bounding box for py
"""
def test_bounding_box_py():
    card_string = "1 py 3"
    card = MCNPSurfaceCard(card_string)
    box = card.bounding_box()
    assert box[0] ==0
    assert box[1] ==0
    assert box[2] ==3
    assert box[3] ==3
    assert box[4] ==0
    assert box[5] ==0
"""
