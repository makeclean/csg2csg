#!/usr/env/python3

from csg2csg.MCNPFormatter import mcnp_line_formatter

from csg2csg.CellCard import CellCard
from enum import Enum
import re
import math

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
    string += " " + str(CellCard.cell_universe) + " "
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

    string = mcnp_line_formatter(string)


    filestream.write(string)

    # write the universe transform
    if CellCard.cell_fill != 0: 
        string = ""
        if CellCard.cell_universe_offset != 0 or CellCard.cell_universe_rotation != 0:
            string = "trans f " + str(CellCard.cell_id) + " "

            # universe may have no traslation?
            if CellCard.cell_universe_offset != 0:
                for i in range(3):
                    string += str(CellCard.cell_universe_offset[i]) + " "
            else:
                string += " 0 0 0 "
    
            if CellCard.cell_universe_rotation != 0:
                for i in range(9):
                    value = float(CellCard.cell_universe_rotation[i])
                    # transofmr should be in radians
                    #value = math.cos(value/180.*math.pi)
                    string += str(value) + " "
            else:
                string += "1 0 0 0 1 0 0 0 1 " 
            string += "1 \n"

        filestream.write(string)


class SerpentCellCard(CellCard):
    def __init__(self, card_string):
        CellCard.__init__(self, card_string)

    
