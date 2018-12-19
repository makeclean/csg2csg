#/usr/env/python3

from CellCard import CellCard
from enum import Enum

import re

# to support more keywords for cells add them here
mcnp_cell_keywords = ["imp","u","fill","vol"]

# take a massive string for an MCNP cell line 
# makes it no more than 80 chars wide and 
# include the right indentation
def mcnp_line_formatter(string_to_format):
    tmp_string = string_to_format
    # early return string already ok
    if(len(tmp_string) < 72 ):
        return tmp_string
    else:
        # need to loop until string is finished
        new_string = ""
        while True:
            # to do make line length an argument?
            if len(tmp_string) <= 72:
                if not tmp_string.isspace():
                    new_string += tmp_string
                break
            else:
                # need to not chop text without disturbing
                # underlying definition - find first space 
                # reverse search and split there 
                pos = tmp_string[:72].rfind(" ") 
                # todo - robustify this it must be possible for there
                # to be no space in the string             
                new_string += tmp_string[:pos] + "\n" 
                tmp_string = tmp_string[pos:]
                # if remaining string is empty just leave
                if tmp_string.isspace():
                    return new_string
                else:
                    # if we are continuing add spaces
                     new_string += "     "

    return new_string

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
def write_mcnp_cell(filestream, CellCard):
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
    # like 2 3 -4 into 2 AND 3 AND -4
    def generalise(self):
        
        cell_description = self.cell_text_description
        cell_description = list(cell_description)
    
        idx = 0
        while True:
            s = cell_description[idx]

            if s is ":":
                cell_description[idx] = CellCard.OperationType["UNION"]
                idx += 1
            elif s is "#":
                cell_description[idx] = CellCard.OperationType["NOT"]
                idx += 1
            elif s is ("(" or  ")"):
                idx += 1
                continue
            elif isinstance(s,str) and cell_description[idx-1] is not "(" and cell_description[idx] is not ")":
                cell_description.insert(idx,CellCard.OperationType["AND"])
                idx += 1
            idx += 1
            if idx == len(cell_description): break

        self.cell_interpreted = cell_description    
    
        return

    # generally spaceify the text so that between each item
    # there is only one space i.e (7:8) becomes ( 7 : 8 )
    def __sanitise(self):
        text = self.cell_text_description
        return

    # given a valid keyword and string return the value of the
    # keyword
    def __get_keyword_value(self,keyword,string):
        offset = len(keyword) + 3 
        offset += string.find(keyword,offset)
        end = string.find(" ",offset)
        return string[offset:end]  

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
        # u= , fill= and imp:
        posu = string.find("u")
        posf = string.find("fill")
        posi = string.find("imp")
        posv = string.find("vol")

        # find the posititon of the first match
        positions = [posu,posf,posi,posv]
        if posu != -1 or posf != -1 or posi != -1 or posv != -1:
            m = min(i for i in positions if i > 0)
        else:
            return string

        # from the point m to the end of the string, spacify between = signs
        # remove multiple whitespace such that we have "keyword = value"
        end_of_string = string[m:].replace("="," =")
        end_of_string = end_of_string.replace("=","= ")
        end_of_string = end_of_string.replace("  "," ")

        if posu == -1:
            self.cell_universe = 0
        else:
            self.cell_universe = self.__get_keyword_value('u',end_of_string)
            
        if posf == -1:
            self.cell_fill = 0
        else:
            self.cell_fill = self.__get_keyword_value('fill',end_of_string)
 
        if posi == -1:
            self.cell_importance = 0
        else:
            self.cell_importance = self.__get_keyword_value('imp',end_of_string)

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
            self.cell_density = float(tokens[2])
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
        
        