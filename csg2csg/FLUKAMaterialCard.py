#!/usr/env/python3

from csg2csg.MaterialCard import MaterialCard


""" A function which writes the fluka material card for an element
zz is the zaid of the element and name is the fluka name

Input: filestream - an openfilestream to write to
       zz - the zaid of the the element
       name - the fluka name of the element
"""
def write_fluka_material_element(filestream,zz,name,density="1.0"):
    string = '{:<10}'.format("MATERIAL")
    atomic_number = '{:>10}'.format(float(int(int(zz)/1000)))
    atomic_mass = '{:>10}'.format("")
    density = '{:>10}'.format(density)
    number = '{:>10}'.format("")
    alternate = '{:>10}'.format("")
    mass_num = '{:>10}'.format("")
    name = '{:>10}'.format(name)
    string += atomic_number
    string += atomic_mass
    string += density
    string += number
    string += alternate
    string += mass_num
    string += name
    string += "\n"
    filestream.write(string)     
    return

def write_fluka_material(filestream, material):
    string = '{:<10}'.format("MATERIAL")
    atomic_number = '{:>10}'.format("")
    atomic_mass = '{:>10}'.format("")
    density = '{:>10}'.format(abs(material.density))
    number = '{:>10}'.format("")
    alternate = '{:>10}'.format("")
    mass_num = '{:>10}'.format("")
    name = '{:>10}'.format("M"+str(material.material_number))
    string += atomic_number
    string += atomic_mass
    string += density
    string += number
    string += alternate
    string += mass_num
    string += name
    string += "\n"
    filestream.write(string)
    return

def write_fluka_compound(filestream,material):
    comp_dict = material.composition_dictionary
    card_string = '{:<10}'.format("COMPOUND")    
    mat_name = '{:>10}'.format("M" + material.material_number)

    comp_string = ""
    for mat,frac in comp_dict.items():
        fraction = '{:> 9.3e}'.format(float(frac))
        elemname = '{:>10}'.format(mat)
        comp_string += fraction
        comp_string += elemname


    # work backwards popping off 3 until there none left
    while len(comp_string) > 0:
        part = ""
        if len(comp_string) / 20 >= 3:
            part = comp_string[-60:]
            comp_string = comp_string[:-60]
        elif int(len(comp_string) / 20) == 2:
            part = comp_string[-40:]
            part += '{:>20}'.format("")
            comp_string = comp_string[:-40]
        elif int(len(comp_string) / 20) == 1:
            part = comp_string[-20:]
            part += '{:>40}'.format("")            
            comp_string = comp_string[:-20]
            
        string  = card_string
        string += part
        string += mat_name
        string += "\n"
        filestream.write(string)
    return
                         
""" Class to handle FLUKAMaterialCard tranlation
"""
class FLUKAMaterialCard(MaterialCard):
    def __init__(self, card_string):
        MaterialCard.__init__(self, card_string)
