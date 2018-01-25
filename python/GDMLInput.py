#!/usr/env/python3

from Input import InputDeck

from XMLUtilities import indent

import logging
import sys
import xml.etree.ElementTree as ET

""" Class to handle writing the csg2csg abstracted geometry type to
GDML format
"""
class GDMLInput(InputDeck):
    def __init__(self):
        pass

    # write a single gdml material element
    def __write_gdml_material(self,material_tree,Material):
        # make the material element
        material = ET.SubElement(material_tree, "material", name = "M"+str(Material.material_name),
                                 formula = "M"+str(Material.material_name))

        # determine the material composition
        density = str(abs(Material.density))
        if Material.density < 0.:
            ET.SubElement(material, "D", value = density, unit = "g/cc")
        else:
            ET.SubElement(material, "D", value = density, unit = "atoms/cc")

        # loop over the dictionary and make the material
        for nucid in Material.composition_dictionary.keys():
            fraction = Material.composition_dictionary[nucid]
            abs_fraction = str(abs(fraction))
            # we can use a fancer naming scheme than this really 
            nuclide_name = str(nucid)
            if fraction < 0.:
                ET.SubElement(material, "fraction", n = abs_fraction, ref = nuclide_name)            
            else:
                ET.SubElement(material, "fraction", n = abs_fraction, ref = nuclide_name)            
        
    # write the gdml material elements
    def __write_gdml_materials(self,gdml):
        # make the gdml material section
        materials = ET.SubElement(gdml,"materials")
        # need to make isotope list
        # need to make element list
        # need to make material list
        for mat in self.material_list.keys():
            self.__write_gdml_material(materials,self.material_list[mat])
    
        return

    # write a complete gdml file
    def write_gdml(self, filename, Unified = True, flat = True):
        if Unified:
            # make the gdml element
            gdml = ET.Element('gdml')
            # write the materials
            self.__write_gdml_materials(gdml)
            gdml_tree = ET.ElementTree(gdml)
            indent(gdml)
            # write the gdml file
            gdml_tree.write(filename + '.gdml')
        
