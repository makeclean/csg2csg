#/usr/env/python3

from CellCard import CellCard
from enum import Enum


# if the string is a cell card or not
def is_cell_card(line):
    cell_card = line.split()
    cellid = int(cell_card[0])
    mat_num = int(cell_card[1])
    if cellid and mat_num == 0:
        return True
    elif cellid > 0 and mat_num > 0:
        try:
            float(cell_card[2])
        except ValueError:
            print (cell_card[2]," cannot be converted to float")
        return True
    return False

# turn the generic operation type into a mcnp relevant text string
def mcnp_op_from_generic(Operation):
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
def write_mcnp_cell(filestream, CellCard):
    string = str(CellCard.cell_id) + " "
    
    string += str(CellCard.cell_material_number) + " "
    if CellCard.cell_material_number != 0:
        string += str(CellCard.cell_density) + " "

    string += "( "
    
    # build the cell description
    for item in CellCard.cell_interpreted:
        string += mcnp_op_from_generic(item)

    string += " ) " 

    string += "\n"   

    filestream.write(string)

class MCNPCellCard(CellCard):
    """ Class for the instanciation of generic cell cards
    from MCNP cell card strings
    """

    # constructor
    def __init__(self,card_string):
        CellCard.__init__(self,card_string)
        self.__interpret()

    # check the cell text description for parentheses
    # or not symbols these need extra work
    def __is_sanitised(self):
        if "#" in self.cell_text_description:
            return False
        elif "(" or ")" in self.cell_text_description:
            return False
        else:
            return True

    # method to break mcnp cell definition into something
    # a mere mortal can understand turns mcnp description
    # like 2 3 -4 into 2 AND 3 AND -4
    def generalise(self):
        cell_description = self.cell_text_description
        cell_description = list(cell_description)
        idx = 1
        while True:
            s = cell_description[idx]
            if s is ":":
                cell_description[idx] = CellCard.OperationType["UNION"]
                idx += 1
            elif s is "#":
                cell_description[idx] = CellCard.OperationType["NOT"]
                idx += 1
            elif s is ("(" or  ")"):
                idx += 1
                continue
            elif isinstance(s,str) and cell_description[idx-1] is not "(" and cell_description[idx] is not ")":
                cell_description.insert(idx,CellCard.OperationType["AND"])
                idx += 1
            idx += 1
            if idx == len(cell_description): break

        self.cell_interpreted = cell_description    
        return

    # generally spaceify the text so that between each item
    # there is only one space i.e (7:8) becomes ( 7 : 8 )
    def __sanitise(self):
        return
    
    # populute the part CellCard into its
    # consituent parts
    def __interpret(self):

        # expand the string first
        string = self.text_string
        string = string.replace("(", " ( ")
        string = string.replace(")", " ) ")
        string = string.replace(":", " : ")
        #tokens = self.text_string.split()
        tokens = string.split()

        self.cell_id = int(tokens[0])
        material_number = int(tokens[1])
        if material_number > 0 :
            self.cell_material_number = int(material_number)
            self.cell_density = float(tokens[2])
            self.cell_text_description = tokens[3:]
        else:
            self.cell_density = 0.
            self.cell_material_number = 0
            self.cell_text_description = tokens[2:]
            
        # now interpret the cell text description
        if not self.__is_sanitised():
            self.__sanitise()
        self.generalise()
        return

