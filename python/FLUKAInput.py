#/usr/env/python3

from Input import InputDeck
from FlukaSurfaceCard import FlukaSurfaceCard, write_fluka_surface
from FlukaCellCard import FlukaCellCard, write_fluka_cell
from FlukaMaterialCard import FlukaMaterialCard, write_fluka_material

class FLUKAInput(InputDeck):
    """ FlukaInput class - does the actual processing
    """

    # constructor
    def __init__(self,filename = ""):
        InputDeck.__init__(self,filename)

    # write the fluka input deck ruler
    def __write_ruler(self, filestream):
        filestream.write("*...+....1....+....2....+....3....+....4
                          ....+....5....+....6....+....7....+....8\n")

        
    # Write the Serpent Cell definitions
    def __write_fluka_cells(self, filestream):
        filestream.write("* --- cell definitions --- *\n")
        filestream.write("GEOBEGIN\n")
        for cell in self.cell_list:
            write_fluka_cell(filestream,cell)
        filestream.write("END\n")
        return
    
    # write the serpent surface definitions 
    def __write_fluka_surfaces(self, filestream):
        filestream.write("* --- cell definitions --- *\n")
        for surface in self.surface_list:
            write_fluka_surface(filestream,surface)
        filestream.write("END\n")
        filestream.write("GEOEND\n")
        return

    # write the material compositions
    def __write_fluka_materials(self, filestream):
        filestream.write("* --- material definitions --- *\n")
        for material in self.material_list:
            write_fluka_material(filestream, self.material_list[material])
        return
    
    # main write serpent method, depending upon where the geometry
    # came from 
    def write_fluka(self, filename, flat = True):
        f = open(filename,'w')
        self.__write_ruler(f)
        f.write("TITLE\n input deck automatically created by csg2csg")
        self.__write_ruler(f)
        self.__write_fluka_surfaces(f)
        self.__write_ruler(f)
        self.__write_fluka_cells(f)
        self.__write_ruler(f)
        self.__write_fluka_materials(f)
        self.__write_ruler(f)
        f.write("STOP\n")
        f.close()
