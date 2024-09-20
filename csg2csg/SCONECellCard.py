#!/usr/env/python3

from csg2csg.MCNPFormatter import mcnp_line_formatter

from csg2csg.CellCard import CellCard
from enum import Enum
import re
import math

# turn the generic operation type into a scone relevant text string
def scone_op_from_generic(Operation):
    # if we are not of type operator - we are string do nowt
    if not isinstance(Operation, CellCard.OperationType):
        if Operation == "(":
            return " < "
        elif Operation == ")":
            return " > "
        else:
            return Operation
    else:
        # otherwise we need to do something
        if Operation == CellCard.OperationType["NOT"]:
            string = " # "
        elif Operation == CellCard.OperationType["AND"]:
            string = " "
        elif Operation == CellCard.OperationType["UNION"]:
            string = " : "
        else:
            string = "unknown operation"
    # return the operation
    return string


# write the cell card for a scone cell given a generic cell card
def write_scone_cell(filestream, CellCard):

    # If cell is in the root universe and outside the boundary, skip it.
    # Presently assumes only two cells in the root, with one surface,
    # as in Serpent.
    if CellCard.universe == 0 and CellCard.surfaces[0] >= 0:
        return

    #    print (CellCard)
    string = str(CellCard.cell_id) + "{type unionCell; id " 
    string += str(cellCard.cell_id) + "; " 
    
    # Need to keep track of universe definitions and return
    # to write these separately
    if CellCard.cell_fill != 0:
        string += " filltype uni; universe " + str(CellCard.cell_fill) + "; "

    # Doesn't have a universe - has a material
    if CellCard.cell_fill == 0:
        # material 0 is void
        string += " filltype mat; material "
        if CellCard.cell_material_number == 0:
            string += " void; "
        else:
            string += str(CellCard.cell_material_number) + " "

    string += "surfaces [ "

    # build the cell description
    for item in CellCard.cell_interpreted:
        string += serpent_op_from_generic(item)

    string += " ]; }\n"

    # removes any multiple spaces
    string = re.sub(" +", " ", string)

    string = mcnp_line_formatter(string)

    filestream.write(string)

class SCONECellCard(CellCard):
    def __init__(self, card_string):
        CellCard.__init__(self, card_string)
