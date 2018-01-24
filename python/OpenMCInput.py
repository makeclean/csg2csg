#/usr/env/python3

from Input import InputDeck

import logging
import sys
import xml.etree.ElementTree as ET

from OpenMCSurface import write_openmc_surface
from OpenMCCell import write_openmc_cell
from OpenMCMaterial import write_openmc_material
'''
copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
it basically walks your tree and adds spaces and newlines so the tree is
printed in a nice way
'''
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class OpenMCInput(InputDeck):
    """ OpenMCInputDeck intrastructure to write and OpenMC input deck
    by not invoking the python binding for OpenMC, but writing the 
    xml elements directly
    """
    # constructor
    def __init__(self, filename = ""):
        InputDeck.__init__(self, filename)

    # write the collection of OpenMC surface definitions
    def __write_openmc_surfaces(self, geometry_tree):
        for surface in self.surface_list:
            write_openmc_surface(surface, geometry_tree)

    # write the collection of OpenMC cell definitions
    def __write_openmc_cells(self, geometry_tree):
        for cell in self.cell_list:
            write_openmc_cell(cell, geometry_tree)
            
    # write the collection of Material
    def __write_openmc_materials(self, material_tree):
        for mat in self.material_list:
            write_openmc_material(self.material_list[mat], material_tree)

    # write the openmc geometry
    def write_openmc(self, filename, flat = True):
        geometry = ET.Element("geometry")

        self.__write_openmc_surfaces(geometry)
        self.__write_openmc_cells(geometry)
        
        tree = ET.ElementTree(geometry)
        indent(geometry)
        tree.write(filename+"/geometry.xml")

        # write the materials
        material_tree = ET.Element("materials")
        tree = ET.ElementTree(material_tree)
        self.__write_openmc_materials(material_tree)
        indent(material_tree)
        tree.write(filename+'/materials.xml')
