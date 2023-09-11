from csg2csg.MaterialData import MaterialData


def test_get_nucs():
    mat_data = MaterialData()
    nuclides = mat_data.get_nucs(1000)
    assert len(nuclides) == 2
    assert 1001 in nuclides
    assert 1002 in nuclides


def test_get_nucs_fe():
    mat_data = MaterialData()
    nuclides = mat_data.get_nucs(26000)
    assert len(nuclides) == 4
    assert 26054 in nuclides
    assert 26056 in nuclides
    assert 26057 in nuclides
    assert 26058 in nuclides


def test_get_nucs_u():
    mat_data = MaterialData()
    nuclides = mat_data.get_nucs(92000)
    assert len(nuclides) == 3
    assert 92234 in nuclides
    assert 92235 in nuclides
    assert 92238 in nuclides


def test_atomic_mass_calc():
    mat_data = MaterialData()
    atomic_mass = mat_data.atomic_mass(1000)
    assert atomic_mass == 1.0079407540557772

    atomic_mass = mat_data.atomic_mass(2000)
    assert atomic_mass == 4.002601932120928

    atomic_mass = mat_data.atomic_mass(26000)
    assert atomic_mass == 55.84514442998594


def test_zz_zaid():
    mat_data = MaterialData()
    zz = mat_data.get_zz(1001)
    assert zz == 1
    zz = mat_data.get_zz(26000)
    assert zz == 26
    zz = mat_data.get_zz(92000)
    assert zz == 92


def test_aa_zaid():
    mat_data = MaterialData()
    aa = mat_data.get_aa(1001)
    assert aa == 1
    aa = mat_data.get_aa(26000)
    assert aa == 0
    aa = mat_data.get_aa(92235)
    assert aa == 235
