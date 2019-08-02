#!/usr/env/python3

import unittest
import sys
sys.path.append("..")

from ParticleNames import particleToGeneric,ParticleNames

class TestParticleMethods(unittest.TestCase):

    def test_generic(self):
        self.assertEqual(None, particleToGeneric("NEUTRON"))
        self.assertEqual("Neutron", particleToGeneric(ParticleNames["NEUTRON"]))
        self.assertEqual("Electron", particleToGeneric(ParticleNames["ELECTRON"]))
        self.assertEqual("Positron", particleToGeneric(ParticleNames["POSITRON"]))
        self.assertEqual("Proton", particleToGeneric(ParticleNames["PROTON"]))
        self.assertEqual("Deuteron", particleToGeneric(ParticleNames["DEUTERON"]))        
        self.assertEqual("Triton", particleToGeneric(ParticleNames["TRITON"]))                
        self.assertEqual("Alpha", particleToGeneric(ParticleNames["ALPHA"]))                
        self.assertEqual("Positive Pion", particleToGeneric(ParticleNames["PION_PLUS"]))                
        self.assertEqual("Negative Pion", particleToGeneric(ParticleNames["PION_NEG"]))                
        self.assertEqual("Helion", particleToGeneric(ParticleNames["HELION"]))                
        self.assertEqual("Negative Muon", particleToGeneric(ParticleNames["MUON_NEG"]))                

if __name__ == '__main__':
    unittest.main()
