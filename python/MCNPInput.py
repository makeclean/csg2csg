#/usr/env/python3

from Input import InputDeck
from SurfaceCard import SurfaceCard
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
        mcnp_keywords = ["mode","prdmp","rdum","idum","sdef","si","sp","wwe","fm","vol","tr","fc","*","print"]

        idx = start_line
        while True:
            if idx == len(self.file_lines):
                break

            # this crazy makes sure that we find an "m" in the line but that we dont
            # find another keyword with an m in it like prdmp
            if re.match(" *m[0-9]/*",self.file_lines[idx]):
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

    # explode a macrobody into surfaces
    def explode_macrobody(self,Surface):
        new_surf_list = []
        if Surface.surface_type == SurfaceCard.SurfaceType["MACRO_RPP"]:
            id = int(Surface.surface_id)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " px " + str(Surface.surface_coefficients[0]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " px " + str(Surface.surface_coefficients[1]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " py " + str(Surface.surface_coefficients[2]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " py " + str(Surface.surface_coefficients[3]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " pz " + str(Surface.surface_coefficients[4]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " pz " + str(Surface.surface_coefficients[5]))
            new_surf_list.append(surf)
            # appropriate cell description for inside the macrobody
            cell_description_inside = "( " + str(new_surf_list[0].surface_id)
            cell_description_inside += " -" + str(new_surf_list[1].surface_id)
            cell_description_inside += "  " + str(new_surf_list[2].surface_id)
            cell_description_inside += " -" + str(new_surf_list[3].surface_id)
            cell_description_inside += "  " + str(new_surf_list[4].surface_id)
            cell_description_inside += " -" + str(new_surf_list[5].surface_id)
            cell_description_inside += " )"
            # appropriate cell descripiton for outside the macrobody
            cell_description_outside = "(-" + str(new_surf_list[0].surface_id)
            cell_description_outside += ":" + str(new_surf_list[1].surface_id)
            cell_description_outside += ":-" + str(new_surf_list[2].surface_id)
            cell_description_outside += ":" + str(new_surf_list[3].surface_id)
            cell_description_outside += ":-" + str(new_surf_list[4].surface_id)
            cell_description_outside += ":" + str(new_surf_list[5].surface_id)
            cell_description_outside += ")"

            cell_description = [cell_description_inside,cell_description_outside]

            return cell_description, new_surf_list


    # if we find a macrobody in the surface list 
    # explode it into a surface based definition
    def __flatten_macrobodies(self):
        # look through the list until we find
        # a macrobody
        to_remove = []
        for surf in self.surface_list:
            # if we are a macrobody
            if surf.is_macrobody():
                # explode into constituent surfaces
                cell_description, new_surfaces = self.explode_macrobody(surf)
                # insert the new surfaces into the surface_list
                self.surface_list.extend(new_surfaces)
                # remove the old surface
                to_remove.append(surf)
#                self.surface_list.remove(surf)
                # update the cell definition
                for jdx, cell in enumerate(self.cell_list):
                    # for each part of the cell
#                    for idx, item in enumerate(cell.cell_text_description):
                    for idx, item in enumerate(cell.cell_text_description):
                        # if we find a matching surface
                        if item == str(surf.surface_id): # found the outside description
                            cell.cell_text_description[idx] = cell_description[1]
                            self.cell_list[jdx] = cell
                            text_string = ' '.join(cell.cell_text_description)
                            self.cell_list[jdx].update(text_string) 
                        elif item == str(-1*surf.surface_id): # found the inside description
                            cell.cell_text_description[idx] = cell_description[0]
                            self.cell_list[jdx] = cell
                            text_string = ' '.join(cell.cell_text_description)
                            self.cell_list[jdx].update(text_string)
                        else:
                            pass
                            
        # clear up removed surfaces
        for surf in to_remove:
            self.surface_list.remove(surf)
        return

    # generate bounding coordinates 
    def __generate_bounding_coordinates(self):
        # loop through the surfaces and generate the bounding coordinates
        # condisder only manifold or simple infinite surfaces, like planes
        for surf in self.surface_list:
            box = surf.bounding_box()
            if box[0] < self.bounding_coordinates[0]:
                self.bounding_coordinates[0] = box[0]
            if box[1] > self.bounding_coordinates[1]:
                self.bounding_coordinates[1] = box[1]
            if box[2] < self.bounding_coordinates[2]:
                self.bounding_coordinates[2] = box[2]
            if box[3] > self.bounding_coordinates[3]:
                self.bounding_coordinates[3] = box[3]
            if box[4] < self.bounding_coordinates[4]:
                self.bounding_coordinates[4] = box[4]
            if box[5] > self.bounding_coordinates[5]:
                self.bounding_coordinates[5] = box[5]
        logging.debug("%s 6%e", "bounding box of geometry is ", self.bounding_coordinates[0],self.bounding_coordinates[1],
                      self.bounding_coordinates[2],self.bounding_coordinates[3],self.bounding_coordinates[4],self.bounding_coordinates[5])

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
                self.cell_list.append(cellcard)
            idx += 1
        """
        idx += 1
        print (idx,self.file_lines[idx])
        # idx should have advanced file reading such that we are now at the first
        # surface line
        # now process the surfaces
        while True:
            surface_card = self.file_lines[idx]
            logging.debug('%s','surface cards start at line '+ str(idx))
            
            # if we find the blank line
            if surface_card == "\n" or surface_card.isspace():
                logging.debug('%s', "found end of surfaces at line " + str(idx))
                idx += 1
                break
                           
            if is_surface_card(surface_card):
                surfacecard = MCNPSurfaceCard(surface_card)
                logging.debug('%s',surfacecard)
                self.surface_list.append(surfacecard)
                # update the surface index counter
                if surfacecard.surface_id > self.last_free_surface_index: 
                    self.last_free_surface_index = surfacecard.surface_id

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

        # we need to turn macrobodies into regular surface descriptions
        self.__flatten_macrobodies()
        self.__generate_bounding_coordinates()
        
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


    
