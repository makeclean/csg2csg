#/usr/env/python3

from Input import InputDeck
from MCNPCellCard import MCNPCellCard, is_cell_card, write_mcnp_cell
from MCNPSurfaceCard import MCNPSurfaceCard, is_surface_card, write_mcnp_surface
from MCNPDataCard import MCNPTransformCard, MCNPMaterialCard

import logging
import sys

class MCNPInput(InputDeck):
    """ MCNPInputDeck class - does the actuall processing 
    """

    # constructor
    def __init__(self, filename =""):
        InputDeck.__init__(self,filename)
#        self.process()

    # TODO - maybe make a function that aribitrarily extract text
    # between one keyword until another keyword is found

    def __set_title(self):
        # set the title card
        if "message" in self.file_lines[0]:
            self.title = self.file_lines[1]
            del self.file_lines[0]
            del self.file_lines[0]
        else:
            self.title = self.file_lines[0]
            del self.file_lines[0]

    # make a transform card from a string
    def __make_transform_card(self,transform_line):
        tr_card = MCNPTransformCard(transform_line)
        self.transform_list[tr_card.id] = tr_card
        return

    # get the transform cards
    def __get_transform_cards(self, start_line):
        idx = start_line
        while True:
            if idx == len(self.file_lines):
                break

            if "tr" in self.file_lines[idx]:
                self.__make_transform_card(self.file_lines[idx])
            idx += 1
        return

    # extract a material card from the start line until
    def __get_material_card(self, start_line):
        # we already know that the start line has an M init
        idx = start_line
        tokens = self.file_lines[idx].split()
        mat_num = tokens[0]
        mat_num = mat_num.replace("m","")
        
        mcnp_characters = "nvmptwfrdi" #first letters of mcnp keywords

        material_string = ' '.join(tokens[1:]) + " "
        idx += 1

        while True:
            if idx == len(self.file_lines):
                break
            # if we find any character that belongs to a keyword, we are all done
            # with reading a material card
            if any(char in mcnp_characters for char in self.file_lines[idx]):
                break
            else:
                # turns everything into single line string
                material_string += ' '.join(self.file_lines[idx].split()) + " "
            idx += 1

        material = MCNPMaterialCard(mat_num, material_string)
        self.material_list.append(material) 

        return

    # get the material cards definitions
    def __get_material_cards(self, start_line):
        mcnp_keywords = ["mode","prdmp","rdum","idum"]

        idx = start_line
        while True:
            if idx == len(self.file_lines):
                break
            # this crazy makes sure that we find an "m" in the line but that we dont
            # find another keyword with an m in it like prdmp
            if "m" in self.file_lines[idx] and not any(x in self.file_lines[idx] for x in mcnp_keywords):            
               self.__get_material_card(idx)
            idx += 1
        return

    # get the material cards definitions
    def __get_transform_cards(self, start_line):
        idx = start_line
        while True:
            if idx == len(self.file_lines):
                break
            if "tr" in self.file_lines[idx]:
                self.__make_transform_card(self.file_lines[idx])
            idx += 1
        return

    # apply transforms if needed
    def __apply_surface_transformations(self):
        for surf in self.surface_list:
            if surf.surface_transform != 0:
                #surface.transform()
                print (surf)
    
    def process(self):
        self.__set_title()

        # clear out the comment cards
        idx = 0
        while True:
            if idx == len(self.file_lines):
                break
            if self.file_lines[idx][0].lower() == "c":
#                print (self.file_lines[idx])
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

        # now we need to process the data cards like materials
        # now the order of data cards is entirely arbitrary
        # will need to step around all over idx
        # the idx value should now be at the data block
        self.__get_transform_cards(idx)
        self.__get_material_cards(idx)
        self.__apply_surface_transformations()
        
        return


    # write all surfaces to mcnp format
    def __write_mcnp_surfaces(self, filestream):
        filestream.write("C surface definitions\n")
        for surface in self.surface_list:
            write_mcnp_surface(filestream, surface)
        filestream.write("\n") # blank line

    # write all cells to mcnp format
    def __write_mcnp_cells(self, filestream):
        filestream.write("C cell definitions\n")
        for cell in self.cell_list:
            write_mcnp_cell(filestream, cell)
        filestream.write("\n") # the important blank line

    # main write MCNP method, depnds on where the geometry
    # came from
    def write_mcnp(self, filename, flat = True):
        f = open(filename, 'w')
        self.__write_mcnp_cells(f)
        self.__write_mcnp_surfaces(f)



    
