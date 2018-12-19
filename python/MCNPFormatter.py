#/usr/env/python3

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