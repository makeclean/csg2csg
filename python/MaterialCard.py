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
        string = "Material: " + self.material_name + "\n"
        string += "Material num: " + str(self.material_number) + "\n"
        string += "Density: " + str(self.density) + "\n"
        string += "Composition \n"
        for item in self.composition_dictionary.keys():
            string += item + " " + str(self.composition_dictionary[item]) + "\n"

        return string
    
    # normalise the material composition such that the sum is 1.0
    def normalise(self):
        sum = 0.
        # get the sum
        for nuc in self.composition_dictionary:
            sum += float(self.composition_dictionary[nuc])

        # dont divide by -ve number ! mass->atom
        sum = abs(sum)

        for nuc in self.composition_dictionary:
            self.composition_dictionary[nuc] = float(self.composition_dictionary[nuc])/sum

        # all done
        return
    
        
    
