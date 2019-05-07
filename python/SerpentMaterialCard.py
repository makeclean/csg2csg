#!/usr/env/python3

from MaterialCard import MaterialCard

# write a specific serpent material card
def write_serpent_material(filestream, material):
    string = "% " + material.material_name  +"\n"
    string += "mat " + str(material.material_number) + " "
    string += str(material.density)
    # if its a non tally material set the relevant colour
    if material.material_colour != 0:
        string += " rgb " + material.material_colour + "\n"
    for nuc in material.composition_dictionary:
        string += '{} {:e} \n'.format(nuc, material.composition_dictionary[nuc])
    filestream.write(string)
    return

""" Class to handle SerpentMaterialCard tranlation
"""
class SerpentMaterialCard(MaterialCard):
    def __init__(self, card_string):
        MaterialCard.__init__(self, card_string)
