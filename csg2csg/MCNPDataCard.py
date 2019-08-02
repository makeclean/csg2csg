#!/usr/env/python3
import sys
from csg2csg.Card import Card
from csg2csg.Vector import cross
import math

import warnings

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

    def __str__(self):
        string = "transform: {0}\n".format(self.id)
        string += "shift: {0}\n".format(self.shift)
        string += "v1: {0}\n".format(self.v1)
        string += "v2: {0}\n".format(self.v2)
        string += "v3: {0}\n".format(self.v3)
        return string
    
    def set_shift(self,shift_):
        self.shift = shift_

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

        if len(tokens) == 13 or len(tokens) == 14: # fully defined transform
            self.v1 = [float(tokens[4]),
                       float(tokens[5]),
                       float(tokens[6])]
            self.v2 = [float(tokens[7]),
                       float(tokens[8]),
                       float(tokens[9])]
            self.v3 = [float(tokens[10]),
                       float(tokens[11]),
                       float(tokens[12])]

            # convert from degs to radians
            if self.angle_form:
                for i in range(3):
                    self.v1[i] = math.cos(self.v1[i]/180.*math.pi)
                    self.v2[i] = math.cos(self.v2[i]/180.*math.pi)
                    self.v3[i] = math.cos(self.v3[i]/180.*math.pi)
        elif len(tokens) == 10: # define the las transform as cross product
            self.v1 = [float(tokens[4]),
                       float(tokens[5]),
                       float(tokens[6])]
            self.v2 = [float(tokens[7]),
                       float(tokens[8]),
                       float(tokens[9])]
            # convert from degs to radians
            if self.angle_form:
                for i in range(3):
                    self.v1[i] = math.cos(self.v1[i]/180.*math.pi)
                    self.v2[i] = math.cos(self.v2[i]/180.*math.pi)
            self.v3 = cross(self.v1,self.v2)
        elif len(tokens) == 4: # just a translation 
            # shift already set and unitary rotation matrix
            # defined
            pass 
        else:
            warnings.warn('Unknown transform definition, ' + str(len(tokens)) + self.text_string,Warning)
          
        return

