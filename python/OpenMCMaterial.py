#!/usr/env/python3

from MaterialCard import MaterialCard
import xml.etree.ElementTree as ET

# write the atomic fraction entry
def __write_atomic_fraction(material, nuclide, mass_frac):       
    ET.SubElement(material, "nuclide", name = nuclide, ao = str(abs(mass_frac)))
    return

# write a mass fraction entry
def __write_mass_fraction(material, nuclide, mass_frac):
    ET.SubElement(material, "nuclide", name = nuclide, wo = str(abs(mass_frac)))
    return

# generate the information required to write the
# material xml element
def write_openmc_material(MaterialCard, material_tree):
    matid = str(MaterialCard.material_number)
    name = "Material " + str(matid)
    density = str(abs(MaterialCard.density))
    if MaterialCard.density < 0:
        density_units = "g/cc"
    else:
        density_units = "atom/b-cm"
    
    material = ET.SubElement(material_tree, "material", id = matid)
    ET.SubElement(material, "density", value = density, units = density_units)

    for nuclide in MaterialCard.composition_dictionary:
        mass_frac = MaterialCard.composition_dictionary[nuclide]
        if mass_frac < 0:
            __write_mass_fraction(material, nuclide, mass_frac)
        else:
            __write_atomic_fraction(material, nuclide, mass_frac)

    

    
    
