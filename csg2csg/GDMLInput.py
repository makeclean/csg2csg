#/usr/env/python3

from csg2csg.Input import InputDeck

from csg2csg.GDMLUtility import gdml_lunit_to_cm,gdml_aunit_to_rotation,access_gdml_region
from csg2csg.GDMLMaterialCard import GDMLMaterialCard
from csg2csg.GDMLSolid import GDMLSolid,GDMLBox
from csg2csg.GDMLVolume import GDMLVolume
from csg2csg.GDMLAssembly import GDMLAssembly

import numpy as np

import logging
import sys
import xml.etree.ElementTree as ET

from copy import deepcopy

class GDMLInput(InputDeck):
    """ GDMLInputDeck intrastructure to (eventually) write a GDML input deck
    but right now will only do input from GDML
    """
    # constructor
    def __init__(self, filename = ""):
        InputDeck.__init__(self, filename)
        self.tree = None
        self.root = None

        self.positions = {}
        self.rotations = {}
        self.solids = {}
        self.volumes = {}
        self.assemblies = {}

    # read the xml file
    def read(self):
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()
        return


    """ Process the define statement to give the
    results stored in a dictionary on the class
    """
    def __process_defines(self):
        
        define_tag = access_gdml_region(self.root,"define")
       
        # get and process the position information
        position_tag = access_gdml_region(define_tag[0],"position")
        # loop over the position tags
        for position in position_tag:
            name = position.attrib["name"]
            x = float(position.attrib["x"])
            y = float(position.attrib["y"])
            z = float(position.attrib["z"])
            unit = position.attrib["unit"]

            # convert to cm
            multi = gdml_lunit_to_cm(unit)

            # multiply appropriately
            x *= multi
            y *= multi
            z *= multi

            self.positions[name] = {"x":x,"y":y,"z":z}

        # get and process the rotation information
        position_tag = access_gdml_region(define_tag[0],"rotation")
        # loop over the position tags
        for position in position_tag:
            name = position.attrib["name"]
            x = float(position.attrib["x"])
            y = float(position.attrib["y"])
            z = float(position.attrib["z"])
            unit = position.attrib["unit"]

            # convert to cm
            multi = gdml_aunit_to_rotation(unit)

            # multiply appropriately
            x *= multi
            y *= multi
            z *= multi

            self.rotations[name] = {"x":x,"y":y,"z":z}

        return

    """ Process the define statement to give the
    results stored in a dictionary on the class
    """
    def __process_materials(self):
        # access the material tag
        materials_tag = access_gdml_region(self.root,"materials")

        # extract the element data
        element_tag = access_gdml_region(materials_tag[0],"element")

        # extract the material data
        material_tag = access_gdml_region(materials_tag[0],"material")

        # loop over the material objects
        for idx,material in enumerate(material_tag):
            name = material.attrib["name"]

            # z tag is optional
            if not material.attrib.get("Z"):
                z = 0
            else:
                z = int(material.attrib["Z"])
            
            # you must have density tag
            density_tag = access_gdml_region(material,"D")
            density = density_tag[0].attrib["value"]
            # density unit is optional
            if not density_tag[0].attrib.get("unit"):
                density_unit = "g/cc"
            else:
                density_unit = density_tag[0].attrib["unit"] # there may be no unit
                                                      # in which case g/cc is default

            # a material may have atom, composite, or fraction entries
            materialObject = GDMLMaterialCard()

            if access_gdml_region(material,"composite"):
                composite_tag = access_gdml_region(material,"composite") 
                materialObject.material_from_composite(name,density,
                                                 density_unit,composite_tag)
            elif access_gdml_region(material,"fraction"):  
                fraction_tag = access_gdml_region(material,"fraction")
                materialObject.material_from_fraction(name,density,
                                                 density_unit,fraction_tag)
            elif access_gdml_region(material,"atom"):
                atom_tag = access_gdml_region(material,"atom")
                materialObject.material_from_atom(name,z,density,
                                            density_unit,atom_tag)
            else:
                raise ValueError("Material has no fraction, composite or atom region")
            
            materialObject.material_number = idx + 1
            self.material_list[idx+1] = materialObject
            

        return

    """ process the solids into a form that can be used
    downstream 
    """
    def __process_solids(self):
        # access the solids tag
        solids = access_gdml_region(self.root,"solids")
        for child in solids[0]:
            if child.tag == "box":
                solid = GDMLBox(child)
            solid.explode()
            name = child.attrib["name"]
            self.solids[name] = solid
        return

    """ process the structures into a form that can be used
    downstream - the structures define the actual placements of
    solids into the world - i.e. with a position and rotation
    """
    def __process_structures(self):
        # access the solids tag
        structures = access_gdml_region(self.root,"structure")
        for child in structures[0]:
            name = child.attrib["name"]
            if child.tag == "volume":
                volume = GDMLVolume(name,child)
                self.volumes[volume.name] = volume
            if child.tag == "assembly":
                assembly = GDMLAssembly(name,child)
                self.assemblies[name] = assembly

        return
    
    """ process the setup element to setup the remainder of the gdml
    structure
    """
    def __process_setup(self):
        # access the solids tag
        setup = access_gdml_region(self.root,"setup")
        name = setup[0].attrib["name"]
        world = access_gdml_region(setup[0],"world")
        ref = world[0].attrib["ref"]

    def __incarnate(self):
        for assembly in self.assemblies.keys():
            # create actual cell definitions 
            cells = self.assemblies[assembly].incarnate(self.volumes,self.solids,
                                    self.positions,self.rotations)
            self.cell_list.extend(cells)
        print(self.cell_list)
        return

    # process the gdml input
    def process(self):
        # instanciate all the gdml 
        # structures as expected
        self.__process_defines()
        self.__process_materials()
        self.__process_solids()
        self.__process_structures()
        self.__process_setup()
        # instanciate all the volumes as expected
        # by our flat hierarchies
        self.__incarnate()

        return