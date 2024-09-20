#!/usr/env/python3

from csg2csg.MCNPFormatter import mcnp_line_formatter

from csg2csg.UniverseCard import UniverseCard, uni_fill, mat_fill
import re
import math

# write the universe card for a scone universe given a generic cell card
def write_scone_universe(filestream, UniverseCard):

    # print (UniverseCard)
    # TODO support lattice universes
    string = str(UniverseCard.universe_id) + "{ type "
    if UniverseCard.is_root:
        string += "rootUniverse; "
        string += "border " + str(UniverseCard.border_surface) + "; "
        if UniverseCard.fill_type == uni_fill:
            string += "fill u<" + str(UniverseCard.fill_id) + ">; "
        else:
            string += "fill " + str(UniverseCard.fill_material) + "; "
    else:
        string += "cellUniverse; "
        string += "cells (" + str(UniverseCard.cell_list) + "); "
    
    # Need to increment by 1 due to SCONE not allowing Universe ID = 0
    # This is used by other codes to denote the base/root universe
    string += "id " + str(UniverseCard.universe_id + 1) +"; "

    # Include transformations
    if UniverseCard.origin != 0:
        # Convert origin to a translation
        string += "translation ("
        for i in range(3):
            string += str(UniverseCard.origin[i]) +" "
        string += "); "

    if UniverseCard.rotation != 0:
        # Convert rotation matrix to Euler angles following ZXZ convention
        # Need to double check conventions: rotate[5] might have a negative
        # sign and rot[2] might be * -1
        rotate = UniverseCard.rotation
        rot[0] = math.atan2(rotate[2],-rotate[5])
        rot[1] = math.acos(rotate[8])
        rot[2] = math.atan2(rotate[6],rotate[7])
        rot = math.degrees(rot)
        string += "rotation ("
        for i in range(3):
            string += str(rot[i]) +" "
        string += "); "
    string += " } \n"
    
    # removes any multiple spaces
    string = re.sub(" +", " ", string)
    string = mcnp_line_formatter(string)
    filestream.write(string)

class SCONEUniverseCard(UniverseCard):
    def __init__(self, card_string):
        UniverseCard.__init__(self, card_string)

