#!/usr/env/python3

from SurfaceCard import SurfaceCard

def serpent_plane_string(SurfaceCard):
    string = "surf " + str(SurfaceCard.surface_id)
    string += " plane " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

def serpent_plane_x_string(SurfaceCard):
    string = "surf " + str(SurfaceCard.surface_id)
    string += " px " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

def serpent_plane_y_string(SurfaceCard):
    string = "surf " + str(SurfaceCard.surface_id)
    string += " py " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

def serpent_plane_z_string(SurfaceCard):
    string = "surf " + str(SurfaceCard.surface_id)
    string += " pz " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

def serpent_cylinder_y(SurfaceCard):
    string = "surf " + str(SurfaceCard.surface_id)
    string += " cyly " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += "\n"
    return string


    

# write the surface description to file
def write_serpent_surface(filestream, SurfaceCard):
   # return {
   #     SurfaceCard.SurfaceType["PLANE_GENERAL"]: surface_plane_write(Surface,
   #     SurfaceCard.SurfaceType["CYLINDER_Y"]: "cylinder_y\n"
   #     }.get(SurfaceCard.surface_type,"surface not supported")

    
    if SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_GENERAL"]:
        string = serpent_plane_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_X"]:
        string = serpent_plane_x_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_Y"]:
        string = serpent_plane_y_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_Z"]:
        string = serpent_plane_z_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_Y"]:
        string = serpent_cylinder_y(SurfaceCard)
        filestream.write(string)
    else:
        filestream.write("surface not supported\n")
    return


class SerpentSurfaceCard(SurfaceCard):

    def __init__(self, card_string):
        SurfaceCard.__init__(self, card_string)

    def write(self):
        print ('hello')
