#!/usr/env/python3

from SurfaceCard import SurfaceCard
import xml.etree.ElementTree as ET

def openmc_surface_info(SurfaceCard):
    if SurfaceCard.surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]:
        type_string = "plane"        
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["PLANE_X"]:
        type_string = "x-plane"
        coeff_string = str(SurfaceCard.surface_coefficients[3])
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["PLANE_Y"]:
        type_string = "y-plane"
        coeff_string = str(SurfaceCard.surface_coefficients[3])
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["PLANE_Z"]:
        type_string = "z-plane"
        coeff_string = str(SurfaceCard.surface_coefficients[3])
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CYLINDER_X"]:
        type_string = "x-cylinder"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CYLINDER_Y"]:
        type_string = "y-cylinder"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CYLINDER_Z"]:
        type_string = "z-cylinder"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["SPHERE_GENERAL"]:
        type_string = "sphere"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["GENERAL_QUADRATIC"]:
        type_string = "quadric"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CONE_X"]:
        type_string = "x-cone"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CONE_Y"]:
        type_string = "y-cone"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CONE_Z"]:
        type_string = "z-cone"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    else:
        type_string = "error"
        coeff_string = "error"
    return (type_string, coeff_string)

# write the surface element corresponding to the
# geometry
def write_openmc_surface(SurfaceCard, geometry_tree):
    id = SurfaceCard.surface_id
    type, coeffs  = openmc_surface_info(SurfaceCard)
    ET.SubElement(geometry_tree, "surface", id = str(id), type = str(type),
                  coeffs = str(coeffs), boundary = "transmission")
    
    
class OpenMCSurfaceCard(SurfaceCard):
    """ Class to handle the creation and translation of
    OpenMC surface definitions 
    """
    # constructor
    def __init__(self, card_string):
        SurfaceCard.__init__(card_string)
        
        
