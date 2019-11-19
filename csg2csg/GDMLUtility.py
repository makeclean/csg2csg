#!/usr/bin/python3

import math
import numpy as np

""" takes a string which represents a valid gdml unit
and returns the appropriate multiplier to get it into cm

unit - a string containing a valid gdml unit
"""
def gdml_lunit_to_cm(unit):
    units = {}
    units["cm"] = 1.0
    units["mm"] = units["cm"]*0.1
    units["m"] = units["mm"]*1.e3
    units["km"] = units["m"]*1.e3
    units["nm"] = units["m"]*1.e-9
    units["um"] = units["m"]*1.e-6
    units["micrometer"] = units["um"]
    units["nanometer"] = units["nm"]
    units["kilometer"] = units["km"]
    units["centimeter"] = units["cm"]
    units["millimeter"] = units["mm"]
    units["angstrom"] = units["m"]*1e-10

    try:
        return units[unit]
    except KeyError:
        print ("the key, ",unit, " was not found")

    return units[unit]

""" takes a string which represents a valid gdml angle unit
and returns the appropriate multiplier to get it into radians

unit - a string containing a valid gdml angle unit
"""
def gdml_aunit_to_rotation(unit):
    units = {}
    units["radian"] = 1.0
    units["milliradian"] = units["radian"]*1.0e-3
    units["degree"] = units["radian"]*np.pi/180.0
    units["steradian"] = units["radian"]
    units["rad"] = units["radian"]
    units["mrad"] = units["milliradian"]
    units["sr"] = units["steradian"]
    units["deg"] = units["degree"]

    try:
        return units[unit]
    except KeyError:
        print ("the key, ",unit, " was not found")

    return units[unit]

""" access gdml region
"""
def access_gdml_region(parent,tag):
    tags = []
    for child in parent:
        if child.tag == tag:
            tags.append(child)

    return tags