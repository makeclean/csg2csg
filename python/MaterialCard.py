#!/usr/env/python3

from Card import Card

class MaterialCard(Card):

    """ A fully defined material card should have a name, a material number, 
    a density, a composition dictionary, and optionally a xsid dictionary.
    MCNP being an exception, most MC codes define the density of a material
    belonging to the material definition as opposed to a given cell. This 
    approach is taken here for maximal compability amongst codes.
    """

    material_name = ""
    material_number = 0
    composition_dictionary = {}
    xsid_dictionary = {}
    density = 0

    # constructor
    def __init__(self, material_number = 0, card_string = ""):
        Card.__init__(self,card_string)
        self.material_number = material_number

    def __str__(self):
        string = "Material: " + material_name + "\n"
        string += "Material num: " + str(material_number) + "\n"
        string += "Density: " + str(density) + "\n"
        string += "Composition \n"
        for item in composition_dictionary.keys():
            string += item + " " + composition_dictionary[item] + "\n"

        return string
    
