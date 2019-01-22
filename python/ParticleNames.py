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

def particleToGeneric(particle_name):
    if particle_name == ParticleNames["NEUTRON"]:
        return "Neutron"
    if particle_name == ParticleNames["PHOTON"]:
        return "Photon"
    if particle_name == ParticleNames["ELECTRON"]:
        return "Electron"
    if particle_name == ParticleNames["POSITRON"]:
        return "Positron"