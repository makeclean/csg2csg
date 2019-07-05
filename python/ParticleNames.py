#!/usr/env/python3

from enum import Enum

""" Class for the storage of the generic particle names
for translation of metadata downstream
"""
class ParticleNames(Enum):
    NEUTRON = 0
    PHOTON = 1
    ELECTRON = 2
    POSITRON = 3
    PROTON = 4
    DEUTERON = 5
    TRITON = 6
    ALPHA = 7
    PION_PLUS = 8
    PION_NEUT = 9
    PION_NEG = 10
    HELION = 11
    MUON_NEG = 12

def particleToGeneric(particle_name):
    if particle_name == ParticleNames["NEUTRON"]:
        return "Neutron"
    if particle_name == ParticleNames["PHOTON"]:
        return "Photon"
    if particle_name == ParticleNames["ELECTRON"]:
        return "Electron"
    if particle_name == ParticleNames["POSITRON"]:
        return "Positron"
    if particle_name == ParticleNames["PROTON"]:
        return "Proton"
    if particle_name == ParticleNames["DEUTERON"]:
        return "Deuteron"
    if particle_name == ParticleNames["TRITON"]:
        return "Triton"
    if particle_name == ParticleNames["ALPHA"]:
        return "Alpha"
    if particle_name == ParticleNames["PION_PLUS"]:
        return "Positive Pion"
    if particle_name == ParticleNames["PION_NEUT"]:
        return "Neutral Pion"
    if particle_name == ParticleNames["PION_NEG"]:
        return "Negative Pion"
    if particle_name == ParticleNames["HELION"]:
        return "Helion"
    if particle_name == ParticleNames["MUON_NEG"]:
        return "Negative Muon"