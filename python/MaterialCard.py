#!/usr/env/python3

from Card import Card
from MaterialData import MaterialData


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
    mat_data = 0

    # constructor
    def __init__(self, material_number = 0, card_string = ""):
        Card.__init__(self,card_string)
        self.material_number = material_number
        self.mat_data = MaterialData()

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

    # explode elements loop through the dictionary and any material that has elements
    # and explode it into its nuclidewise definition
    def explode_elements(self):
        keys_to_remove = []
        new_nuclides = {}
        for nuc in self.composition_dictionary:
            if int(nuc)%1000 == 0 :
                keys_to_remove.append(nuc)
                nuclides = self.mat_data.get_nucs(int(nuc))
                # loop over the nuclides
                for nuclide in nuclides:
                    if self.composition_dictionary[nuc] < 0: # if its mass fraction then 
                        new_nuclides[str(nuclide)] = self.composition_dictionary[nuc] * \
                        self.mat_data.natural_abund_map[nuclide*10000] \
                        / 100 * self.mat_data.atomic_mass(int(nuc))/self.mat_data.get_aa(nuclide)     
                    else: #its atom fraction pure multiplication
                        new_nuclides[str(nuclide)] = self.composition_dictionary[nuc]*self.mat_data.natural_abund_map[nuclide*10000]/100


        #print(self.composition_dictionary)
        for key in keys_to_remove:
            del self.composition_dictionary[key]

        for key in new_nuclides.keys():
            self.composition_dictionary[key] = new_nuclides[key]
            self.xsid_dictionary[key] = ""
        