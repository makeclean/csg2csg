#/usr/env/python3

from csg2csg.Input import InputDeck
from csg2csg.SerpentSurfaceCard import SerpentSurfaceCard, write_serpent_surface
from csg2csg.SerpentCellCard import SerpentCellCard, write_serpent_cell
from csg2csg.SerpentMaterialCard import SerpentMaterialCard, write_serpent_material

import logging
import re

class SerpentInput(InputDeck):
    """ SerpentInput class - does the actual processing
    """

    # constructor
    def __init__(self,filename = ""):
        InputDeck.__init__(self,filename)
        
    # extract a material card from the start line until
    def __get_material_card(self, start_line, mat_num):
        # we already know that the start line has an mat name
        idx = start_line
        tokens = self.file_lines[idx].split()
        mat_name = tokens[1]
        # set the material name

        mat_density = float(tokens[2])
        
        # build the first mat string
        material_string = ' '
        idx += 1

        while True:
            # if at the end of the file
            if idx == len(self.file_lines):
                break
            while True:
                # its possible that we will have advanced to the end of the
                # file
                if (idx == len(self.file_lines)):
                    break
                if ('mat' == self.file_lines[idx].split()[0]):
                    break                
                line = self.file_lines[idx]
                if '%' in line:
                    pos = line.find('%')
                    line = line[:pos]
                material_string += line
                # increment the line that we are looking at
                idx += 1
            break
            
        material = SerpentMaterialCard(mat_num, mat_name, mat_density, material_string)

        self.material_list[material.material_number] = material
        
        
        return

    # get the material cards definitions
    def __get_material_cards(self):

        idx = 0
        mat_num = 1
        while True:
            if idx == len(self.file_lines):
                break

            # this crazy makes sure that we find an "mat " in the line
            if re.match(" *mat /*",self.file_lines[idx]):
                logging.debug("%s", "material found on line " + str(idx))
                self.__get_material_card(idx, mat_num)
                mat_num += 1
            idx += 1
        return


    # process the serpent input deck and read into a generic datastructure
    # that we can translate to other formats
    def process(self):

        # clear out the comment and white space cards
        idx = 0
        while True:
            if idx == len(self.file_lines):
                break
            if self.file_lines[idx].isspace():
                del self.file_lines[idx]
            elif self.file_lines[idx].strip().startswith("%"):
                del self.file_lines[idx]
            else:
                idx += 1

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("%s", "Input Echo")
            for idx,line in enumerate(self.file_lines):
                logging.debug("%i %s",idx,line)

        self.__get_material_cards()

        # raise NotImplementedError('Serpent input files are not fully supported yet')

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
        filestream.write("% --- material definitions --- %\n")
        for material in self.material_list:
            write_serpent_material(filestream, self.material_list[material])
        return
    
    # main write serpent method, depending upon where the geometry
    # came from 
    def write_serpent(self, filename, flat = True):
        f = open(filename,'w')   
        self.__write_serpent_surfaces(f)
        self.__write_serpent_cells(f)
        self.__write_serpent_materials(f)
        f.close()
