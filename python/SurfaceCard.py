from Card import Card
from enum import Enum, auto

class SurfaceCard(Card):
    """ Class for the storage of the generic SurfaceCard type
    Methods for the generation of flat geometry surface card data
    should be place here. Classes needing to write flat 
    surface card data should be implemented in its own
    CodeSurfaceCard.py file
    """
    
    surface_type = 0
    surface_id = 0
    surface_transform = 0
    surface_coefficients = []
    comment = ""
    
    class SurfaceType(Enum):
        PLANE_GENERAL = auto()
        PLANE_X = auto()
        PLANE_Y = auto()
        PLANE_Z = auto()
        CYLINDER_X = auto()
        CYLINDER_Y = auto()
        CYLINDER_Z = auto()
        SPHERE_GENERAL = auto()
        TORUS_X = auto()
        TORUS_Y = auto()
        TORUS_Z = auto()
        GENERAL_QUADRATIC = auto()
        MACRO_RPP = auto()
        MACRO_BOX = auto()
        MACRO_RCC = auto()
    
    # constructor for building a surface card
    def __init__(self,card_string):
        Card.__init__(self,card_string)

    def __str__(self):
        string = "SurfaceCard: \n"
        string += "Surface ID " + str(self.surface_id)+"\n"
        string += "Transform ID " + str(self.surface_transform) + "\n"
        string += "Surface Type " + str(self.surface_type)+"\n"
        string += "Surface Coefficients " + str(self.surface_coefficients)+"\n"
        string += "Comment: " + str(self.comment)+"\n"
        return string
        
    def set_type(self, surf_id, surf_transform, surf_type, coords):
        self.surface_id = surf_id
        self.surface_transform = surf_transform
        self.surface_type = surf_type
        self.surface_coefficients = coords
        
    # test if the current surface is a macrobody or not
    def is_macrobody(self):
        if self.surface_type == self.SurfaceType['MACRO_RPP']:
            return True
        if self.surface_type == self.SurfaceType['MACRO_BOX']:
            return True
        if self.surface_type == self.SurfaceType['MACRO_RCC']:
            return True
        return False
