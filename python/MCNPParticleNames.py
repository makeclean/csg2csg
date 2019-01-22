#!/usr/env/python3 

from ParticleNames import ParticleNames

def particleToMCNP(particle_name):
    if particle_name == ParticleNames["NEUTRON"]:
        return "n"
    if particle_name == ParticleNames["PHOTON"]:
        return "p"
    if particle_name == ParticleNames["ELECTRON"]:
        return "e"
    if particle_name == ParticleNames["POSITRON"]:
        return "f"

def mcnpToParticle(particle_name):
    if particle_name == "n":
        return ParticleNames["NEUTRON"]
    if particle_name == "p":
        return ParticleNames["PHOTON"]
    if particle_name == "e":
        return ParticleNames["ELECTRON"]
    if particle_name == "f":
        return ParticleNames["POSITRON"]