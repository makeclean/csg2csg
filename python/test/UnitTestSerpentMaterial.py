#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
 
from SerpentMaterialCard import SerpentMaterialCard
from SerpentInput import SerpentInput

class TestSerpentMaterial(unittest.TestCase):

    def test_serpent_material(self):
        string ="29063 6.917000e-01 \n" + \
                "29065 3.083000e-01 \n"
        number = 1
        name = "copper"
        density = 8.93
        matcard = SerpentMaterialCard(number,name,density,string)

        self.assertEqual(matcard.density,density)
        self.assertEqual(matcard.material_number,number)
        self.assertEqual(matcard.material_name,name)

    def test_serpent_mat_input(self):
        string = ["mat 1 8.93\n", \
                "29063 6.917000e-01\n" ,\
                "29065 3.083000e-01\n"]
        print(string)
        serpent = SerpentInput()
        serpent.file_lines = string
        serpent.process()


if __name__ == '__main__':
    unittest.main()
