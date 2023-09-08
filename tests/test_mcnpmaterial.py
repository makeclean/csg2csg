from csg2csg.MCNPMaterialCard import MCNPMaterialCard


def test_mcnp_material():
    string = (
        "29063 6.917000e-01 \n"
        "29065.31c 3.083000e-01 \n"
    )
    number = 1
    name = "M1"
    matcard = MCNPMaterialCard(number, string)

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


def test_mcnp_material_with_duplicates():
    string = (
        "29063 2.e-00 \n"
        "29063 1.e-00 \n"
        "29065.31c 3.083000e-01 \n"
    )
    number = 1
    name = "M1"
    matcard = MCNPMaterialCard(number, string)

    assert matcard.material_number == number
    assert matcard.material_name == name
    assert len(matcard.composition_dictionary) == 2

    assert list(matcard.composition_dictionary.keys())[0] == "29063"
    assert list(matcard.composition_dictionary.keys())[1] == "29065"

    assert list(matcard.composition_dictionary.values())[0] == 3.
    assert list(matcard.composition_dictionary.values())[1] == 3.083000e-01

    assert len(matcard.xsid_dictionary) == 2

    assert list(matcard.xsid_dictionary.keys())[0] == "29063"
    assert list(matcard.xsid_dictionary.keys())[1] == "29065"

    assert list(matcard.xsid_dictionary.values())[0] == ""
    assert list(matcard.xsid_dictionary.values())[1] == "31c"


def test_mcnp_material_with_keywords():
    string = (
        "29063 6.917000e-01 \n"
        "29065.31c 3.083000e-01 \n"
        "hlib=.70h  pnlib=70u"
    )
    number = 1
    name = "M1"
    matcard = MCNPMaterialCard(number, string)

    assert matcard.material_number == number
    assert matcard.material_name == name
    assert len(matcard.composition_dictionary) == 2

    assert list(matcard.composition_dictionary.keys())[0] == "29063"
    assert list(matcard.composition_dictionary.keys())[1] == "29065"

    assert list(matcard.composition_dictionary.values())[0] == 6.917000e-01
    assert list(matcard.composition_dictionary.values())[1] == 3.083000e-01

    assert len(matcard.xsid_dictionary) == 2

    assert list(matcard.xsid_dictionary.keys())[0], "29063"
    assert list(matcard.xsid_dictionary.keys())[1], "29065"

    assert list(matcard.xsid_dictionary.values())[0] == ""
    assert list(matcard.xsid_dictionary.values())[1] == "31c"


def test_mcnp_material_with_keyword():
    string = (
        "29063 6.917000e-01 \n"
        "29065.31c 3.083000e-01 \n"
        "hlib=.70h"
    )
    number = 1
    name = "M1"
    matcard = MCNPMaterialCard(number, string)

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
