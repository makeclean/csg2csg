from csg2csg.ParticleNames import ParticleNames
from csg2csg.MCNPParticleNames import particleToMCNP, mcnpToParticle


def test_generic():
    for particle in ParticleNames:
        name = particleToMCNP(particle)
        assert isinstance(name, str)
        assert len(name) > 0
        assert mcnpToParticle(name) == particle
