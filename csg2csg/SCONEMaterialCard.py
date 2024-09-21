#!/usr/env/python3

from csg2csg.MaterialCard import MaterialCard
from csg2csg.MCNPFormatter import get_fortran_formatted_number

# write a specific serpent material card
def write_scone_material(filestream, MaterialCard):

    string = "! " + MaterialCard.material_name + " \n"
    string += str(MaterialCard.material_number) + " { \n"
    string += "composition { \n"
    for nuc in MaterialCard.composition_dictionary:
        string += "{} {:e}; \n".format(
                nuc, MaterialCard.composition_dictionary[nuc]
                )
    string += "} \n"

    # if its a non tally material set the relevant colour
    if MaterialCard.material_colour:
        string += "rgb (" + MaterialCard.material_colour + "); \n"

    string += "} \n"
    filestream.write(string)
    return

