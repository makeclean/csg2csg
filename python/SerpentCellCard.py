#!/usr/env/python3

from CellCard import CellCard
from enum import Enum

# turn the generic operation type into a serpent relevant text string
def serpent_op_from_generic(Operation):
    # if we are not of type operator - we are string do nowt
    if not isinstance(Operation, CellCard.OperationType):
        return Operation
    else:
        # otherwise we need to do something
        if Operation is CellCard.OperationType["NOT"]:
            string = "#"
        elif Operation is CellCard.OperationType["AND"]:
            string = " "
        elif Operation is CellCard.OperationType["UNION"]:
            string = ":"
        else:
            string = "unknown operation"
    # return the operation
    return string

# write the cell card for a serpent cell given a generic cell card
def write_serpent_cell(filestream, CellCard):
    string = "cell " + str(CellCard.cell_id) + " 0 " # note the 1 refers to universe number
    string += str(CellCard.cell_material_number) + " "
    
    # build the cell description
    for item in CellCard.cell_interpreted:
        string += serpent_op_from_generic(item)
    string += "\n"
    

    filestream.write(string)

class SerpentCellCard(CellCard):
    def __init__(self, card_string):
        CellCard.__init__(self, card_string)

    
