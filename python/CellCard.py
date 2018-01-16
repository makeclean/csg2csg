#/usr/env/python3

from Card import Card
from enum import Enum

class CellCard(Card):
    """ Class for the storage of the Generic CellCard type 
    methods for the generation of CellCards should be placed
    here. Classes instanciating CellCard objects should be 
    implemented in its own CodeCellCard.py file
    """

    cell_comment = ""
    cell_id = 0
    cell_density = 0
    cell_material_num = 0
    cell_comment = ""
    cell_text_description = ""
    cell_interpreted = ""

    class OperationType(Enum):
        NOT = 2
        UNION = 1
        AND = 0

    # constructor for the cellcard class
    def __init__(self,card_string):
        Card.__init__(self,card_string)

    # print method
    def __str__(self):
        string = "Cell Card: \n"
        string += "Cell ID " + str(self.cell_id) + "\n"
        string += "Comment " + str(self.cell_comment) + "\n"
        string += "Cell Description " + str(self.cell_interpreted) + "\n"
        return string
