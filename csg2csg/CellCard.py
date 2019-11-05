#/usr/env/python3

from csg2csg.Card import Card
from enum import Enum

class CellCard(Card):
    """ Class for the storage of the Generic CellCard type 
    methods for the generation of CellCards should be placed
    here. Classes instanciating CellCard objects should be 
    implemented in its own CodeCellCard.py file
    """

    class OperationType(Enum):
        def __str__(self):
            return str(self.value)

        NOT = 2
        UNION = 1
        AND = 0

    # constructor for the cellcard class
    def __init__(self,card_string):
        
        self.cell_comment = ""
        self.cell_id = 0
        self.cell_density = 0
        self.cell_material_number = 0
        self.cell_importance = 1 # note any importance - we assume everything else is 0
        self.cell_text_description = ""
        self.cell_interpreted = ""
        self.cell_fill = 0
        self.cell_universe = 0
        self.cell_universe_offset = 0
        self.cell_universe_rotation = 0
        self.cell_universe_transformation_id = "0" # if there is a cell_universe tr number it should be purged
                                        # and converted into an offset and rotation
        self.cell_surface_list = set() # list of surfaces used in the cell definition

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
        string += "Surfs in Cell " + str(self.cell_surface_list) + "\n"
        return string

    """ Look for surface new in the list
    and replace with surface reference
    """
    def replace_surface(self,reference_surface,new,reverse):
        #self.cell_surface_list.remove(reference_surface)
        #self.cell_surface_list.add(new)
        print('ref ',reference_surface,' new ',new)
        # loop over the cell looking for surfaces
        for idx,item in enumerate(self.cell_interpreted):
            # if the surface has -ve or +ve sense and doesnt
            # need reversing just insert it
            if not isinstance(item, self.OperationType) and item not in {'(',')'}:                
                surf = int(item)
                if abs(surf) == new and surf == new and not reverse:
                    self.cell_interpreted[idx] = str(int(reference_surface))
                elif abs(surf) == new and surf != new and not reverse:
                   self.cell_interpreted[idx] = str(-1*int(reference_surface))
                elif abs(surf) == new and surf != new and reverse:
                    self.cell_interpreted[idx] = str(int(reference_surface))
                elif abs(surf) == new and surf == new and reverse:
                    self.cell_interpreted[idx] = str(-1*int(reference_surface))
        return