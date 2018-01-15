#/usr/env/python3

from Input import InputDeck

class SerpentInput(InputDeck):
    """ SerpentInput class - does the actual processing
    """

    # constructor
    def __init__(self,filename):
        InputDeck.__init__(self,filename)

    def write_serpent(self, flat = True):
        if flat:
            self.__write_serpent_from_flat()
        else:
            self.__write_serpent_from_hierarchy()
    
