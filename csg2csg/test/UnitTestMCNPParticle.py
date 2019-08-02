#!/usr/env/python3

import unittest
import sys
sys.path.append("..")

from ParticleNames import ParticleNames
from MCNPParticleNames import particleToMCNP,mcnpToParticle

class TestMCNPParticleMethods(unittest.TestCase):

    def test_generic(self):

        for i in range(len(list(ParticleNames))):
            self.assertEqual(particleToMCNP(i),mcnpToParticle(particleToMCNP(i)))

        

if __name__ == '__main__':
    unittest.main()
