#/usr/env/python3

from Input import InputDeck

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

    # def write a serpent geometry file produced
    # via a method 
    def __write_serpent_from_flat(self, filename):
        # given the a geometry file that has simply been read 
        # into a an InputFile text buffer we can simply write
        # the surface definitions by simple reformat 
        return
    
    # write a serpent geometry produced via
    # a generic translation method
    def __write_serpent_from_hierarchy(self, filename):
        return

    # main write serpent method, depending upon where the geometry
    # came from 
    def write_serpent(self, filename, flat = True):
        if flat:
            self.__write_serpent_from_flat(filename)
        else:
            self.__write_serpent_from_hierarchy(filename)
    
