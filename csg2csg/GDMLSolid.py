#/usr/env/python3

import math
import numpy as np

from csg2csg.GDMLUtility import gdml_lunit_to_cm

from csg2csg.CellCard import CellCard
from csg2csg.SurfaceCard import SurfaceCard

import xml.etree.ElementTree as ET

def plane_builder(id,type,coefficients):
    surf = SurfaceCard("")    
    surf.id = id
    surf.surface_type = SurfaceCard.SurfaceType[type]
    surf.surface_coefficients = coefficients
    return surf

class GDMLSolid():
    def __init__(self,xml_element):
        self.surface_list = []
        self.cell = CellCard("")
        self.name = ""
        return 

    def get_cell(self):
        return self.cell

    def get_surfaces(self):
        return self.surface_list

    """ apply translation to the surfaces in the cells
    """
    def position(self, coordinates):
        if not self.surface_list:
            print("There are no surfaces belonging to this volume")

        trans = [coordinates["x"],coordinates["y"],coordinates["z"]]
        for surf in self.surface_list: 
            surf.translation(trans)
   
        return

    """ apply rotation to the surfaces in the cells
    """
    def rotation(self, rotation):
        return
        if not self.surface_list:
            print("There are no surfaces belonging to this volume")

        # tait-bryan angles in cosines
        angles = [rotation.x,rotation.y,rotation.z]
        #rotation_matrix = rotation_matrix_from_euler(angles)

        # rotate each surface appropriately 
        for surf in self.surface_list: 
            surf.transform(rotation_matrix)
   
        return

# there will be a solid class for each solid type with a similarly
# named method Cone,Ellipsoid,EllipticalTube,Orb,Paraboloid,Pallalepiped
# PolyCone,PolyHedra,Sphere,Torus,Trapezoid,GeneralTrapezoid,
# there are some solids which will not be supported - TesselatedSolid
# and the Twisted Classses
class GDMLBox(GDMLSolid):
    def __init__(self,xml_element):
        GDMLSolid.__init__(self,"")
        self.unit = gdml_lunit_to_cm(xml_element.attrib["lunit"])
        self.x = float(xml_element.attrib["x"])*self.unit
        self.y = float(xml_element.attrib["y"])*self.unit
        self.z = float(xml_element.attrib["z"])*self.unit
        self.name = xml_element.attrib["name"]
        self.inside_description = []
        self.outside_description = []
        return

    def __str__(self):
        string  = "type: box\n"
        string += "name: " + self.name 
        return str

    """ Explode the GDML macrobody like description into 
    generalised surface descriptions - note the surfaces 
    are numbered arbitrarily 1 to N and will need to be
    consistently numbered later. The surfaces will have
    -ve sense wrt to the solid just like an MCNP macro
    body
    """
    def explode(self):
        # make 6 surfaces with -ve sense wrt to the point 0,0,0
        # define both the inside of the shape and the outside
        surf = plane_builder(1,"PLANE_GENERAL",[1,0,0,self.x])
        self.surface_list.append(surf)
        surf = plane_builder(2,"PLANE_GENERAL",[-1,0,0,-self.x])
        self.surface_list.append(surf)
        surf = plane_builder(3,"PLANE_GENERAL",[0,1,0,self.y])
        self.surface_list.append(surf)
        surf = plane_builder(4,"PLANE_GENERAL",[0,-1,0,-self.y])
        self.surface_list.append(surf)
        surf = plane_builder(5,"PLANE_GENERAL",[0,0,1,self.z])
        self.surface_list.append(surf)
        surf = plane_builder(6,"PLANE_GENERAL",[0,0,-1,-self.z])
        self.surface_list.append(surf)

        self.inside = ['(',self.surface_list[0].surface_id,CellCard.OperationType["AND"], \
        self.surface_list[1].surface_id,CellCard.OperationType["AND"],\
        self.surface_list[2].surface_id,CellCard.OperationType["AND"],\
        self.surface_list[3].surface_id,CellCard.OperationType["AND"],\
        self.surface_list[4].surface_id,CellCard.OperationType["AND"],\
        self.surface_list[5].surface_id,CellCard.OperationType["AND"],')']

        self.cell.cell_interpreted = self.inside

        return
