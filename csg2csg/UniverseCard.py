# /usr/env/python3

from csg2csg.Card import Card
from enum import Enum

uni_fill = 1
mat_fill = 2

class UniverseCard(Card):
    """Class for the storage of the Generic UniverseCard type
    methods for the generation of UniverseCards should be placed
    here. Classes instanciating UniverseCard objects should be
    implemented in its own CodeUniverseCard.py file.
    This is primarily intended for SCONE - do any other codes
    have explicit cell universe cards? Maybe this is useful for
    translating lattices?
    """

    # constructor for the universecard class
    def __init__(self):
        self.universe_comment = ""
        self.universe_id = 0
        self.cell_list = set()
        self.fill_type = 0
        self.fill_id = 0
        self.fill_mat = ''
        self.offset = 0
        self.rotation = 0
        self.is_root = 0
        self.border_surface = 0
        self.universe_offset = 0
        self.universe_rotation = 0
        #Card.__init__(self, card_string)

    # print method
    def __str__(self):
        string = "Universe Card: \n"
        string += "Universe ID " + str(self.universe_id) + "\n"
        string += "Comment " + str(self.universe_comment) + "\n"
        string += "Is cell universe? " + str(bool(self.cell_list)) + "\n"
        if bool(self.cell_list):
            string += "Cells in Universe " + str(self.cell_list) + "\n"
        string += "Is root? " + str(self.is_root) + "\n"
        if self.is_root:
            string += "Bounding surface " + str(self.border_surface) + "\n"
            if self.fill_type == uni_fill:
                string += "Contains universe " + str(self.fill_id) + "\n"
            else:
                string += "Contains material " + self.fill_mat + "\n"
        return string

    # Build from CellCard list
    # Loops through cell list to identify any cells it contains.
    # Also identifies which cells contain it and takes their
    # cell transformations as its own.
    def build_from_cell_list(self, uni_id, cell_list):
        self.cell_list = []
        self.universe_id = uni_id

        #print(self.__str__())
        #print(uni_id)

        # This is the root universe
        if uni_id == 0:
            self.is_root = 1
        
        for cell in cell_list:

            # Universe contains this cell
            if cell.cell_universe == uni_id:
                self.cell_list.append(cell.cell_id)

                # Search the root universe for a cell which has a single
                # surface in which it is in the positive halfspace.
                # This is (probably??) the bounding surface.
                # The indicator that a cell is definitely in the positive
                # halfspace comes from cell_text_description. Check it for
                # a single entry which is positive.
                numeric_list = [item for item in cell.cell_text_description if item.lstrip('-').isdigit()]
                halfspaces = [int(x) for x in numeric_list]
                if (uni_id == 0 and len(halfspaces) == 1): 
                    surface_id = halfspaces[0]
                    if surface_id > 0:
                        self.border_surface = surface_id
                

            # Universe is contained by this cell
            if cell.cell_fill == uni_id:

                # Apply rotations and transformations as appropriate
                if cell.cell_universe_rotation != 0:
                    self.universe_rotation = cell.cell_universe_rotation

                if cell.cell_universe_offset != 0:
                    self.universe_offset = cell.cell_universe_offset




