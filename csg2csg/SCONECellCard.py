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

    #    print (CellCard)
    string = str(CellCard.cell_id) + "{type unionCell; id " + str(cellCard.cell_id) + "; "
    string += " " + str(CellCard.cell_universe) + " "
    # Is it possible to fill with universes???
    # May need to keep track of universe definitions and return
    # to write these separately
    if CellCard.cell_fill != 0:
        string += " filltype mat; material " + str(CellCard.cell_fill) + "; "

    # base level universe cant have material
    if CellCard.cell_fill == 0:
        # material 0 is void
        if CellCard.cell_material_number == 0:
            string += " filltype mat; material void; "
        else:
            string += str(CellCard.cell_material_number) + " "

    string += "[ "

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
