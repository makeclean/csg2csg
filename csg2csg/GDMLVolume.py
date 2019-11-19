#/usr/env/python3

import math
import numpy as np

from csg2csg.GDMLSolid import GDMLSolid

import xml.etree.ElementTree as ET

""" This is quite a light class mostly to reduce
cognitive burden as it maps 1-1 with the GDML
specification - these GDML volumes are 
used a virtual placements before becoming 
concrete in physical volumes
"""
class GDMLVolume:
    def __init__(self,name,xml_element):
        self.material = None
        self.solid = None
        self.name = name

        self.from_xml(xml_element)
        return

    def from_xml(self,xml_element):
        for child in xml_element:
            if child.tag == "materialref":
                self.material = child.attrib["ref"]
            if child.tag == "solidref":
                self.solid = child.attrib["ref"]

        if not self.material:
           print("material not set")
        if not self.solid:
            print("sold not set")
        
        return