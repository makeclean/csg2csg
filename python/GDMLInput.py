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
        material = ET.SubElement(material_tree, "material", name = str(Material.material_name),
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
            # it appears that gdml allows only atom fractions for a material description
            if fraction < 0.:
                ET.SubElement(material, "fraction", n = abs_fraction, ref = nuclide_name)            
            else:
                ET.SubElement(material, "fraction", n = abs_fraction, ref = nuclide_name)            
        
    # write the solid parts of the geometry
    def __write_gdml_solids(self, gdml):
        # make 
        # planes will be defined as boxes with offsets to ensure correct placement.
        # spheres are spheres -> transform needed to shift it to correct placement
        # cylinders are cylinders -> transfomred as needed
        # cones when they are supported will be cones -> transform as needed
        # tori will be tori
        # the real question is what to do with GQ -> try turning into basic conic
        # section - ala - cad2mcnp

        return

    def __write_gdml_operations(self,gdml):
        # this writes the boolean operations as required by 
        # the gdml format - some of the mcnp ones are petty
        # lengthy - need to see how they will be expanded
        
        return
    
    def __write_gdml_structures(self,gdml):
        # this declares solids that are made
        # from the boolean operations previously declared

    # write the gdml geometry part
    def __write_gdml_geometry(self,gdml):
        solids = ET.SubElement(gdml,"solids")
        self.__write_gdml_solids(solids)
        self.__write_gdml_operations(solids)
        self.__write_gdml_structures(solids)
        return

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
            # write the geometry
            self.__write_gdml_geometry(gdml)

            gdml_tree = ET.ElementTree(gdml)
            indent(gdml)
            # write the gdml file
            gdml_tree.write(filename + '.gdml')
        
