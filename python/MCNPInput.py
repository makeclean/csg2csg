#/usr/env/python3

from Input import InputDeck
from MCNPCellCard import MCNPCellCard, is_cell_card
from MCNPSurfaceCard import MCNPSurfaceCard, is_surface_card

import logging

class MCNPInput(InputDeck):
    """ MCNPInputDeck class - does the actuall processing 
    """

    # constructor
    def __init__(self,filename):
        InputDeck.__init__(self,filename)
#        self.process()

    def __set_title(self):
        # set the title card
        if "message" in self.file_lines[0]:
            self.title = self.file_lines[1]
            del self.file_lines[0]
            del self.file_lines[0]
        else:
            self.title = self.file_lines[0]
            del self.file_lines[0]

    def process(self):
        self.__set_title()

        # clear out the comment cards
        idx = 0
        while True:
            if idx == len(self.file_lines):
                break
            if self.file_lines[idx][0].lower() == "c":
                del self.file_lines[idx]
            else:
                idx += 1

        # line by line insert into dictionary of cell descriptions
        # until we find a blank line
        idx = 0
        while True:
            cell_card = self.file_lines[idx]
            # its a cell card if the first 2 items are ints and the 
            # third is a float, or if the first 2 items are ints, and the
            # second int is a 0
            if cell_card == "\n": break
            
            if is_cell_card(cell_card):
                cellcard = MCNPCellCard(cell_card)
                logging.debug('%s',cellcard)
                self.cell_list.append(cellcard)
            idx += 1

        idx += 1
        # now process the surfaces
        while True:
            surface_card = self.file_lines[idx]

            # if we find the blank line
            if surface_card == "\n": break

            if is_surface_card(surface_card):
                surfacecard = MCNPSurfaceCard(surface_card)
                logging.debug('%s',surfacecard)
                self.surface_list.append(surfacecard)

            idx += 1
            # if this is a surface card the first item should be an int
            # and the 2nd should be text, its possible the surface has a 
            # tr card associated with it in which case the first is a tr card
            # the 2nd is the surface id the third is surface type          


        #for i in self.surface_list:
        #    print (i,text_description)
        # line by line insert into dictionary of cell descriptions
        #for i in self.file_lines:
        #    print (i)
                
        return

#input = MCNPInput("mcnp_tld.inp")
#input.read()
#input.process()
#for i in input.cell_list:
#    print (i.text_string)
#for i in input.surface_list:
#    print (i.text_string)



    
