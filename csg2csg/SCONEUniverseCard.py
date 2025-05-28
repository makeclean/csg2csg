#!/usr/env/python3

from csg2csg.MCNPFormatter import mcnp_line_formatter

from csg2csg.UniverseCard import UniverseCard, uni_fill, mat_fill
import re
import math

# write the universe card for a scone universe given a generic cell card
def write_scone_universe(filestream, UniverseCard):

    # print (UniverseCard)
    # TODO support lattice universes
    if UniverseCard.is_root:
        string = "root { type "
        string += "rootUniverse; "
        string += "border " + str(UniverseCard.border_surface) + "; "
        if UniverseCard.fill_type == uni_fill:
            string += "fill u<" + str(UniverseCard.fill_id + 1) + ">; "
        if UniverseCard.fill_type == mat_fill:
            # Name preceded by an m due to SCONE weirdness
            string += "fill m" + str(UniverseCard.fill_material) + "; "
    else:
        string = str(UniverseCard.universe_id + 1) + " { type "
        string += "cellUniverse; cells ("
        for cell_id in UniverseCard.cell_list:
            string += str(cell_id) + " "
        string += "); "
    
    # Need to increment by 1 due to SCONE not allowing Universe ID = 0
    # This is used by other codes to denote the base/root universe
    string += "id " + str(UniverseCard.universe_id + 1) +"; "

    # Include transformations
    if UniverseCard.universe_offset != 0:
        # Convert origin to a translation
        string += "translation ("
        for i in range(3):
            string += str(UniverseCard.universe_offset[i]) +" "
        string += "); "

    if UniverseCard.universe_rotation != 0:
        # Convert rotation matrix to Euler angles following ZXZ convention
        # Need to double check conventions: rotate[5] might have a negative
        # sign and rot[2] might be * -1
        rotate = UniverseCard.universe_rotation
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


