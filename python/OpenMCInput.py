#/usr/env/python3

from Input import InputDeck

import logging
import sys
import xml.etree.ElementTree as ET

from XMLUtilities import indent
from OpenMCSurface import write_openmc_surface
from OpenMCCell import write_openmc_cell
from OpenMCMaterial import write_openmc_material


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
