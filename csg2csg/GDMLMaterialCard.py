#!/usr/env/python3

from csg2csg.Card import Card
from csg2csg.MaterialData import MaterialData
from csg2csg.MaterialCard import MaterialCard

from csg2csg.MaterialData import MaterialData

import xml.etree.ElementTree as ET

def density_multiplier_from_unit(unit):
    units = {}
    units["g/cm3"]  = 1.0
    units["g/mol"]  = 1.0
    units["g/mole"]  = 1.0
    units["kg/m3"] = units["g/cm3"]*1.0e3

    try:
        return units[unit]
    except KeyError:
        print ("the key, ",unit, " was not found")

    return units[unit]

class GDMLMaterialCard(MaterialCard):
    def __init__(self):
        MaterialCard.__init__(self)
        return

    """ given a description of the composite material
    instance a material in the generic form
    """
    def material_from_composite(self,name,density,density_unit,composite_tag):
        self.material_name = name
        self.density = float(density)*density_multiplier_from_unit(density_unit)
        
        # loop over the constituents - note the fractions
        # are always atom numbers
        for fraction in composite_tag:
            component = fraction.attrib["n"]
            nuclide = fraction.attrib["ref"]
            zaid = self.mat_data.name_zaid[nuclide.lower()]
            self.composition_dictionary[zaid] = float(component)
        self.normalise()
        self.explode_elements()

        return

    """ given a description of the fraction material
    instance a material in the generic form
    """
    def material_from_fraction(self,name,density,density_unit,fraction_tag):
        self.material_name = name
        self.density = float(density)*density_multiplier_from_unit(density_unit)

        # loop over the constituents - note the fractions
        # are always atom fractions
        for fraction in fraction_tag:
            component = fraction.attrib["n"]
            nuclide = fraction.attrib["ref"]
            zaid = self.mat_data.name_zaid[nuclide.lower()]
            self.composition_dictionary[zaid] = float(component)

        self.explode_elements()

        return

    """ given a description of the atom material
    instance a material in the generic form. The atom constructor
    can only contain one element and hence there are no loops
    """
    def material_from_atom(self,name,z,density,density_unit,atom_tag):
        self.material_name = name
        self.density = float(density)*density_multiplier_from_unit(density_unit)
        self.composition_dictionary[str(z*1000)] = 1.0 
        self.explode_elements()
        return