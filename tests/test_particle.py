from csg2csg.ParticleNames import particleToGeneric, ParticleNames


def test_generic():
    assert particleToGeneric("NEUTRON") is None
    assert "Neutron" == particleToGeneric(ParticleNames["NEUTRON"])
    assert "Electron" == particleToGeneric(ParticleNames["ELECTRON"])
    assert "Positron" == particleToGeneric(ParticleNames["POSITRON"])
    assert "Proton" == particleToGeneric(ParticleNames["PROTON"])
    assert "Deuteron" == particleToGeneric(ParticleNames["DEUTERON"])
    assert "Triton" == particleToGeneric(ParticleNames["TRITON"])
    assert "Alpha" == particleToGeneric(ParticleNames["ALPHA"])
    assert "Positive Pion" == particleToGeneric(ParticleNames["PION_PLUS"])
    assert "Negative Pion" == particleToGeneric(ParticleNames["PION_NEG"])
    assert "Helion" == particleToGeneric(ParticleNames["HELION"])
    assert "Negative Muon" == particleToGeneric(ParticleNames["MUON_NEG"])
