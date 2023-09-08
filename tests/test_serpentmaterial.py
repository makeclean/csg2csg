from csg2csg.SerpentMaterialCard import SerpentMaterialCard
from csg2csg.SerpentInput import SerpentInput


def test_serpent_material():
    string = (
        "29063 6.917000e-01 \n"
        "29065.31c 3.083000e-01 \n"
    )
    number = 1
    name = "copper"
    density = 8.93
    matcard = SerpentMaterialCard(number, name, density, string)

    assert matcard.density == density
    assert matcard.material_number == number
    assert matcard.material_name == name
    assert len(matcard.composition_dictionary) == 2

    assert list(matcard.composition_dictionary.keys())[0] == "29063"
    assert list(matcard.composition_dictionary.keys())[1] == "29065"

    assert list(matcard.composition_dictionary.values())[0] == 6.917000e-01
    assert list(matcard.composition_dictionary.values())[1] == 3.083000e-01

    assert len(matcard.xsid_dictionary) == 2

    assert list(matcard.xsid_dictionary.keys())[0] == "29063"
    assert list(matcard.xsid_dictionary.keys())[1] == "29065"

    assert list(matcard.xsid_dictionary.values())[0] == ""
    assert list(matcard.xsid_dictionary.values())[1] == "31c"


def test_serpent_mat_input():
    string = ["mat 1 8.93\n", "29063 6.917000e-01\n", "29065 3.083000e-01\n"]

    serpent = SerpentInput()
    serpent.file_lines = string
    serpent.process()
