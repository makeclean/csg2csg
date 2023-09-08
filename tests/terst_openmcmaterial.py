from csg2csg.OpenMCMaterial import zaid_to_name


def test_zaid_name_conversion():
    name = "1001"
    assert zaid_to_name(name) == "H1"
    name = "26056"
    print(name[0:0], name[1:1])
    assert zaid_to_name(name) == "Fe56"
    name = "53133"
    assert zaid_to_name(name) == "I133"
    name = "56133"
    assert zaid_to_name(name) == "Ba133"
    name = "118294"
    assert zaid_to_name(name) == "Og294"
