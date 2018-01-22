#!/usr/env/python3

from SurfaceCard import SurfaceCard

# write the general form of a plane
def serpent_plane_string(SurfaceCard):
    string = " plane " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the specific x form of the plane
def serpent_plane_x_string(SurfaceCard):
    string = " px " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the specific y form of the plane
def serpent_plane_y_string(SurfaceCard):
    string = " py " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the specific z form of the plane
def serpent_plane_z_string(SurfaceCard):
    string = " pz " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write a cylinder_x
def serpent_cylinder_x(SurfaceCard):
    string = " cylx " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += "\n"
    return string

# write a cylinder_y
def serpent_cylinder_y(SurfaceCard):
    string = " cyly " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += "\n"
    return string

# write a cylinder_z
def serpent_cylinder_z(SurfaceCard):
    string = " cylz " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += "\n"
    return string

# write a sphere
def serpent_sphere(SurfaceCard):
    string = " sph " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3])
    string += "\n"
    return string

# write a general quadratic
def serpent_gq(SurfaceCard):
    string = " quadratic " 
    for coefficient in SurfaceCard.surface_coefficients:
        string += " " + str(coefficient) + " " 
    string += "\n"
    return string
  

# write the surface description to file
def write_serpent_surface(filestream, SurfaceCard):
   # NOTE this appears to be a nice way to get a pythonic case statement
   # is it equally ugly as below?
   # return {
   #     SurfaceCard.SurfaceType["PLANE_GENERAL"]: surface_plane_write(Surface,
   #     SurfaceCard.SurfaceType["CYLINDER_Y"]: "cylinder_y\n"
   #     }.get(SurfaceCard.surface_type,"surface not supported")

    string = "surf " + str(SurfaceCard.surface_id)

    if SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_GENERAL"]:
        string += serpent_plane_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_X"]:
        string += serpent_plane_x_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_Y"]:
        string += serpent_plane_y_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_Z"]:
        string += serpent_plane_z_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_X"]:
        string += serpent_cylinder_x(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_Y"]:
        string += serpent_cylinder_y(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_Z"]:
        string += serpent_cylinder_z(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["SPHERE_GENERAL"]:
        string += serpent_sphere(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["GENERAL_QUADRATIC"]:
        string += serpent_gq(SurfaceCard)
        filestream.write(string)
    else:
        filestream.write("surface not supported\n")
    return


class SerpentSurfaceCard(SurfaceCard):

    def __init__(self, card_string):
        SurfaceCard.__init__(self, card_string)

    def write(self):
        print ('hello')
