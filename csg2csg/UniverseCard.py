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
    def __init__(self, card_string):
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
        Card.__init__(self, card_string)

    # print method
    def __str__(self):
        string = "Universe Card: \n"
        string += "Universe ID " + str(self.cell_id) + "\n"
        string += "Comment " + str(self.cell_comment) + "\n"
        string += "Is cell universe? " + str(cell_universe) + "\n"
        if self.cell_universe:
            string += "Cells in Universe " + str(self.cell_list) + "\n"
        string += "Is root? " + str(self.is_root) + "\n"
        if self.is_root:
            string += "Bounding surface " + str(self.bounding_surface) + "\n"
            if self.fill_type == uni_fill:
                string += "Contains universe " + str(self.fill_id) + "\n"
            else:
                string += "Contains material " + self.fill_mat + "\n"
        return string

    # Build from CellCard list
    # Loops through cell list to identify any cells it contains.
    # Also identifies which cells contain it and takes their
    # cell transformations as its own.
    def build_from_cell_list(self, id, cell_list):
        self.cell_list = []
        self.universe_id = id

        # This is the root universe
        if id == 0:
            self.is_root = 1
        
        for cell in cell_list:

            # Universe contains this cell
            if cell.cell_universe == id:
                self.cell_list.append(cell.cell_id)

                # Root universe cell must be defined by only one surface
                if id == 0:
                    self.bounding_surface = abs(cell.surfaces[0].surface_id)
                

            # Universe is contained by this cell
            if cell.cell_fill == id:

                # Apply rotations and transformations as appropriate
                if cell.cell_universe_rotation != 0:
                    self.rotation = cell.cell_universe_rotation

                if cell.cell_universe_translation != 0:
                    self.translation = cell.cell_universe_translation




