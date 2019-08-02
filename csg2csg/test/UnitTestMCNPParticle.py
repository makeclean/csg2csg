#!/usr/env/python3

import unittest
import sys
sys.path.append("..")

from csg2csg.ParticleNames import ParticleNames
from csg2csg.MCNPParticleNames import particleToMCNP,mcnpToParticle

class TestMCNPParticleMethods(unittest.TestCase):

    def test_generic(self):

        for i in range(len(list(ParticleNames))):
            self.assertEqual(particleToMCNP(i),mcnpToParticle(particleToMCNP(i)))

        

if __name__ == '__main__':
    unittest.main()
