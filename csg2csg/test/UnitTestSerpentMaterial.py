#!/usr/env/python3

import unittest
import sys

sys.path.append("..")

from csg2csg.SerpentMaterialCard import SerpentMaterialCard
from csg2csg.SerpentInput import SerpentInput


class TestSerpentMaterial(unittest.TestCase):
    def test_serpent_material(self):
        string = "29063 6.917000e-01 \n" + "29065.31c 3.083000e-01 \n"
        number = 1
        name = "copper"
        density = 8.93
        matcard = SerpentMaterialCard(number, name, density, string)

        self.assertEqual(matcard.density, density)
        self.assertEqual(matcard.material_number, number)
        self.assertEqual(matcard.material_name, name)
        self.assertEqual(len(matcard.composition_dictionary), 2)

        self.assertEqual(list(matcard.composition_dictionary.keys())[0], "29063")
        self.assertEqual(list(matcard.composition_dictionary.keys())[1], "29065")

        self.assertEqual(list(matcard.composition_dictionary.values())[0], 6.917000e-01)
        self.assertEqual(list(matcard.composition_dictionary.values())[1], 3.083000e-01)

        self.assertEqual(len(matcard.xsid_dictionary), 2)

        self.assertEqual(list(matcard.xsid_dictionary.keys())[0], "29063")
        self.assertEqual(list(matcard.xsid_dictionary.keys())[1], "29065")

        self.assertEqual(list(matcard.xsid_dictionary.values())[0], "")
        self.assertEqual(list(matcard.xsid_dictionary.values())[1], "31c")

    def test_serpent_mat_input(self):
        string = ["mat 1 8.93\n", "29063 6.917000e-01\n", "29065 3.083000e-01\n"]

        serpent = SerpentInput()
        serpent.file_lines = string
        serpent.process()


if __name__ == "__main__":
    unittest.main()
