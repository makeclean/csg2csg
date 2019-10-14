#/usr/env/python3

from csg2csg.CellCard import CellCard
from enum import Enum

from csg2csg.MCNPFormatter import mcnp_line_formatter, get_fortran_formatted_number

import re
import math

import logging

# to support more keywords for cells add them here
mcnp_cell_keywords = ["imp","u","fill","vol", "tmp"]

# if the string is a cell card or not
def is_cell_card(line):
    cell_card = line.split()
    if len(cell_card) == 0:
        return False
    try:
        if any(s == cell_card[0][0] for s in ['(',':',')','#']):
            return False
        else:
            if int(cell_card[0]):
                return True
    except ValueError:
        return False
    
    cellid = int(cell_card[0])
    mat_num = int(cell_card[1])
    if cellid and mat_num == 0:
        return True
    elif cellid > 0 and mat_num > 0:
        try:
            float(cell_card[2])
        except ValueError:
            print (cell_card[2]," cannot be converted to float")
        return True
    return False

# turn the generic operation type into a mcnp relevant text string
def mcnp_op_from_generic(Operation):
    # if we are not of type operator - we are string do nowt
    if not isinstance(Operation, CellCard.OperationType):
        if Operation is "(":
            return " "+Operation+" "
        elif Operation is ")":
            return " "+Operation+" "
        else:
            return Operation
    else:
        # otherwise we need to do something
        if Operation is CellCard.OperationType["NOT"]:
            string = " #"
        elif Operation is CellCard.OperationType["AND"]:
            string = "  "
        elif Operation is CellCard.OperationType["UNION"]:
            string = " : "
        else:
            string = "unknown operation"
    # return the operation
    return string

# write the cell card for a serpent cell given a generic cell card
def write_mcnp_cell(filestream, CellCard, print_importances = True):
    string = str(CellCard.cell_id) + " "
    
    string += str(CellCard.cell_material_number) + " "
    if CellCard.cell_material_number != 0:
        string += str(CellCard.cell_density) + " "

    string += " ( "
    
    # build the cell description
    for item in CellCard.cell_interpreted:
        string += mcnp_op_from_generic(item)

    # TODO make string no longer than 60 chars    
    string += " ) " 
    string += "\n"
    
    string = re.sub(" +"," ",string)
    string = string.strip()

    if CellCard.cell_universe != 0:
        string += " u=" + CellCard.cell_universe

    if CellCard.cell_fill != 0:
        string += " fill="+CellCard.cell_fill + " "
        if CellCard.cell_universe_offset != 0 or CellCard.cell_universe_rotation != 0:          
            # universe may have no traslation?
            string += "("
            if CellCard.cell_universe_offset != 0:
                for i in range(3):
                    string += str(CellCard.cell_universe_offset[i]) + " "
            else:
                string += " 0 0 0 "
    
            if CellCard.cell_universe_rotation != 0:
                for i in range(9):
                    value = float(CellCard.cell_universe_rotation[i])
                    #value = math.cos(value/180.*math.pi) 
                    string += str(value) + " "
            string += ")"
    
    if print_importances:
        string += " IMP:N=" + str(CellCard.cell_importance)

    string += "\n"
    string = mcnp_line_formatter(string)

    filestream.write(string)

