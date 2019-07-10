#/usr/env/python3

from csg2csg.Input import InputDeck

import logging
import sys
import xml.etree.ElementTree as ET

from csg2csg.OpenMCSurface import SurfaceCard,surface_from_attribute, write_openmc_surface
from csg2csg.OpenMCCell import cell_from_attribute, write_openmc_cell
from csg2csg.OpenMCMaterial import material_from_attribute, write_openmc_material
from csg2csg.OpenMCLattice import lattice_from_attribute, write_openmc_lattice

'''
copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
it basically walks your tree and adds spaces and newlines so the tree is
printed in a nice way
'''
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class OpenMCInput(InputDeck):
    """ OpenMCInputDeck intrastructure to write and OpenMC input deck
    by not invoking the python binding for OpenMC, but writing the 
    xml elements directly
    """
    # constructor
    def __init__(self,geometry_file="geometry.xml",material_file="materials.xml"):
        self.geometry = geometry_file
        self.material = material_file
        self.xml_geom = None
        self.xml_material = None
        # make a new input deck
        InputDeck.__init__(self,filename="")

    # read the openmc files
    def read(self):
        self.xml_geom = self.__read_geometry_xml(self.geometry)
        self.xml_material = self.__read_material_xml(self.material)

    # read the geometry file
    def __read_geometry_xml(self, geometry_filename):
        geom = ET.parse(geometry_filename)
        geom_root = geom.getroot()
        return geom_root

    # read the material file
    def __read_material_xml(self, material_filename):
        mat = ET.parse(material_filename)
        mat_root = mat.getroot()
        return mat_root

    # process the files
    def process(self):
        # do materials first 
        self.__process_materials()
        self.__process_geometry()
        

    # process the geometry
    def __process_geometry(self):

        for child in self.xml_geom:
            if child.tag == "surface":
                surface = surface_from_attribute(child.attrib)
                InputDeck.surface_list.append(surface)
            elif child.tag == "cell":
                cell = cell_from_attribute(child.attrib)
                InputDeck.cell_list.append(cell)
            elif child.tag == "lattice":
                lattice = lattice_from_attribute('lattice', child.attrib, child.getchildren())
                InputDeck.lattice_list.append(lattice)
            elif child.tag == "hex_lattice":
                lattice = lattice_from_attribute('hex_latice', child.attrib, child.getchildren())
                InputDeck.lattice_list.append(lattice)


        # loop over the cells and set the material 
        # density for each cell
        for cell in InputDeck.cell_list:
            cell_mat = cell.cell_material_number
            if cell_mat is not 0:
                density = InputDeck.material_list[cell_mat].density
                cell.cell_density = density

        # identify the cells that have a surface with a vacuum
        # boundary condition, they mark the end of the universe
        boundary_surfs = []
        for surface in InputDeck.surface_list:
            if surface.boundary_condition == SurfaceCard.BoundaryCondition["VACUUM"]:
                boundary_surfs.append(surface.surface_id)

        # now loop through the cells and mark as importance 0 where
        # appropriate
        for cell in InputDeck.cell_list:
            if set(boundary_surfs) & set(cell.cell_interpreted) == set(boundary_surfs):
                cell.cell_importance = 0

    # process the materials
    def __process_materials(self):
        for child in self.xml_material:
            if child.tag == "material":
                material = material_from_attribute(child.attrib, child.getchildren())
                InputDeck.material_list[material.material_number] = material

    # write the collection of OpenMC surface definitions
    def __write_openmc_surfaces(self, geometry_tree):
        for surface in self.surface_list:
            write_openmc_surface(surface, geometry_tree)

    # write the collection of OpenMC cell definitions
    def __write_openmc_cells(self, geometry_tree):
        for cell in self.cell_list:
            write_openmc_cell(cell, geometry_tree)

    # write the collection of OpenMC lattice definitions
    def __write_openmc_lattices(self, geometry_tree):
        for lattice in self.lattice_list:
            write_openmc_lattice(lattice, geometry_tree)


    # write the collection of Material
    def __write_openmc_materials(self, material_tree):
        for mat in self.material_list:
            write_openmc_material(self.material_list[mat], material_tree)

    def __get_unused_fills(self,geometry_tree):
        universes = set()
        fill_universes = set()

        for cell_elem in geometry_tree.findall('cell'):
            u = int(cell_elem.get('universe'))
            universes.add(u)

            if 'fill' in cell_elem.keys():
                fill = int(cell_elem.get('fill'))
                fill_universes.add(fill)

        for lattice_elem in geometry_tree.findall('lattice'):
            u = int(lattice_elem.get('id'))
            universes.add(u)
            for u in lattice_elem.find('universes').text.split():
                fill_universes.add(int(u))

        not_used_universerses = universes - fill_universes
        
        return not_used_universerses

    # check to see if any universes are unsed
    def __check_unused_universes(self, geometry_tree):
        # loop over the unsed fills 
        while len(self.__get_unused_fills(geometry_tree)) > 1:
            cells_to_remove = set()
            # loop over the universes not used as a fill
            for universe in self.__get_unused_fills(geometry_tree):
                if universe != 0:  
                    for cell_elem in geometry_tree.findall('cell'):
                        u = int(cell_elem.get('universe'))
                        if u == universe:
                            cells_to_remove.add(cell_elem)

            # loop over the cells that have not fill
            for cell in cells_to_remove:
                geometry_tree.remove(cell)

        return

    # write the openmc geometry
    def write_openmc(self, filename, flat = True):
        geometry = ET.Element("geometry")

        self.__write_openmc_surfaces(geometry)
        self.__write_openmc_cells(geometry)
        self.__write_openmc_lattices(geometry)
        self.__check_unused_universes(geometry)

        tree = ET.ElementTree(geometry)
        indent(geometry)
        tree.write(filename+"/geometry.xml")

        # write the materials
        material_tree = ET.Element("materials")
        tree = ET.ElementTree(material_tree)
        self.__write_openmc_materials(material_tree)
        indent(material_tree)
        tree.write(filename+'/materials.xml')
