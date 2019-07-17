#!/usr/env/python3

import unittest
import sys
sys.path.append("..")
 
from MCNPMaterialCard import MCNPMaterialCard
from MCNPInput import MCNPInput

class TestMCNPMaterial(unittest.TestCase):

    def test_mcnp_material(self):
        string ="29063 6.917000e-01 \n" + \
                "29065.31c 3.083000e-01 \n"
        number = 1
        name = "M1"
        matcard = MCNPMaterialCard(number,string)

        self.assertEqual(matcard.material_number,number)
        self.assertEqual(matcard.material_name,name)
        self.assertEqual(len(matcard.composition_dictionary),2)
        
        self.assertEqual(list(matcard.composition_dictionary.keys())[0],'29063')
        self.assertEqual(list(matcard.composition_dictionary.keys())[1],'29065')
        
        self.assertEqual(list(matcard.composition_dictionary.values())[0],6.917000e-01)
        self.assertEqual(list(matcard.composition_dictionary.values())[1],3.083000e-01)
        
        self.assertEqual(len(matcard.xsid_dictionary),2)

        self.assertEqual(list(matcard.xsid_dictionary.keys())[0],'29063')
        self.assertEqual(list(matcard.xsid_dictionary.keys())[1],'29065')

        self.assertEqual(list(matcard.xsid_dictionary.values())[0],'')
        self.assertEqual(list(matcard.xsid_dictionary.values())[1],'31c')

if __name__ == '__main__':
    unittest.main()