class MCNPCellCard(CellCard):
    """ Class for the instanciation of generic cell cards
    from MCNP cell card strings
    """

    # constructor
    def __init__(self,card_string):
        CellCard.__init__(self,card_string)
        self.__interpret()

    # check the cell text description for parentheses
    # or not symbols these need extra work
    def __is_sanitised(self):
        if "#" in self.cell_text_description:
            return False
        elif "(" or ")" in self.cell_text_description:
            return False
        else:
            return True

    # method to break mcnp cell definition into something
    # a mere mortal can understand turns mcnp description
    # like 2 3 -4 into 2 AND 3 AND -4 or even 2 AND 3 AND 
    # +4
    def generalise(self):
        
        cell_description = self.cell_text_description
        # wholesale replace + signs as they are implicit
        # print(cell_description)
        # cell_description = [ s = "" for item in cell_description if item == "+"]
        cell_description = list(cell_description)
    
        idx = 0
        while True:
            s = cell_description[idx]
            if s is ":":
                cell_description[idx] = CellCard.OperationType["UNION"]
                idx += 1
                continue
            elif s is "#":
                cell_description[idx] = CellCard.OperationType["NOT"]
                idx += 1
                continue
            elif s is ("(" or  ")"):
                idx += 1
                continue
            elif isinstance(s,str) and cell_description[idx-1] is not "(" and cell_description[idx] is not ")":
                cell_description.insert(idx,CellCard.OperationType["AND"])
                idx += 1
                try:
                    surf_num = abs(int(s))
                    self.cell_surface_list.add(surf_num)
                except:
                    pass # its means it was a macrobody
                
            idx += 1
            if idx == len(cell_description): break

        self.cell_interpreted = cell_description  
        #print(self.cell_id) 
        #print(self.cell_interpreted) 
        #logging.debug("%s\n", "Generalised cell card " + ''.join([str(i) for i in self.cell_interpreted]))

        return

    # generally spaceify the text so that between each item
    # there is only one space i.e (7:8) becomes ( 7 : 8 )
    def __sanitise(self):
        text = self.cell_text_description
        return

    # given a valid keyword and string return the value of the
    # keyword
    def __get_keyword_value(self,keyword,string):
        #regex = re.regex=re.compile("("+keyword+") ?= ?[1-9][0-9]*") 
        regex = re.regex=re.compile("("+keyword+") ?= ?(?=.)([+-]?([0-9]*)(\.([0-9]+))?)")
        result = regex.search(string)[0]
        return result.split(" ")[2] #string[offset:end]  

    def __extract_string_between(self, string, first_substring, second_substring):
        #print(string, first_substring, second_substring,string.find(first_substring),string.find(second_substring))
        pos1 = string.find(first_substring) + 1
        pos2 = string.find(second_substring)
        result = ' '.join(string[pos1:pos2].split())

        if pos1 == -1:
            return ""
        return result

    # look through the string for the keywords 
    def __detect_keywords(self, keywords, string):
        
        # loop over the keywords and test
        found_keyword = False
        for word in keywords:
            if word in string:
                found_keyword = True
                break
        if not found_keyword:
            return string

        # 
        posd = string.find('$')
        if posd != -1:
            string = string[:posd]
            
        # otherwise loop through and find
        # u= , fill=, imp and tmp:
        posu = string.find("u")
        posf = string.find("fill")
        post = string.find("tmp")
   
        # universe fill angle could be specified in degrees
        rot_angle_degrees = False
        if string.find("*fill") != -1:
            rot_angle_degrees = True
            posf -= 1
        
        posi = string.find("imp")
        posv = string.find("vol")

        # find the posititon of the first match
        positions = [posu, posf, posi, posv, post]
        if posu != -1 or posf != -1 or posi != -1 or posv != -1 or post != -1:
            m = min(i for i in positions if i > 0)
        else:
            return string

        # from the point m to the end of the string, spacify between = signs
        # remove multiple whitespace such that we have "keyword = value"
        end_of_string = string[m:].replace("="," =")
        end_of_string = end_of_string.replace("=","= ")
        end_of_string = end_of_string.replace("  "," ")
        end_of_string += " "

        if posu == -1:
            self.cell_universe = 0
        else:
            self.cell_universe = self.__get_keyword_value('u',end_of_string)
            
        if posf == -1:
            self.cell_fill = 0
        else:
            self.cell_fill = self.__get_keyword_value('fill',end_of_string).strip()
            # if we have found fill, there may also be a rotation and translation
            # associated with the universe of the form (0 0 0)
            if '(' in string[posf:]:
                rot_trans = self.__extract_string_between(string[posf:],'(',')')
            else:
                rot_trans = "0"

            self.__set_universe_transform(rot_trans,rot_angle_degrees)
 
        if posi == -1:
            self.cell_importance = 1.
        else:
            self.cell_importance = float(self.__get_keyword_value('imp:n',end_of_string))

        # return the string upto the posisiotn of the first detected keyword          
        return string[:m]
    
    # populute the part CellCard into its
    # consituent parts
    def __interpret(self):

        string = self.text_string

        # look for mcnp cell specific keywords
        string = self.__detect_keywords(mcnp_cell_keywords,string)
        
        # this is to detect the presence of any importance
        # values only need one - used to indentify the
        # graveyard

        # expand the string first
        string = string.replace("(", " ( ")
        string = string.replace(")", " ) ")
        string = string.replace(":", " : ")
        string = string.replace("+","") # purge + signs

        # there can be mulitple comments per cell you sick sick people
        # why? is there any need? I mean really?!
        while '$' in string:
            pos = string.find('$')
            nl = string.find('\n',pos)
            string = string[:pos] + string[nl:]
            self.cell_comment += string[pos:nl]
        tokens = self.text_string.split()

        tokens = string.split()

        self.cell_id = int(tokens[0])
        material_number = int(tokens[1])
        if material_number > 0 :
            self.cell_material_number = int(material_number)
            self.cell_density = get_fortran_formatted_number(tokens[2])
            self.cell_text_description = tokens[3:]
        else:
            self.cell_density = 0.
            self.cell_material_number = 0
            self.cell_text_description = tokens[2:]
            
        # now interpret the cell text description
        if not self.__is_sanitised():
            self.__sanitise()
        self.generalise()

        return

    # set the universe transform 
    # angle
    def __set_universe_transform(self, transform, angle_form_degrees):
        tokens = transform.split()
        for idx,i in enumerate(tokens):
            tokens[idx] = i

        # transform is a TR card
        if len(tokens) == 1:
            self.cell_universe_transformation_id = tokens[0]
        elif len(tokens) > 2:
            # set the offset
            self.cell_universe_offset = [tokens[0],tokens[1],tokens[2]]
            if len(tokens) > 11:
                rot_angles = [tokens[3],tokens[4],tokens[5],tokens[6],tokens[7],tokens[8],tokens[9],tokens[10],tokens[11]]
                # cannonical storage format is in radians
                if angle_form_degrees:
                    for idx, angle in enumerate(rot_angles):
                        rot_angles[idx] = math.cos(float(angle)/180.*math.pi)
                self.cell_universe_rotation = rot_angles
        else:
            print('unknown method of transformation')
        return

    # apply the transform to the universe
    def apply_universe_transform(self,transform):
        self.cell_universe_offset = transform.shift # set the offset
        self.cell_universe_rotation = transform.v1 + transform.v2 + transform.v3
        # reset the transform
        self.cell_universe_transformation_id = "0"

    # update an existing cell description with 
    def update(self,new_cell_description):
        # take the new cell description and make a new 
        # cell description
        self.text_string = str(self.cell_id)
        self.text_string += " " + str(self.cell_material_number)
        if self.cell_material_number == 0:
            self.text_string += " " + new_cell_description
        else:
            self.text_string += " " + str(self.cell_density)
            self.text_string += " " + new_cell_description
        
        self.__interpret()
        
        