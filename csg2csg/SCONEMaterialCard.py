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
    for nuc in MaterialCard.composition_dictionary:
        adens = MaterialCard.density
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

