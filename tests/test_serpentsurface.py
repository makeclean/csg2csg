from csg2csg.MCNPSurfaceCard import MCNPSurfaceCard
from csg2csg.SerpentSurfaceCard import serpent_cone_x


def test_cone_x_up_write():
    card = "1 k/x 0 0 0 0.5 1"
    surfcard = MCNPSurfaceCard(card)
    surfcard.b_box = [0, 10, 0, 0, 0, 0]
    result = serpent_cone_x(surfcard)
    assert result == " ckx 0.000000 0.000000 0.000000 0.500000 1.000000\n"


def test_cone_x_down_write():
    card = "1 k/x 0 0 0 0.5 -1"
    surfcard = MCNPSurfaceCard(card)
    surfcard.b_box = [0, 0, 0, 0, 0, 0]
    surfcard.b_box = [-10, 0, 0, 0, 0, 0]
    result = serpent_cone_x(surfcard)
    assert result == " ckx 0.000000 0.000000 0.000000 0.500000 -1.000000\n"
