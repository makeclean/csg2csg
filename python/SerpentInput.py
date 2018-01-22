#/usr/env/python3

from Input import InputDeck
from SerpentSurfaceCard import SerpentSurfaceCard, write_serpent_surface
from SerpentCellCard import SerpentCellCard, write_serpent_cell

class SerpentInput(InputDeck):
    """ SerpentInput class - does the actual processing
    """

    # constructor
    def __init__(self,filename = ""):
        InputDeck.__init__(self,filename)
        
    def from_input(self,InputDeckClass):
        InputDeck.filename = InputDeckClass.filename
        InputDeck.title = InputDeckClass.title
        InputDeck.cell_list = InputDeckClass.cell_list
        InputDeck.surfcace_list = InputDeckClass.surface_list
        return

    # Write the Serpent Cell definitions
    def __write_serpent_cells(self, filestream):
        filestream.write("% --- cell definitions --- %\n")
        for cell in self.cell_list:
            write_serpent_cell(filestream,cell)
        return
    
    # write the serpent surface definitions 
    def __write_serpent_surfaces(self, filestream):
        filestream.write("% --- surface definitions --- %\n")
        for surface in self.surface_list:
            write_serpent_surface(filestream,surface)
        return

    # write the material compositions
    def __write_serpent_materials(self, filestream):
        filestream.write("% --- material definitions --- %n")
        for material in self.material_list:
            write_serpent_material(filestream, material)
        return
    
    # main write serpent method, depending upon where the geometry
    # came from 
    def write_serpent(self, filename, flat = True):
        f = open(filename,'w')   
        self.__write_serpent_surfaces(f)
        self.__write_serpent_cells(f)
#        self.__write_serpent_materials(f)
        f.close()
