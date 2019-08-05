#/usr/env/python3

from csg2csg.Input import InputDeck
from csg2csg.MCNPSurfaceCard import MCNPSurfaceCard, write_mcnp_surface
from csg2csg.MCNPCellCard import MCNPCellCard, write_mcnp_cell
from csg2csg.MCNPMaterialCard import MCNPMaterialCard, write_mcnp_material

class PhitsInput(InputDeck):
    """ PhitsInput class - does the actual processing
    """

    # constructor
    def __init__(self,filename = ""):
        InputDeck.__init__(self,filename)

    # write the header information
    def __write_header_information(self,filestream):
        string = "[ T I T L E ]\n"
        string += "This PHITS file was produced automatically by csg2csg \n"
        string += "\n"
        string += "[ P A R A M E T E R S ]\n"
        string += "icntl = 11\n"
        string += "maxbch = 10\n"
        string += "maxcas = 1000000\n"
        filestream.write(string)
        return

    # Write the Phits Cell definitions
    def __write_phits_cells(self, filestream):
        filestream.write("[ C E L L ]\n")
        for cell in self.cell_list:
            write_mcnp_cell(filestream,cell,False)
        return
    
    # write the serpent surface definitions 
    def __write_phits_surfaces(self, filestream):
        filestream.write("[ S U R F A C E ]\n")
        for surface in self.surface_list:
            write_mcnp_surface(filestream,surface)
        return

    # write the material compositions
    def __write_phits_importances(self, filestream):
        filestream.write("[ I M P O R T A N C E ]\n")
        filestream.write("   reg       imp   \n")
        for cell in self.cell_list:
            filestream.write("    " + str(cell.cell_id) + 
                             "        " + str(cell.cell_importance) + "\n")
        return

    # write the material compositions
    def __write_phits_materials(self, filestream):
        filestream.write("[ M A T E R I A L ]\n")
        for material in self.material_list:
            write_mcnp_material(filestream, self.material_list[material],True)
        return
    
    # main write serpent method, depending upon where the geometry
    # came from 
    def write_phits(self, filename, flat = True):
        f = open(filename,"w")
        self.__write_header_information(f)
        f.write("\n")   
        self.__write_phits_surfaces(f)
        f.write("\n")
        self.__write_phits_cells(f)
        f.write("\n")
        self.__write_phits_importances(f)
        f.write("\n")
        self.__write_phits_materials(f)
        f.write("\n")
        f.close()
