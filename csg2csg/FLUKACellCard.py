#!/usr/env/python3

from csg2csg.CellCard import CellCard
from enum import Enum
import re

# turn the generic operation type into a serpent relevant text string
def fluka_op_from_generic(Operation):
    # if we are not of type operator - we are string do nowt
    if not isinstance(Operation, CellCard.OperationType):
        if Operation is "(":
            return " +"+Operation+" "
        elif Operation is ")":
            return " "+Operation+" "
        elif int(Operation) < 0:
            return " +S" + str(abs(int(Operation)))
        elif int(Operation) > 0:
            return " -S" + str(int(Operation))            
        else:
            return Operation
    else:
        # otherwise we need to do something
        if Operation is CellCard.OperationType["NOT"]:
            string = " -"
        elif Operation is CellCard.OperationType["AND"]:
            string = "  "
        elif Operation is CellCard.OperationType["UNION"]:
            string = " | "
        else:
            string = "unknown operation"
    # return the operation
    return string

# write the cell card for a fluka cell given a generic cell card
def write_fluka_cell(filestream, CellCard):
    
    string =  " C" + str(CellCard.cell_id) + " 5 " # number of adjacent cells
            
    string += "( "
    
    # build the cell description
    for item in CellCard.cell_interpreted:
        string += fluka_op_from_generic(item)

    string += " ) " 
    string += "\n"

    # removes any multiple spaces
    string = re.sub("  "," ",string)
    string = re.sub("\- \+"," -",string)

    filestream.write(string)

class FLUKACellCard(CellCard):
    def __init__(self, card_string):
        CellCard.__init__(self, card_string)

    
