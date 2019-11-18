#/usr/env/python3

from csg2csg.Input import InputDeck #, get_surface_with_id
from csg2csg.SurfaceCard import SurfaceCard #, BoundaryCondition
from csg2csg.ParticleNames import particleToGeneric, ParticleNames
from csg2csg.MaterialCard import get_material_colour
from csg2csg.MCNPParticleNames import mcnpToParticle
from csg2csg.MCNPFormatter import strip_dollar_comments
from csg2csg.MCNPCellCard import MCNPCellCard, is_cell_card, write_mcnp_cell
from csg2csg.MCNPSurfaceCard import MCNPSurfaceCard, is_surface_card, write_mcnp_surface
from csg2csg.MCNPDataCard import MCNPTransformCard
from csg2csg.MCNPMaterialCard import MCNPMaterialCard, write_mcnp_material

from collections import Counter

from numpy import linalg as np
from numpy import dot 
from numpy import cross 
from numpy import inf as npinf
from numpy import around as nparound

from copy import deepcopy

import warnings
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
        logging.debug("%s", "TR card initialised " + str(tr_card))
        self.transform_list[tr_card.id] = tr_card
        return

    def __process_importances(self):
        # process the lists
        for particle in self.importance_list.keys():
            # early exit
            if 'i' not in self.importance_list[particle] and \
               'r' not in self.importance_list[particle]:
                return

            importance_list = self.importance_list[particle].split()
            # look through the list for r's or i's
            # in mcnp syntax Xr means repeat the value previous
            # to x r times
            for idx,value in enumerate(importance_list):
                # if we find a repeat value
                if 'r' in value:
                    repeat = int(value.replace("r","")) - 1
                    # this is safe since r cannot be the first
                    # value in the list
                    last_importance = importance_list[idx-1]  
                    to_insert = [last_importance]*repeat
                    importance_list[idx] = ' '.join(str(e) for e in to_insert)
            # flatten the list
            self.importance_list[particle] = ' '.join(str(e) for e in importance_list)         

        return

    # get the importance cards
    def __get_importances(self, start_line):
        idx = start_line

        # dictionary of importances
        while True:
            # check to see if we are at the end of the file
            if idx == len(self.file_lines):
                #print (self.importance_list)
                return self.__process_importances()

            # check for importance keyword
            if "imp" in self.file_lines[idx]:
                particle = self.file_lines[idx].split()[0].split(":")[1]
               
                # TODO mcnp allows the following forms imp:n imp:n,p etc 
                particle = mcnpToParticle(particle)
                logging.debug("%s", "found importance statement for particle " + 
                              particleToGeneric(particle) + " on line" + str(idx))

                self.importance_list[particle] = self.file_lines[idx][5:].rstrip()
                idx += 1
                # while we find a continue line
                while self.file_lines[idx][0:5] == "     ":
                    self.importance_list[particle] += self.file_lines[idx].rstrip()
                    logging.debug("%s", "importance statement has continue line" + str(idx))
                    idx += 1
                else:
                    continue
            else:
                # otherwise advance the line by one
                idx += 1        

        return

    """ Given a starting line munge through the file
    looking to read weight window information. MCNP
    Supports at least two forms of reading weight
    window information

    1) a wwe card 
    """
    def __get_weight_windows(self, start_line):
        return
        line = start_line
        while True:
            if line == len(self.file_lines):
                break


            # if 'wwe' in line:

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
        # set the colour based on the number of colours
        # but only if its really used rather than a tally
        # multiplier material
        material.material_colour = get_material_colour(len(self.material_list))
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

    # apply surface transforms if needed
    def __apply_surface_transformations(self):
        for surf in self.surface_list:
            if surf.surface_transform != 0 and not surf.is_macrobody():
                surf.generalise() # generalise the surface into a gq
                if surf.surface_transform in self.transform_list.keys():
                    surf.transform(self.transform_list[surf.surface_transform])
                    surf.simplify() # turn the transformed surface into its simplest form
                else:
                    print ("transform " + surf.surface_transform +" not found ")
            else:
                pass

    # apply universe transformations if needed
    def __apply_universe_transformations(self):

        # loop over all the cells
        for cell in self.cell_list:
            # if the transform id is not 0
            if cell.cell_universe_transformation_id is not "0":
                # apply the transform
                cell.apply_universe_transform(self.transform_list[cell.cell_universe_transformation_id])
                

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

        # maybe void problem
        if not len(material_density): return

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

    # helper function for macrobody explosion
    def __make_new_plane(self, vector, offset):
        self.last_free_surface_index += 1
        surface_string = str(self.last_free_surface_index) + " p "
        for coeff in vector:
            surface_string += str(coeff) + " "
        surface_string += str(offset)
        surf = MCNPSurfaceCard(surface_string) # todo maybe instanciate explicitly generically?
        return surf

    def __macro_rcc_cylinder_arbitrary(self,Surface,vector):

        new_surf_list = []
        cell_description = []

        # this is where the cylinder points
        axis_vector = vector/np.norm(vector)
        # the vector perpendicular to this will be the capping plane

        gq_coeffs = [0]*10

        # form the gq quadratic terms
        gq_coeffs[0] = 1. - axis_vector[0]**2
        gq_coeffs[1] = 1. - axis_vector[1]**2        
        gq_coeffs[2] = 1. - axis_vector[2]**2 
        # form the rotational terms
        gq_coeffs[3] = -2.*axis_vector[0]*axis_vector[1]        
        gq_coeffs[4] = -2.*axis_vector[1]*axis_vector[2]        
        gq_coeffs[5] = -2.*axis_vector[0]*axis_vector[2]
        # form the linear offset terms
        gq_coeffs[6] =  -Surface.surface_coefficients[1]*gq_coeffs[3] \
                        -Surface.surface_coefficients[2]*gq_coeffs[5] \
                        -2.0*Surface.surface_coefficients[0]*gq_coeffs[0]
        gq_coeffs[7] =  -Surface.surface_coefficients[0]*gq_coeffs[3] \
                        -Surface.surface_coefficients[2]*gq_coeffs[4] \
                        -2.0*Surface.surface_coefficients[1]*gq_coeffs[1]
        gq_coeffs[8] =  -Surface.surface_coefficients[0]*gq_coeffs[5] \
                        -Surface.surface_coefficients[1]*gq_coeffs[4] \
                        -2.0*Surface.surface_coefficients[2]*gq_coeffs[2]
        # form the offset term
        gq_coeffs[9] = Surface.surface_coefficients[0]*Surface.surface_coefficients[1]*gq_coeffs[3] + \
                       Surface.surface_coefficients[1]*Surface.surface_coefficients[2]*gq_coeffs[4] + \
                       Surface.surface_coefficients[0]*Surface.surface_coefficients[2]*gq_coeffs[5] + \
                       Surface.surface_coefficients[0]**2*gq_coeffs[0] + \
                       Surface.surface_coefficients[1]**2*gq_coeffs[1] + \
                       Surface.surface_coefficients[2]**2*gq_coeffs[2] - \
                       Surface.surface_coefficients[6]**2

        #for idx,coeff in enumerate(gq_coeffs):
        #    gq_coeffs[idx] = nparound(coeff,decimals=15)

        self.last_free_surface_index += 1
        surface_string = str(self.last_free_surface_index) + " gq "
        for coeff in gq_coeffs:
            surface_string += str(coeff) + " "
        surf = MCNPSurfaceCard(surface_string) # todo maybe instanciate explicitly generically?
        new_surf_list.append(surf)

        # plane offset 1
        d1 =   axis_vector[0]*Surface.surface_coefficients[0] \
             + axis_vector[1]*Surface.surface_coefficients[1] \
             + axis_vector[2]*Surface.surface_coefficients[2]

        self.last_free_surface_index += 1
        surface_string = str(self.last_free_surface_index) + " p "
        for coeff in axis_vector:
            surface_string += str(-1.*coeff) + " "
        surface_string += str(-d1)
        surf = MCNPSurfaceCard(surface_string) # todo maybe instanciate explicitly generically?
        new_surf_list.append(surf)


        # plane offset 2
        d2 =   axis_vector[0]*(Surface.surface_coefficients[0] + vector[0]) \
             + axis_vector[1]*(Surface.surface_coefficients[1] + vector[1]) \
             + axis_vector[2]*(Surface.surface_coefficients[2] + vector[2]) 

        self.last_free_surface_index += 1
        surface_string = str(self.last_free_surface_index) + " p "
        for coeff in axis_vector:
            surface_string += str(coeff) + " "
        surface_string += str(d2)
        surf = MCNPSurfaceCard(surface_string) # todo maybe instanciate explicitly generically?
        new_surf_list.append(surf)

        cell_description_inside = "("
        cell_description_inside += " -" + str(new_surf_list[0].surface_id)
        cell_description_inside += " -" + str(new_surf_list[1].surface_id)
        cell_description_inside += " -"  + str(new_surf_list[2].surface_id)
        cell_description_inside += ")"

        cell_description_outside = "("
        cell_description_outside += str(new_surf_list[0].surface_id)
        cell_description_outside += ":" + str(new_surf_list[1].surface_id)
        cell_description_outside += ":" + str(new_surf_list[2].surface_id)
        cell_description_outside += ")"

        cell_description = [cell_description_inside,cell_description_outside]

        return new_surf_list, cell_description

    def __macro_rcc_cylinder(self,Surface,vector):
        new_surf_list = []

        if vector[0] == 0 and vector[1] == 0:
            plane = " pz "
            cylinder = " c/z "
            c1 = Surface.surface_coefficients[0]
            c2 = Surface.surface_coefficients[1]
            top = Surface.surface_coefficients[5] + Surface.surface_coefficients[2]
            bottom = Surface.surface_coefficients[2]
        elif vector[0] == 0 and vector[2] == 0:
            plane = " py "
            cylinder = " c/y "
            c1 = Surface.surface_coefficients[0]
            c2 = Surface.surface_coefficients[2]
            top = Surface.surface_coefficients[4] + Surface.surface_coefficients[1]
            bottom = Surface.surface_coefficients[1]
        elif vector[1] == 0 and vector[2] == 0:
            plane = " px "
            cylinder = " c/x "
            c1 = Surface.surface_coefficients[1]
            c2 = Surface.surface_coefficients[2]
            top = Surface.surface_coefficients[3] + Surface.surface_coefficients[0] 
            bottom = Surface.surface_coefficients[0]


        # if coefficients 4 & 5 are zero then its a cz with planes at 
        self.last_free_surface_index += 1
        surf = MCNPSurfaceCard(str(self.last_free_surface_index) + cylinder +
                                str(c1) + " " +
                                str(c2) + " " +
                                str(Surface.surface_coefficients[6]))
        new_surf_list.append(surf)
        self.last_free_surface_index += 1
        surf = MCNPSurfaceCard(str(self.last_free_surface_index) + plane + str(bottom))
        new_surf_list.append(surf)
        self.last_free_surface_index += 1
        surf = MCNPSurfaceCard(str(self.last_free_surface_index) + plane + str(top))
        new_surf_list.append(surf)

        cell_description_inside = "("
        cell_description_inside += " -" + str(new_surf_list[0].surface_id)
        cell_description_inside += " -" + str(new_surf_list[1].surface_id)
        cell_description_inside += " -" + str(new_surf_list[2].surface_id)
        cell_description_inside += ")"

        cell_description_outside = "("
        cell_description_outside += "  " +str(new_surf_list[0].surface_id)
        cell_description_outside += ":" + str(new_surf_list[1].surface_id)
        cell_description_outside += ":" + str(new_surf_list[2].surface_id)
        cell_description_outside += ")"

        cell_description = [cell_description_inside,cell_description_outside]

        return new_surf_list, cell_description

    # explode a macrobody into surfaces
    def explode_macrobody(self,Surface):
        new_surf_list = []
        # NOTE MCNP Macrobodies have +ve sense outside of it, and -ve sense inside
        # of it. Therefore, on a RPP the first index is the right hand side of the cube
        # and the 2nd is the left hand side
        if Surface.surface_type == SurfaceCard.SurfaceType["MACRO_RPP"]:
            # the order is weird here but so is MCNP
            id = int(Surface.surface_id)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " px " + str(Surface.surface_coefficients[1]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " p -1.0 0 0 " + str(-1.0*Surface.surface_coefficients[0]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " py " + str(Surface.surface_coefficients[3]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " p 0 -1.0 0 " + str(-1.0*Surface.surface_coefficients[2]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " pz " + str(Surface.surface_coefficients[5]))
            new_surf_list.append(surf)
            self.last_free_surface_index += 1
            surf = MCNPSurfaceCard(str(self.last_free_surface_index) + " p 0 0 -1.0 " + str(-1.0*Surface.surface_coefficients[4]))
            new_surf_list.append(surf)
            # NOTE new_surf list here is now in MCNP facet order
            # appropriate cell description for inside the macrobody
            cell_description_inside = "( -" + str(new_surf_list[0].surface_id)
            cell_description_inside += " -" + str(new_surf_list[1].surface_id)
            cell_description_inside += " -" + str(new_surf_list[2].surface_id)
            cell_description_inside += " -" + str(new_surf_list[3].surface_id)
            cell_description_inside += " -" + str(new_surf_list[4].surface_id)
            cell_description_inside += " -" + str(new_surf_list[5].surface_id)
            cell_description_inside += " )"
            # appropriate cell descripiton for outside the macrobody
            cell_description_outside = "( " + str(new_surf_list[0].surface_id)
            cell_description_outside += " : " + str(new_surf_list[1].surface_id)
            cell_description_outside += " : " + str(new_surf_list[2].surface_id)
            cell_description_outside += " : " + str(new_surf_list[3].surface_id)
            cell_description_outside += " : " + str(new_surf_list[4].surface_id)
            cell_description_outside += " : " + str(new_surf_list[5].surface_id)
            cell_description_outside += ")"
            
            cell_description = [cell_description_inside,cell_description_outside]
            
        elif Surface.surface_type == SurfaceCard.SurfaceType["MACRO_RCC"]:
            id = int(Surface.surface_id)
            
            vector = [Surface.surface_coefficients[3],Surface.surface_coefficients[4],Surface.surface_coefficients[5]]
            new_surf_list, cell_description = self.__macro_rcc_cylinder_arbitrary(Surface,vector)

        elif Surface.surface_type == SurfaceCard.SurfaceType["MACRO_BOX"]:

            id = int(Surface.surface_id)
            
            origin = [Surface.surface_coefficients[0], Surface.surface_coefficients[1], Surface.surface_coefficients[2]]

            vec1 = [Surface.surface_coefficients[3], Surface.surface_coefficients[4], Surface.surface_coefficients[5]]
            vec2 = [Surface.surface_coefficients[6], Surface.surface_coefficients[7], Surface.surface_coefficients[8]]
            vec3 = [Surface.surface_coefficients[9], Surface.surface_coefficients[10], Surface.surface_coefficients[11]]

            vec1n = vec1/np.norm(vec1)
            vec2n = vec2/np.norm(vec2)
            vec3n = vec3/np.norm(vec3)

            d1 = vec1n[0]*origin[0] + vec1n[1]*origin[1] + vec1n[2]*origin[2] 
            d2 = vec1n[0]*(origin[0] + vec1[0]) + vec1n[1]*(origin[1]+vec1[1]) + vec1n[2]*(origin[2]+vec1[2])
            d3 = vec2n[0]*origin[0] + vec2n[1]*origin[1] + vec2n[2]*origin[2]
            d4 = vec2n[0]*(origin[0] + vec2[0]) + vec2n[1]*(origin[1]+vec2[1]) + vec2n[2]*(origin[2]+vec2[2])
            d5 = vec3n[0]*origin[0] + vec3n[1]*origin[1] + vec3n[2]*origin[2]
            d6 = vec3n[0]*(origin[0] + vec3[0]) + vec3n[1]*(origin[1]+vec3[1]) + vec3n[2]*(origin[2]+vec3[2])

            
            # cannonical facet ordering is done such that the surfaces
            # making up the macrobody all point inwards
            p1 = self.__make_new_plane(vec1n,d2)
            p2 = self.__make_new_plane(-1.0*vec1n,-1*d1)

            p3 = self.__make_new_plane(vec2n,d4)
            p4 = self.__make_new_plane(-1.0*vec2n,-1*d3)

            p5 = self.__make_new_plane(vec3n,d6)
            p6 = self.__make_new_plane(-1.0*vec3n,-1*d5)

            new_surf_list = [p1,p2,p3,p4,p5,p6]

            cell_description_inside = "("
            cell_description_inside += " -" + str(new_surf_list[0].surface_id)
            cell_description_inside += " -" + str(new_surf_list[1].surface_id)
            cell_description_inside += " -" + str(new_surf_list[2].surface_id)
            cell_description_inside += " -" + str(new_surf_list[3].surface_id)
            cell_description_inside += " -" + str(new_surf_list[4].surface_id)
            cell_description_inside += " -" + str(new_surf_list[5].surface_id)          
            cell_description_inside += ")"

            cell_description_outside = "("
            cell_description_outside += " "  + str(new_surf_list[0].surface_id)
            cell_description_outside += ":" + str(new_surf_list[1].surface_id)
            cell_description_outside += ":"  + str(new_surf_list[2].surface_id)
            cell_description_outside += ":" + str(new_surf_list[3].surface_id)
            cell_description_outside += ":"  + str(new_surf_list[4].surface_id)
            cell_description_outside += ":" + str(new_surf_list[5].surface_id)          
            cell_description_outside += ")"
            
            cell_description = [cell_description_inside,cell_description_outside]
        else:
            warnings.warn('Found an unsupported macrobody, files will not be correct',Warning)
            cell_description = ["",""]
            
        return cell_description, new_surf_list

    # if we find a macrobody in the surface list 
    # explode it into a surface based definition
    def __flatten_macrobodies(self):
        # look through the list until we find
        # a macrobody
        to_remove = []

        logging.debug("%s ", "Flattening macrobodies")

        for surf in self.surface_list:
            # if we are a macrobody
            if surf.is_macrobody():
                logging.debug("%s %i %s", "Surface",surf.surface_id,"is a macrobody")
                # explode into constituent surfaces
                cell_description, new_surfaces = self.explode_macrobody(surf)
                # if macro surface has transform apply it to new surfaces
                if surf.surface_transform != 0:
                    for surface in new_surfaces:
                        surface.surface_transform = surf.surface_transform

                # insert the new surfaces into the surface_list
                self.surface_list.extend(new_surfaces)
                # remove the old surface
                logging.debug("%s %i %s", "Surface",surf.surface_id,"is to be deleted")
                to_remove.append(surf)

                # update the cell definition - loop over all cells
                for jdx, cell in enumerate(self.cell_list):
                    while True:
                        # cell text description is contually updated
                        cell_text_description = cell.cell_text_description
                        
                        # if we find the surface id of the macrobdy in the text description
                        sub = str(surf.surface_id)
                        regex = re.compile("^-?("+str(surf.surface_id)+")(\.+[1-9])?$")
                        matches = [m.group(0) for l in cell_text_description for m in [regex.search(l)] if m]
                        #if str(surf.surface_id) in cell_text_description or str(surf.surface_id)+"." in cell_text_description:
                        
                        if matches:                       
                            # loop over each component and find the macrobody
                            for idx, surface in enumerate(cell.cell_text_description):
                                # if it matches we have the simmple form
                                if str(surf.surface_id) == surface:
                                    # replace it
                                    cell.cell_text_description[idx] = cell_description[1]
                                elif "-"+str(surf.surface_id) == surface:
                                    cell.cell_text_description[idx] = cell_description[0]
                   
                                # else we have the facet form
                                if str(surf.surface_id)+"." in surface:                                    
                                    surface_index = int(surface.split(".")[1]) # get just the mcnp surface index
                                    new_surface_id = new_surfaces[surface_index-1].surface_id # mcnp numbers them 1->n
                                    if "-" in surface: # need to take care of the -sign
                                        cell.cell_text_description[idx] = "-"+str(new_surface_id)
                                    else:
                                        cell.cell_text_description[idx] = str(new_surface_id)
                        else:
                            break
                    # update the text description
                    text_string = ' '.join(cell.cell_text_description)
                    self.cell_list[jdx].update(text_string)
                
        # clear up removed surfaces
        logging.debug("%s", "Deleting macrobody surfaces")
        for surf in to_remove:
            logging.debug("%s %i", "Deleting surface", surf.surface_id)
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
        cell_part = cell.cell_interpreted[:pos]
        
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
            # this relies upon us checking correctly for all other
            # cases where there may be blank lines due to our 
            # processing of the string
            if cell_line.isspace():
                logging.info('%s',"found end of cell cards at line " + str(idx))
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
                    cell_comment = self.file_lines[jdx][pos_comment:] # set the comment 
                    self.file_lines[jdx] = cell_line # update the file data
                    
                # mcnp continue line is indicated by 5 spaces
                if cell_line[0:5] == "     " and not cell_line.isspace():
                    card_line += cell_line
                # we have found a $comment line with nothing before it
                elif cell_line.isspace() and cell_comment:
                    print(cell_line,cell_comment, cell_line.isspace(), cell_comment.isspace())
                    pass
                else: # else we have found a new cell card
                    logging.debug("%s\n", "Found new cell card " + card_line)
                    cellcard = MCNPCellCard(card_line)
                    # we should set the comment here
                    self.cell_list.append(cellcard)
                    break 
                jdx += 1
            idx = jdx                   
        return idx

    # set the boundary conditions
    def __apply_boundary_conditions(self):
        
        # apply the importances to cells 
        if len(self.importance_list) != 0:
            # TODO make this loop apply to multiple particle
            # types but for now just do neutrons
            if len(self.importance_list[ParticleNames["NEUTRON"]]) != 0:
                importances = self.importance_list[ParticleNames["NEUTRON"]].split()
                for idx,value in enumerate(importances):
                    self.cell_list[idx].cell_importance = float(value)

        # loop over the cells and if the cell has 
        # importance 0, all the sufaces get boundary
        # condition 
        for cell in self.cell_list: 
            if cell.cell_importance == 0:
                for surf in cell.cell_surface_list:
                    self.get_surface_with_id(surf).boundary_condition = SurfaceCard.BoundaryCondition["VACUUM"]
        return

    # extract all the surface cards from the input deck
    def __get_surface_cards(self,idx):
        while True:
            surf_line = strip_dollar_comments(self.file_lines[idx])
            if surf_line.isspace():
                logging.debug('%s',"found end of cell cards at line " + str(idx))
                idx += 1
                break

            surf_card = surf_line
            jdx = idx + 1
            # scan until we are all done
            while True:
                surf_line = strip_dollar_comments(self.file_lines[jdx])
                # mcnp continue line is indicated by 5 spaces
                if surf_line[0:5] == "     " and not surf_line.isspace():
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

        # try to get importances defined in the data block
        self.__get_importances(idx)  
        # try to get weights defined the data block
        self.__get_weight_windows(idx)

        self.__get_transform_cards(idx)
        self.__get_material_cards(idx)
        # need to flatten first to get transformed surface in the 
        # correct place 
        self.__flatten_macrobodies()
        self.__explode_nots()

        self.__apply_surface_transformations()
        self.__apply_universe_transformations()
        # materials in other codes are tie their composition
        # and density together - need to make new material cards
        # based on the mateiral number / density pairs
        # and update cells accordingly.
        self.__reorganise_materials()
        # we need to turn macrobodies into regular surface descriptions

        self.__apply_boundary_conditions() # must be done after explode & flatten

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
        
    
