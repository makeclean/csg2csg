#!/usr/env/python3

from csg2csg.Card import Card
from csg2csg.MaterialData import MaterialData

colours = [0]*71
colours[0]="0 208 31"
colours[1]="0 0 255"
colours[2]="255 255 0"
colours[3]="0 255 0"
colours[4]="0 255 255"
colours[5]="255 164 0"
colours[6]="255 192 202"
colours[7]="159 31 239"
colours[8]="164 42 42"
colours[9]="111 128 144"
colours[10]="239 255 255"
colours[11]="222 184 134"
colours[12]="126 255 0"
colours[13]="255 0 255"
colours[14]="255 126 80"
colours[15]="255 248 220"
colours[16]="177 33 33"
colours[17]="255 214 0"
colours[18]="239 255 239"
colours[19]="239 230 139"
colours[20]="175 47 95"
colours[21]="218 111 213"
colours[22]="218 164 31"
colours[23]="221 159 221"
colours[24]="255 245 237"
colours[25]="159 82 44"
colours[26]="215 190 215"
colours[27]="255 98 70"
colours[28]="64 223 208"
colours[29]="245 222 179"
colours[30]="249 128 113"
colours[31]="95 158 159"
colours[32]="184 133 10"
colours[33]="84 107 46"
colours[34]="106 90 205"
colours[35]="255 139 0"
colours[36]="153 49 204"
colours[37]="143 187 143"
colours[38]="46 79 79"
colours[39]="255 19 146"
colours[40]="0 190 255"
colours[41]="249 235 214"
colours[42]="255 239 245"
colours[43]="172 215 230"
colours[44]="237 221 130"
colours[45]="255 182 193"
colours[46]="30 144 255"
colours[47]="255 159 121"
colours[48]="134 206 249"
colours[49]="255 255 223"
colours[50]="185 84 210"
colours[51]="175 196 222"
colours[52]="146 111 219"
colours[53]="255 69 0"
colours[54]="151 250 151"
colours[55]="174 237 237"
colours[56]="219 111 146"
colours[57]="223 255 255"
colours[58]="65 105 224"
colours[59]="187 143 143"
colours[60]="134 206 235"
colours[61]="0 255 126"
colours[62]="70 130 180"
colours[63]="255 0 0"
colours[64]="0 0 0"
colours[65]="0 0 255"
colours[66]="191 0 0"
colours[67]="0 255 0"
colours[68]="191 0 255"
colours[69]="255 255 0"
colours[70]="255 255 255"

# get the mcnp colour for the material
# this is mostly for automated testing
def get_material_colour(idx):
    # this obviously returns the same colour more than once
    # but this is what MCNP does so we duplicate this behavior
    return colours[idx%63] 

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
    material_colour = 0
    
    # constructor
    def __init__(self, material_number = 0, card_string = ""):
        Card.__init__(self,card_string)
        self.material_number = material_number
        self.mat_data = MaterialData()

    def __str__(self):
        string = "Material: " + self.material_name + "\n"
        string += "Material num: " + str(self.material_number) + "\n"
        string += "Density: " + str(self.density) + "\n"
        string += "Colour: " + str(self.material_colour) + "\n"
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
        
