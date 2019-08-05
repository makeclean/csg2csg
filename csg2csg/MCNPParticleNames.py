#!/usr/env/python3 

from csg2csg.ParticleNames import ParticleNames

def particleToMCNP(particle_name):
    if particle_name == ParticleNames["NEUTRON"]:
        return "n"
    if particle_name == ParticleNames["PHOTON"]:
        return "p"
    if particle_name == ParticleNames["ELECTRON"]:
        return "e"
    if particle_name == ParticleNames["POSITRON"]:
        return "f"
    if particle_name == ParticleNames["PROTON"]:
        return "h"
    if particle_name == ParticleNames["DEUTERON"]:
        return "d"
    if particle_name == ParticleNames["TRITON"]:
        return "t"
    if particle_name == ParticleNames["ALPHA"]:
        return "a"
    if particle_name == ParticleNames["PION_PLUS"]:
        return "/"
    if particle_name == ParticleNames["PION_NEUT"]:
        return "z"
    if particle_name == ParticleNames["PION_NEG"]:
        return "*"
    if particle_name == ParticleNames["HELION"]:
        return "s"
    if particle_name == ParticleNames["MUON_NEG"]:
        return "|"

def mcnpToParticle(particle_name):
    if particle_name == "n":
        return ParticleNames["NEUTRON"]
    if particle_name == "p":
        return ParticleNames["PHOTON"]
    if particle_name == "e":
        return ParticleNames["ELECTRON"]
    if particle_name == "f":
        return ParticleNames["POSITRON"]
    if particle_name == "h":
        return ParticleNames["PROTON"]
    if particle_name == "d":
        return ParticleNames["DEUTERON"]
    if particle_name == "t":
        return ParticleNames["TRITON"]
    if particle_name == "a":
        return ParticleNames["ALPHA"]
    if particle_name == "/":
        return ParticleNames["PION_PLUS"]
    if particle_name == "z":
        return ParticleNames["PION_NEUT"]
    if particle_name == "*":
        return ParticleNames["PION_NEG"]
    if particle_name == "s":
        return ParticleNames["HELION"]
    if particle_name == "|":
        return ParticleNames["MUON_NEG"]
