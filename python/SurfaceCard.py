from Card import Card
from enum import Enum

class SurfaceCard(Card):
    """ Class for the storage of the generic SurfaceCard type
    Methods for the generation of flat geometry surface card data
    should be place here. Classes needing to write flat 
    surface card data should be implemented in its own
    CodeSurfaceCard.py file
    """
    
    surface_type = 0
    surface_id = 0
    surface_coefficients = []
    comment = ""
    
    class SurfaceType(Enum):
        PLANE_GENERAL = 1
        PLANE_X = 2
        PLANE_Y = 3
        PLANE_Z = 4
        CYLINDER_GENERAL = 5
        CYLINDER_X = 6
        CYLINDER_Y = 7
        CYLINDER_Z = 8
        SPHERE_GENERAL = 9
        TORUS_X = 10
        TORUS_Y = 11
        TORUS_Z = 12
    
    # constructor for building a surface card
    def __init__(self,card_string):
        Card.__init__(self,card_string)

    def __str__(self):
        string = "SurfaceCard: \n"
        string += "Surface ID " + str(self.surface_id)+"\n"
        string += "Surface Type " + str(self.surface_type)+"\n"
        string += "Surface Coefficients " + str(self.surface_coefficients)+"\n"
        string += "Comment: " + str(self.comment)+"\n"
        return string
        
    def set_type(self, surf_id, surf_type, coords):
        self.surface_id = surf_id
        self.surface_type = surf_type
        self.surface_coefficients = coords
        
        
