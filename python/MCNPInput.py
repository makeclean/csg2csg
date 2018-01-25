#/usr/env/python3

from Input import InputDeck
from MCNPCellCard import MCNPCellCard, is_cell_card, write_mcnp_cell
from MCNPSurfaceCard import MCNPSurfaceCard, is_surface_card, write_mcnp_surface
from MCNPDataCard import MCNPTransformCard
from MCNPMaterialCard import MCNPMaterialCard, write_mcnp_material

from collections import Counter

from copy import deepcopy
import logging
import sys
import re

class MCNPInput(InputDeck):
    """ MCNPInputDeck class - does the actuall processing 
    """
    preserve_xsid = False

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
        line = start_line
        while True:
            if line == len(self.file_lines):
                break

            if "tr" in self.file_lines[line]:
                self.__make_transform_card(self.file_lines[line])
            line += 1
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
        self.material_list[material.material_number] = material

        return

    # get the material cards definitions
    def __get_material_cards(self, start_line):
        mcnp_keywords = ["mode","prdmp","rdum","idum","sdef","si","sp","wwe","fm","vol","tr","fc"]

        idx = start_line
        while True:
            if idx == len(self.file_lines):
                break
            # this crazy makes sure that we find an "m" in the line but that we dont
            # find another keyword with an m in it like prdmp
            if re.match("^m[0-9]+",self.file_lines[idx]):
#            if "m" in self.file_lines[idx] and not any(x in self.file_lines[idx] for x in mcnp_keywords):
                logging.debug("%s", "material found on line " + str(idx))
                self.__get_material_card(idx)
            idx += 1
        return

    # get the material cards definitions
    def __get_transform_cards(self, start_line):
        idx = start_line     

        while True:
            if idx == len(self.file_lines):
                break
            if re.match("^\*?tr",self.file_lines[idx]):
                self.__make_transform_card(self.file_lines[idx])
            idx += 1
        return

    # apply transforms if needed
    # need to figure out how MCNP does its surface transforms
    # this is not a widely supported feature amongst other
    # monte carlo codes
    def __apply_surface_transformations(self):
        for surf in self.surface_list:
            if surf.surface_transform != 0:
                #surface.transform()
                #print (surf)
                pass

    # find the next free material number 
    def __next_free_int(self):
        idx = 1
        while True:
            if str(idx) in self.material_list.keys():
                idx += 1
            else:
                break
        return str(idx)

    # reorganise materials such that we get a new set of unique 
    # material number/ density pairs
    def __reorganise_materials(self):
        material_density = {}
        for cell in self.cell_list:
            # if the material number already exists
            if cell.cell_material_number in material_density:
                # append another density if its unique
                if not any(cell.cell_density == density for density in material_density[cell.cell_material_number]):
                    material_density[cell.cell_material_number].append(cell.cell_density)
            else:
                material_density[cell.cell_material_number] = [cell.cell_density]
        # remove density 0.0 and material 0
        if 0 in material_density.keys(): del material_density[0]

        # loop over the material_number density pairs
        for mat in sorted(material_density.keys()):
            num_densities = len(material_density[mat])
            if num_densities > 1:
                # the first density is cannonical
                self.material_list[str(mat)].density = material_density[mat][0]

                # the the remaining materials/density pairs get new material
                for density in material_density[mat][1:]:
                    material = deepcopy(self.material_list[str(mat)])
                    material.density = density
                    material.material_number = self.__next_free_int()
                    material.material_name = "Copy of Material " + str(mat) + " with density "
                    material.material_name += str(density)

                    self.material_list[str(material.material_number)] = material

                    # go through cells and update the material numbers accordingly
                    for idx in range(len(self.cell_list)):
                        cell = self.cell_list[idx]
                        # if we match
                        if cell.cell_material_number == mat and cell.cell_density == density:
                            # update the cell material number - density is already correct
                            cell.cell_material_number = material.material_number
            else:
                # there is only one density for this material, assign it directly
                self.material_list[str(mat)].density = material_density[mat][0]

        # normalise the material dictionary
        for mat in self.material_list:
            material = self.material_list[mat]
            material.normalise()
            self.material_list[mat] = material

        return

    # process the mcnp input deck and read into a generic datastructure
    # that we can translate to other formats
    def process(self):

        self.__set_title()

        # clear out the comment cards
        idx = 0
        while True:
            if idx == len(self.file_lines):
                break
            if self.file_lines[idx][0] == "c":
                del self.file_lines[idx]
            else:
                idx += 1

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("%s", "Input Echo")
            for idx,line in enumerate(self.file_lines):
                logging.debug("%i %s",idx,line)
            

        # line by line insert into dictionary of cell descriptions
        # until we find a blank line
        idx = 0
        while True:
            cell_line = self.file_lines[idx]
            if cell_line == "\n":
                logging.debug('%s',"found end of cell cards at line " + str(idx))
                idx += 1
                break
            # if we are a cell card
            if is_cell_card(cell_line):
                jdx = idx + 1
                # if were are at the end of cell data
                if self.file_lines[jdx] == "\n":
                    cell_card = MCNPCellCard(cell_line)
                    self.cell_list.append(cell_card)
                    break
                # if we immediately find another valid cell card
                if is_cell_card(self.file_lines[jdx]):
                    cell_card = MCNPCellCard(cell_line)
                    self.cell_list.append(cell_card)
                # until we discover a new valid cell line                    
                else:
                    while not is_cell_card(self.file_lines[jdx]):
                        cell_line += self.file_lines[jdx]
                        jdx += 1
                        cellcard = MCNPCellCard(cell_line)
                        self.cell_list.append(cellcard)
                idx += 1
        idx +=1 
        """
        while True:
            cell_card = self.file_lines[idx]
            # its a cell card if the first 2 items are ints and the 
            # third is a float, or if the first 2 items are ints, and the
            # second int is a 0
            if cell_card == "\n": break

            # the first instance of cell_card should start the string of a cell
            # the next time we find a valid cell card, should start a new one
            
            if is_cell_card(cell_card):
                cellcard = MCNPCellCard(cell_card)
                logging.debug('%s',cellcard)
                self.cell_list.append(cellcard)
            idx += 1
        """
        idx += 1
        # idx should have advanced file reading such that we are now at the first
        # surface line
        # now process the surfaces
        while True:
            surface_card = self.file_lines[idx]

            # if we find the blank line
            if surface_card == "\n":
                logging.debug('%s', "found end of surfaces at line " + str(idx))
                break
                           
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

        # materials in other codes are tie their composition
        # and density together - need to make new material cards
        # based on the mateiral number / density pairs
        # and update cells accordingly.
        self.__reorganise_materials()
        
        return

    # perhaps these write functions should actually build strings 
    # and then write at once?
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

    # write all cells to mcnp format
    def __write_mcnp_materials(self, filestream):
        filestream.write("C material definitions\n")
        for material in sorted(self.material_list.keys()):
            write_mcnp_material(filestream, self.material_list[material], self.preserve_xsid )

    # main write MCNP method, depnds on where the geometry
    # came from
    def write_mcnp(self, filename, flat = True):
        f = open(filename, 'w')
        self.__write_mcnp_cells(f)
        self.__write_mcnp_surfaces(f)
        self.__write_mcnp_materials(f)


    
