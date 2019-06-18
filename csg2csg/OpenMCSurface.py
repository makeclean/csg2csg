#!/usr/env/python3

from csg2csg.SurfaceCard import SurfaceCard
import xml.etree.ElementTree as ET

import warnings

def boundarystring_to_type(boundary_string):
    if boundary_string == "transmission":
        boundary_type = SurfaceCard.BoundaryCondition["TRANSMISSION"]
    if boundary_string == "vacuum":
        boundary_type = SurfaceCard.BoundaryCondition["VACUUM"]
    if boundary_string == "reflecting":
        boundary_type = SurfaceCard.BoundaryCondition["REFLECTING"]
    return boundary_type

def boundary_condition(boundaryCondition):
    if boundaryCondition == SurfaceCard.BoundaryCondition["TRANSMISSION"]:
        boundary = "transmission"
    if boundaryCondition == SurfaceCard.BoundaryCondition["VACUUM"]:
        boundary = "vacuum"
    if boundaryCondition == SurfaceCard.BoundaryCondition["REFLECTING"]:
        boundary = "reflecting"
    if boundaryCondition == SurfaceCard.BoundaryCondition["WHITE"]:
        boundary = "vacuum"
        warnings.warn('Found an unsupported boundary condition for OpenMC, White boundary considered vacuum',Warning)

    return boundary

def type_to_generictype(surface_string):
    if surface_string == "sphere":
        surface = SurfaceCard.SurfaceType["SPHERE_GENERAL"]
    if surface_string == "x-plane":
        surface = SurfaceCard.SurfaceType["PLANE_X"]
    if surface_string == "y-plane":
        surface = SurfaceCard.SurfaceType["PLANE_Y"]
    if surface_string == "z-plane":
        surface = SurfaceCard.SurfaceType["PLANE_Z"]
    if surface_string == "plane":
        surface = SurfaceCard.SurfaceType["PLANE_GENERAL"]
    if surface_string == "x-cylinder":
        surface = SurfaceCard.SurfaceType["CYLINDER_X"]
    if surface_string == "y-cylinder":
        surface = SurfaceCard.SurfaceType["CYLINDER_Y"]
    if surface_string == "z-cylinder":
        surface = SurfaceCard.SurfaceType["CYLINDER_Z"]
    if surface_string == "x-cone":
        surface = SurfaceCard.SurfaceType["CONE_X"]
    if surface_string == "y-cone":
        surface = SurfaceCard.SurfaceType["CONE_Y"]
    if surface_string == "z-cone":
        surface = SurfaceCard.SurfaceType["CONE_Z"]
    if surface_string == "quadric":
        surface = SurfaceCard.SurfaceType["GENERAL_QUADRATIC"]

    return surface

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
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["TORUS_X"]:
        type_string = "x-torus"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["TORUS_Y"]:
        type_string = "y-torus"
        coeff_string = ' '.join(str(e) for e in SurfaceCard.surface_coefficients)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["TORUS_Z"]:
        type_string = "z-torus"
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
                  coeffs = str(coeffs), 
                  boundary = boundary_condition(SurfaceCard.boundary_condition))

# import openmc surface functions
def surface_from_attribute(xml_attribute):
    surface = SurfaceCard("")
    # loop over the surface attributes and build the generic description
    surface.boundary_condition = boundarystring_to_type(xml_attribute['boundary']) 
    surface.surface_coefficients = xml_attribute['coeffs'].split() 
    surface.surface_id = xml_attribute['id'] 
    surface.surface_type = type_to_generictype(xml_attribute['type'])
    return surface
    
class OpenMCSurfaceCard(SurfaceCard):
    """ Class to handle the creation and translation of
    OpenMC surface definitions 
    """
    # constructor
    def __init__(self, card_string):
        SurfaceCard.__init__(card_string)
        
        
