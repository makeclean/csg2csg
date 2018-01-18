#!/usr/env/python3

from Card import Card
from Vector import cross

# Class to handle MCNP datacards
class MCNPDataCard(Card):
    def __init__(self, card_string):
        Card.__init__(self, card_string)

# Class to handle MCNP Transform Cards        
class MCNPTransformCard(MCNPDataCard):
    id = 0 # transform card number
    angle_form = 0 # 0 is radians, 1 is degrees
    # spatial shift
    shift = [0.,0.,0.]
    # default basis vector
    v1 = [1.,0.,0.]
    v2 = [0.,1.,0.]
    v3 = [0.,0.,1.]

    def __init__(self, card_string):
        MCNPDataCard.__init__(self, card_string)
        self.__process_string()

    # process the string into a transformation card
    def __process_string(self):
        tokens = self.text_string.split()
        # is the angle specificed in rads or degrees
        if "*" in tokens[0]:
            self.angle_form = 1
        else:
            self.angle_form = 0
        # id string 
        id_string = tokens[0].find("r") + 1
        self.id = tokens[0][id_string:]
        # the xyz shift of the tform
        self.shift = [float(tokens[1]),
                      float(tokens[2]),
                      float(tokens[3])]

        if len(tokens) == 13: # fully defined transform
            self.v1 = [float(tokens[4]),
                       float(tokens[5]),
                       float(tokens[6])]
            self.v2 = [float(tokens[7]),
                       float(tokens[8]),
                       float(tokens[9])]
            self.v3 = [float(tokens[10]),
                       float(tokens[11]),
                       float(tokens[12])]
        elif len(tokens) == 10: # define the las transform as cross product
            self.v1 = [float(tokens[4]),
                       float(tokens[5]),
                       float(tokens[6])]
            self.v2 = [float(tokens[7]),
                       float(tokens[8]),
                       float(tokens[9])]
            self.v3 = cross(self.v1,self.v2)
        else:
            print('Unknown transform definition')
            sys.exit(1)
        return

# Class to handle MCNP Material Card
class MCNPMaterialCard(MCNPDataCard):
    material_number = 0
    composition_dictionary = {}

    def __init__(self, material_number, card_string):
        MCNPDataCard.__init__(self, card_string)
        self.material_number = material_number
        self.__process_string()

    # print method
    def __str__(self):
        string =  "material " + self.material_number + "\n"
        for item in self.composition_dictionary.keys():
            string += item + " " + self.composition_dictionary[item] + "\n"
        return string

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
            nucid = tokens[0]
            frac = tokens[1]
            tokens.pop(0)
            tokens.pop(0)
            self.composition_dictionary[nucid] = frac
        return
