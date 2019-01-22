#/usr/env/python3

# given a string find a dollar comment '$' and
# return the string upto that point
def strip_dollar_comments(string):
    pos = string.find("$")
    if pos == -1:
        return string

    return string[0:pos]


# given a fortran formatted number return
# it as a float
def get_fortran_formatted_number(string):
    
    new_string = string.split(".")
    # now have something like [2][321455]
    if len(new_string) == 1 : # no decimal point
        return float(string)

    # its a normal number
    if any(item in new_string[1].lower() for item in ["e-", "e+","e"]):
        return float(string)

    # its some weird old style fortran formatted number
    new_string[1] = new_string[1].replace("-","e-")
    new_string[1] = new_string[1].replace("+","e+")
        
    return float(new_string[0]+"."+new_string[1])
    
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