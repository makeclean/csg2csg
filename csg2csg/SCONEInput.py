# /usr/env/python3

from csg2csg.Input import InputDeck
from csg2csg.SCONESurfaceCard import SCONESurfaceCard, write_scone_surface
from csg2csg.SCONECellCard import SCONECellCard, write_scone_cell
from csg2csg.SCONEMaterialCard import SCONEMaterialCard, write_scone_material

import logging
import re


class SCONEInput(InputDeck):
    """SCONEInput class - does the actual processing"""

    # constructor
    def __init__(self, filename=""):
        InputDeck.__init__(self, filename)

    # write the SCONE surface definitions
    def __write_scone_surfaces(self, filestream):
        filestream.write("% --- surface definitions --- %\n")
        # Open the SCONE geometry card
        filestream.write("geometry { \n")
        # Surely there is a way to customise this?
        filestream.write("boundary (0 0 0 0 0 0); \n")
        filestream.write("graph {type shrunk;} \n")
        filestream.write("surfaces { \n")
        for surface in self.surface_list:
            write_scone_surface(filestream, surface)
        filestream.write("} \n")
        return
    
    # Write the SCONE Cell definitions
    def __write_scone_cells(self, filestream):
        filestream.write("% --- cell definitions --- %\n")
        filestream.write("cells { \n")
        for cell in self.cell_list:
            write_scone_cell(filestream, cell)
        filestream.write("} \n")
        # Close the SCONE geometry card
        # Need to do something about universes!
        # E.g., add in a rootUniverse and a single cellUniverse containing all cells
        # Most codes have universes implicit in their cells, complicating things slightly.
        filestream.write("} \n")
        return

    # write the material compositions
    def __write_scone_materials(self, filestream):
        filestream.write("% --- material definitions --- %\n")
        # Open the SCONE nuclearData card
        filestream.write("nuclearData { \n")
        filestream.write("handles { \n")
        filestream.write("ce {type aceNeutronDatabase; acelibrary $SCONE_ACE; ures 0;} \n")
        filestream.write("} \n")
        filestream.write("materials { \n")
        for material in self.material_list:
            write_scone_material(filestream, self.material_list[material])
        filestream.write("} \n")
        filestream.write("} \n")
        return

    # main write scone method, depending upon where the geometry
    # came from
    def write_scone(self, filename, flat=True):
        f = open(filename, "w")
        self.__write_scone_surfaces(f)
        self.__write_scone_cells(f)
        self.__write_scone_materials(f)
        f.close()
