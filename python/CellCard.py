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
    cell_material_number = 0
    cell_importance = 1 # note any importance - we assume everything else is 0
    cell_comment = ""
    cell_text_description = ""
    cell_interpreted = ""
    cell_fill = 0
    cell_universe = 0
    cell_universe_offset = 0
    cell_universe_rotation = 0

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
        string += "Material Number " + str(self.cell_material_number) + "\n"
        string += "Material Density " + str(self.cell_density) + "\n"
        string += "Importance " + str(self.cell_importance) + "\n"
        string += "Comment " + str(self.cell_comment) + "\n"
        string += "Text Description " + str(self.cell_text_description) + "\n"
        string += "Cell Description " + str(self.cell_interpreted) + "\n"
        return string
