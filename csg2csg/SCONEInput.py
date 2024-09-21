# /usr/env/python3

from csg2csg.Input import InputDeck
from csg2csg.SCONESurfaceCard import write_scone_surface
from csg2csg.SCONECellCard import write_scone_cell
from csg2csg.SCONEMaterialCard import write_scone_material
from csg2csg.SCONEUniverseCard import write_scone_universe

import logging
import re


class SCONEInput(InputDeck):
    """SCONEInput class - does the actual processing"""

    # constructor
    def __init__(self, filename=""):
        InputDeck.__init__(self, filename)

    # open the geometry card
    def __write_scone_geometry_start(self, filestream):
        filestream.write("geometry { \n")
        # Surely there is a way to customise this? Am I missing a 
        # method somewhere?  For now I will leave as vacuum - should be easy 
        # for the user to change
        filestream.write("boundary (0 0 0 0 0 0); \n")
        filestream.write("graph {type shrunk;} \n")
        return

    # close the geometry card
    def __write_scone_geometry_end(self, filestream):
        filestream.write("} \n")
        return

    # open the nuclear data card
    def __write_scone_data_start(self, filestream):
        filestream.write("nuclearData { \n")
        filestream.write("handles { \n")
        filestream.write("ce {type aceNeutronDatabase; ")
        filestream.write("acelibrary $SCONE_ACE; ures 0;} \n")
        filestream.write("} \n")
        return

    # close the data card
    def __write_scone_data_end(self, filestream):
        filestream.write("} \n")
        return

    # write the SCONE surface definitions
    def __write_scone_surfaces(self, filestream):
        filestream.write("! --- surface definitions --- !\n")
        filestream.write("surfaces { \n")
        for surface in self.surface_list:
            write_scone_surface(filestream, surface)
        filestream.write("} \n")
        return
    
    # Write the SCONE Cell definitions
    def __write_scone_cells(self, filestream):
        filestream.write("! --- cell definitions --- !\n")
        filestream.write("cells { \n")
        for cell in self.cell_list:
            write_scone_cell(filestream, cell)
        filestream.write("} \n")
        return

    # Write the SCONE universe definitions
    # Most codes have universes implicit in their cells, complicating things 
    # slightly.
    def __write_scone_universes(self, filestream):
        filestream.write("! --- universe definitions --- !\n")
        filestream.write("universes { \n")
        for universe in self.universe_list:
            write_scone_universe(filestream, universe)
        filestream.write("} \n")
    
    # write the material compositions
    def __write_scone_materials(self, filestream):
        filestream.write("! --- material definitions --- !\n")
        filestream.write("materials { \n")
        for material in self.material_list:
            write_scone_material(filestream, self.material_list[material])
        filestream.write("} \n")
        return


    # main write scone method, depending upon where the geometry
    # came from
    def write_scone(self, filename, flat=True):
        f = open(filename, "w")
        self.__write_scone_geometry_start(f)
        self.__write_scone_surfaces(f)
        self.__write_scone_cells(f)
        self.create_universes_from_cells()
        self.__write_scone_universes(f)
        self.__write_scone_geometry_end(f)
        self.__write_scone_data_start(f)
        self.__write_scone_materials(f)
        self.__write_scone_data_end(f)
        f.close()
