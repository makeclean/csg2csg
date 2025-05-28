#!/usr/env/python3

from csg2csg.MaterialCard import MaterialCard
from csg2csg.MCNPFormatter import get_fortran_formatted_number

# write a specific scone material card
def write_scone_material(filestream, MaterialCard):

    string = "! " + MaterialCard.material_name + " \n"
    string += "m" + str(MaterialCard.material_number) + " { \n"
    string += "composition { \n"
    # Stick on .03 regardless until something to read temperature
    # from MCNP is added!
    # Multiply by adens because SCONE requires absolute densities
    dens = MaterialCard.density
    if dens > 0:
        adens = dens
    else:
        molar_mass = 0
        for nuc in MaterialCard.composition_dictionary:
            molar_mass += MaterialCard.composition_dictionary[nuc] * (int(nuc) % 1000)
            
        adens = -dens * 6.02214e-01 / molar_mass
    
    for nuc in MaterialCard.composition_dictionary:
        string += "{}.03 {:e}; \n".format(
                nuc, MaterialCard.composition_dictionary[nuc] * adens
                )

    string += "} \n"

    # set the relevant colour
    if MaterialCard.material_colour:
        string += "rgb (" + MaterialCard.material_colour + "); \n"

    string += "} \n"
    filestream.write(string)
    return
