#!/usr/env/python3

from MaterialCard import MaterialCard

# writes an mcnp material card given the generic description
def write_mcnp_material(filestream, Material, preserve_xs):
    filestream.write("C Material " + str(Material.material_name) + "\n")
    filestream.write("M"+ str(Material.material_number) + "\n")
    for nucid in Material.composition_dictionary:
        string = "        " + str(nucid)
        if preserve_xs:
            string += "." + str(Material.xsid_dictionary[nucid])
        string += " " + str(Material.composition_dictionary[nucid]) + "\n"
        filestream.write(string)
    return

# Class to handle MCNP Material Card
class MCNPMaterialCard(MaterialCard):
    
    def __init__(self, material_number, card_string):
        MaterialCard.__init__(self, material_number, card_string)
        self.material_name = "M"+str(material_number)
        self.material_number = material_number
        self.__process_string()

    # populate the MCNP Material Card
    def __process_string(self):
        tokens = self.text_string.split()
        # need to reset the dictionary
        # otherwise state seems to linger - weird
        self.composition_dictionary = {}

        if len(tokens)%2 != 0:
            print ("Material string not correctly processed")
            sys.exit(1)
        while len(tokens) != 0:
            nuclide = tokens[0].split(".")
            nucid = nuclide[0]
            xsid = nuclide[1]
            frac = tokens[1]
            tokens.pop(0)
            tokens.pop(0)
            self.composition_dictionary[nucid] = frac
            self.xsid_dictionary[nucid] = xsid
        return
