#/usr/env/python3

from Input import InputDeck

class MCNPInput(InputDeck):
    """ MCNPInputDeck class - does the actuall processing 
    """

    # constructor
    def __init__(self,filename):
        InputDeck.__init__(self,filename)

    def __set_title(self):
        # set the title card
        if "message" in self.file_lines[0]:
            self.title = self.file_lines[1]
        else:
            self.title = self.file_lines[0]

    def process(self):
        self.__set_title()
        return

input = MCNPInput("../files/fng_sic/mcnp_tld_mod")
input.read()


    
