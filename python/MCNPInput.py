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
        # set the material number
        
        # rebuild the first mat string
        material_string = ' '.join(tokens[1:]) + " " 
        if '$' in material_string:
            pos = material_string.find('$')
            material_string = material_string[:pos]
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
                line = self.file_lines[idx]
                # mcnp continue line is indicated by 5 spaces
                if line[0:5] == "     ":
                    if '$' in line:
                        pos = line.find('$')
                        line = line[:pos]
                    material_string += line
                else: # else we have found a new cell card
                    break 
                # increment the line that we are looking at
                idx += 1
            break

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
            #cell_line = self.file_lines[jdx]
            if idx == len(self.file_lines):
                return

            if re.match("^\*?tr",self.file_lines[idx]):
                logging.debug("%s", "trn card found on line " + str(idx))
                card_line = self.file_lines[idx]
                idx += 1 # only check one more line ahead
                # mcnp continue line is indicated by 5 spaces
                while self.file_lines[idx][0:5] == "     ":
                    logging.debug("%s", "trn card has continue line " + str(idx))
                    card_line += self.file_lines[idx]
                    idx += 1
                idx -=1 
                self.__make_transform_card(card_line)
                card_line = ""
            idx += 1
        return

        
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
                surf.generalise() # generalise the surface into a gq
                try:
                    self.transform_list[surf.surface_transform]
                    surf.transform(self.transform_list[surf.surface_transform])
                except KeyError:
                    print ("transform " + surf.surface_transform +" not found ")
                    #sys.exit()
            else:
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
    # material number/ density pairs - this to avoid mcnp's
    # overloadable materials
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
            material.explode_elements()
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
            cell_description_outside += " : " + str(new_surf_list[1].surface_id)
            cell_description_outside += " : -" + str(new_surf_list[2].surface_id)
            cell_description_outside += " : " + str(new_surf_list[3].surface_id)
            cell_description_outside += " : -" + str(new_surf_list[4].surface_id)
            cell_description_outside += " : " + str(new_surf_list[5].surface_id)
            cell_description_outside += ")"
            
            cell_description = [cell_description_inside,cell_description_outside]
            
        elif Surface.surface_type == SurfaceCard.SurfaceType["MACRO_RCC"]:
            id = int(Surface.surface_id)
            if Surface.surface_coefficients[3] == 0. and Surface.surface_coefficients[4] == 0.:
                # if coefficients 4 & 5 are zero then its a cz with planes at 
                self.last_free_surface_index += 1
                surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " pz " + str(Surface.surface_coefficients[2]))
                new_surf_list.append(surf)
                self.last_free_surface_index += 1
                surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " pz " + str(Surface.surface_coefficients[5]))
                new_surf_list.append(surf)
                self.last_free_surface_index += 1
                surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " c/z " +
                                       str(Surface.surface_coefficients[0]) + " " +
                                       str(Surface.surface_coefficients[1]) + " " +
                                       str(Surface.surface_coefficients[6]))
                new_surf_list.append(surf)
                cell_description_inside = "("
                cell_description_inside += str(new_surf_list[0].surface_id)
                cell_description_inside += " -" + str(new_surf_list[1].surface_id)
                cell_description_inside += " " + str(new_surf_list[2].surface_id)
                cell_description_inside += ")"

                cell_description_outside = "("
                cell_description_outside += " -" +str(new_surf_list[0].surface_id)
                cell_description_outside += "  " + str(new_surf_list[1].surface_id)
                cell_description_outside += " -" + str(new_surf_list[2].surface_id)
                cell_description_outside += ")"

                cell_description = [cell_description_inside,cell_description_outside]
                        
            else:
                print ("Need to implement the other RCC explode kinds")
                cell_description = ["",""]
        else:
            print ("Need to implement the other macro body types")
            cell_description = ["",""]
        
    
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

                # update the cell definition - loop over all cells
                for jdx, cell in enumerate(self.cell_list):
                    # for each part of the cell - for each component in the cell
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

    # any more nots to process
    def __nots_remaining(self, cell):
        for i in cell.cell_interpreted:
            if not isinstance(i,cell.OperationType):
                if re.findall("#(\d+)",i):
                    return True
        return False

    # split the first # we find
    def __split_nots(self,cell):
        # if the cell has a not in it
        pos = 0
        count = 0 
        # loop over the constituents of the cell
        # we have to do this rookie looking stuff
        # because cell.OperationType is not iterable
        for i in cell.cell_interpreted:
            # if its not an operation 
            if not isinstance(i,cell.OperationType):
                if "#" in  i:
                    pos = count
                    break
            count = count + 1

        # now we know the position of the # arguments in the

        cell_id = re.findall("#(\d+)",cell.cell_interpreted[pos])
        if not cell_id:
            return
        cell_id = cell_id[0]

        # get the cell for the not
        cell_text = self.find_cell(cell_id)
        cell_text = cell_text.cell_interpreted
        # build the cell into the interpreted form
        cell_text = [cell.OperationType(2)] + ["("] + cell_text
        cell_text = cell_text + [")"]
        
        # remove the #cell and insert the full new form
        cell_part = cell.cell_interpreted[0:pos-1]
        
        cell_part.extend(cell_text)
        cell_part2 = cell.cell_interpreted[pos+1:]
        cell_part.extend(cell_part2)
        cell.cell_interpreted = cell_part

        return
        
    # loop through the cells and insert
    # cell definititons where needed
    # assuming that we have nots of the form #33 #44 and
    # not #(33 44) as this pertains to surfaces
    def __explode_nots(self):
        for cell in self.cell_list:
            while self.__nots_remaining(cell):
                self.__split_nots(cell)
            continue
            

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
        logging.debug("%s ", "bounding box of geometry is " + str(self.bounding_coordinates[0]) + " " + 
                      str(self.bounding_coordinates[1]) + " " +
                      str(self.bounding_coordinates[2]) + " " + 
                      str(self.bounding_coordinates[3]) + " " + 
                      str(self.bounding_coordinates[4]) + " " + 
                      str(self.bounding_coordinates[5]) + "\n")

    # update surfaces that need their bounding coordinates updated
    def __update_surfaces(self):
        for surf in self.surface_list:
            if surf.surface_type in [SurfaceCard.SurfaceType["CONE_X"],
                                     SurfaceCard.SurfaceType["CONE_Y"],
                                     SurfaceCard.SurfaceType["CONE_Z"]]:
                if surf.surface_type == SurfaceCard.SurfaceType["CONE_X"]:
                    surf.b_box[0] = self.bounding_coordinates[0]
                    surf.b_box[1] = self.bounding_coordinates[1]
                elif surf.surface_type == SurfaceCard.SurfaceType["CONE_Y"]:
                    surf.b_box[2] = self.bounding_coordinates[2]
                    surf.b_box[3] = self.bounding_coordinates[3]
                elif surf.surface_type == SurfaceCard.SurfaceType["CONE_Z"]:
                    surf.b_box[4] = self.bounding_coordinates[4]
                    surf.b_box[5] = self.bounding_coordinates[5]
                else:
                    pass
        return

    # extract all the cell cards
    def __get_cell_cards(self):
        # line by line insert into dictionary of cell descriptions
        # until we find a blank line
        idx = 0
        while True:
            cell_line = self.file_lines[idx]
            if cell_line == "\n":
                logging.debug('%s',"found end of cell cards at line " + str(idx))
                idx += 1
                break

            card_line = cell_line
            jdx = idx + 1
            # scan until we are all done
            while True:
                cell_line = self.file_lines[jdx]
                pos_comment = cell_line.find("$")
                cell_comment = ""
                
                if pos_comment != -1:
                    cell_line = cell_line[:pos_comment]
                    self.file_lines[jdx] = cell_line # update the file data
                    cell_comment = cell_line[pos_comment:] # set the comment
                
                # mcnp continue line is indicated by 5 spaces
                if cell_line[0:5] == "     ":
                    card_line += cell_line
                else: # else we have found a new cell card
                    cellcard = MCNPCellCard(card_line)
                    # we should set the comment here
                    self.cell_list.append(cellcard)
                    break 
                jdx += 1
            idx = jdx                   
        return idx

    # extract all the surface cards from the input deck
    def __get_surface_cards(self,idx):
        while True:
            surf_line = self.file_lines[idx]
            if surf_line == "\n":
                logging.debug('%s',"found end of cell cards at line " + str(idx))
                idx += 1
                break

            surf_card = surf_line
            jdx = idx + 1
            # scan until we are all done
            while True:
                surf_line = self.file_lines[jdx]
                # mcnp continue line is indicated by 5 spaces
                if surf_line[0:5] == "     ":
                    surf_card += surf_line
                else: # else we have found a new surf card
                    surfacecard = MCNPSurfaceCard(surf_card)
                    self.surface_list.append(surfacecard)
                    # update the surface index counter
                    if surfacecard.surface_id > self.last_free_surface_index: 
                        self.last_free_surface_index = surfacecard.surface_id
                    break 
                jdx += 1
            idx = jdx                  
        return idx

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
            

        # get the cell cards
        idx = self.__get_cell_cards()

        # idx should have advanced file reading such that we are now at the first
        # surface line and now process the surfaces
        # line by line insert into dictionary of cell descriptions
        # until we find a blank line
        idx = self.__get_surface_cards(idx)

        # now we need to process the data cards like materials
        # now the order of data cards is entirely arbitrary
        # will need to step around all over idx
        # the idx value should now be at the data block
        # also idx will never be advanced from this point

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
        self.__explode_nots()

        self.__generate_bounding_coordinates()
        # update the bounding coordinates of surfaces that need it
        # cones for example
        self.__update_surfaces()

        self.split_unions()
       
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
        f.close()
        
    
