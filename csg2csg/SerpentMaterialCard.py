#!/usr/env/python3

from csg2csg.MaterialCard import MaterialCard
from csg2csg.MCNPFormatter import get_fortran_formatted_number

# write a specific serpent material card
def write_serpent_material(filestream, material):

    string = "% " + material.material_name  +"\n"
    string += "mat " + str(material.material_number) + " "
    string += str(material.density)

    # if its a non tally material set the relevant colour
    if material.material_colour:
        string += " rgb " + material.material_colour + "\n"
    else:
        string += "\n"
        
    for nuc in material.composition_dictionary:
        string += '{} {:e} \n'.format(nuc, material.composition_dictionary[nuc])
    filestream.write(string)
    return

""" Class to handle SerpentMaterialCard tranlation
"""
class SerpentMaterialCard(MaterialCard):
    
    def __init__(self, material_number, material_name, material_density, card_string):
        MaterialCard.__init__(self, material_number, card_string)
        self.material_name = material_name
        self.material_number = material_number
        self.density = material_density
        self.__process_string()

    # populate the Serpent Material Card
    def __process_string(self):
        # need to reset the dictionary
        # otherwise state seems to linger - weird
        self.composition_dictionary = {}

        mat_string = self.text_string
        mat_string = mat_string.replace("\n"," ")
        
        # split string
        tokens = mat_string.split()
        
        if len(tokens)%2 != 0:
            raise Exception("Material string not correctly processed")

        while len(tokens) != 0:
            nuclide = tokens[0].split(".")
            nucid = nuclide[0]
            try:
                xsid = nuclide[1]
            except:
                xsid = ""
            frac = get_fortran_formatted_number(tokens[1])
            tokens.pop(0)
            tokens.pop(0)
            self.composition_dictionary[nucid] = frac
            self.xsid_dictionary[nucid] = xsid
        return