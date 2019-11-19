#/usr/env/python3

import math
import numpy as np

from copy import deepcopy

import xml.etree.ElementTree as ET

""" GDML Physvol
"""
class GDMLPhysvol:
    def __init__(self,name,xml_element):
        self.name = name
        self.volume = None
        self.position = None
        self.rotation = None
        self.from_xml(xml_element)
        return

    def __str__(self):
        string = "name: " + self.name + "\n"
        string += "volume: " + str(self.volume or "") + "\n"
        string += "position: " + str(self.position or "") + "\n"
        string += "rotation: " + str(self.rotation or "")
        return string

    def from_xml(self,xml_element):
        for child in xml_element:
            if child.tag == "volumeref":
                self.volume = child.attrib["ref"]
            if child.tag == "positionref":
                self.position = child.attrib["ref"]
            if child.tag == "rotationref":
                self.rotation = child.attrib["ref"]
        if not self.volume: 
            print ("volume not set")
        if not self.position:
            print ("position not set")   
        return

""" GDML Assembly
"""
class GDMLAssembly:
    def __init__(self,name,xml_element):
        self.name = name
        self.physvols = {}
        self.from_xml(xml_element)
        return

    def from_xml(self,xml_element):
        # for every physvol in the list
        for child in xml_element:
            physvol = GDMLPhysvol(child.attrib["name"],child)
            self.physvols[physvol.name] = physvol
        return

    """ create new objects in the flat hierarchy for use in the
    other monte carlo codes, creating deep copies of volumes that
    exist place them in the real flat world
    """
    def incarnate(self,volumes,solids,positions,rotations):
        # for each physical volume
        positioned_entities = []
        for idx,item in enumerate(self.physvols.keys()):
            # get the physvol
            physvol = self.physvols[item]
            # get the volume
            volume = volumes[physvol.volume]
            print(volume)
            print('physvol: '+ physvol.volume)
            print('volumes: ', volumes.keys())
            print('solids: ', solids.keys())
            solid = deepcopy(solids[volume.solid])
            solid.position(positions[physvol.position])
            # there may be no rotation
            if physvol.rotation:
                solid.rotation(rotations[physvol.rotation])
            # set the cell id
            solid.cell.cell_id = idx
            solid.cell.cell_interpreted = solid.inside
            cell = solid.cell
            positioned_entities.append(cell)
        return positioned_entities
            