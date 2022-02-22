#!/usr/env/python3

import unittest
import sys

sys.path.append("..")

from csg2csg.MaterialData import MaterialData


class TestMaterialDataMethods(unittest.TestCase):
    def test_get_nucs(self):
        mat_data = MaterialData()
        nuclides = mat_data.get_nucs(1000)
        self.assertEqual(len(nuclides), 2)
        self.assertEqual(1001 in nuclides, True)
        self.assertEqual(1002 in nuclides, True)

    def test_get_nucs_fe(self):
        mat_data = MaterialData()
        nuclides = mat_data.get_nucs(26000)
        self.assertEqual(len(nuclides), 4)
        self.assertEqual(26054 in nuclides, True)
        self.assertEqual(26056 in nuclides, True)
        self.assertEqual(26057 in nuclides, True)
        self.assertEqual(26058 in nuclides, True)

    def test_get_nucs_u(self):
        mat_data = MaterialData()
        nuclides = mat_data.get_nucs(92000)
        self.assertEqual(len(nuclides), 3)
        self.assertEqual(92234 in nuclides, True)
        self.assertEqual(92235 in nuclides, True)
        self.assertEqual(92238 in nuclides, True)

    def test_atomic_mass_calc(self):
        mat_data = MaterialData()
        atomic_mass = mat_data.atomic_mass(1000)
        self.assertEqual(atomic_mass, 1.0079407540557772)

        atomic_mass = mat_data.atomic_mass(2000)
        self.assertEqual(atomic_mass, 4.002601932120928)

        atomic_mass = mat_data.atomic_mass(26000)
        self.assertEqual(atomic_mass, 55.84514442998594)

    def test_zz_zaid(self):
        mat_data = MaterialData()
        zz = mat_data.get_zz(1001)
        self.assertEqual(zz, 1)
        zz = mat_data.get_zz(26000)
        self.assertEqual(zz, 26)
        zz = mat_data.get_zz(92000)
        self.assertEqual(zz, 92)

    def test_aa_zaid(self):
        mat_data = MaterialData()
        aa = mat_data.get_aa(1001)
        self.assertEqual(aa, 1)
        aa = mat_data.get_aa(26000)
        self.assertEqual(aa, 0)
        aa = mat_data.get_aa(92235)
        self.assertEqual(aa, 235)


if __name__ == "__main__":
    unittest.main()
