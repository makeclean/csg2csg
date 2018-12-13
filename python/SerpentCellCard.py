#!/usr/env/python3

from CellCard import CellCard
from enum import Enum
import re

# turn the generic operation type into a serpent relevant text string
def serpent_op_from_generic(Operation):
    # if we are not of type operator - we are string do nowt
    if not isinstance(Operation, CellCard.OperationType):
        if Operation is "(":
            return " "+Operation+" "
        elif Operation is ")":
            return " "+Operation+" "
        else:
            return Operation
    else:
        # otherwise we need to do something
        if Operation is CellCard.OperationType["NOT"]:
            string = " #"
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

#    print (CellCard)
    
    string = "cell " + str(CellCard.cell_id)
    # if CellCard.cell_universe == 0:
    string += " " + str(CellCard.cell_universe) + " "
    #   string += " 0 " # note the 0 refers to universe number
    if CellCard.cell_fill != 0 :
        string += " fill " + str(CellCard.cell_fill) + " "

    # cant base level universe cant have material
    if CellCard.cell_fill == 0:
      # material 0 is void
      if CellCard.cell_material_number == 0:
          string += "void "
      else:
          string += str(CellCard.cell_material_number) + " "
        
    string += "( "
    
    # build the cell description
    for item in CellCard.cell_interpreted:
        string += serpent_op_from_generic(item)

    string += " ) " 
    string += "\n"

    # removes any multiple spaces
    string = re.sub(" +"," ",string)

    filestream.write(string)

class SerpentCellCard(CellCard):
    def __init__(self, card_string):
        CellCard.__init__(self, card_string)

    
