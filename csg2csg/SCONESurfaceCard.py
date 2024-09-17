#!/usr/env/python3

from csg2csg.SurfaceCard import SurfaceCard
from math import sqrt

# write the general form of a plane
def scone_plane_string(SurfaceCard):
    string = " plane; coeffs ( " 
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + "); "
    return string


# write the specific x form of the plane
def scone_plane_x_string(SurfaceCard):
    string = " xPlane; x0 " + str(SurfaceCard.surface_coefficients[3]) + ";"
    return string


# write the specific y form of the plane
def scone_plane_y_string(SurfaceCard):
    string = " yPlane; y0 " + str(SurfaceCard.surface_coefficients[3]) + ";"
    return string


# write the specific z form of the plane
def scone_plane_z_string(SurfaceCard):
    string = " zPlane; z0 " + str(SurfaceCard.surface_coefficients[3]) + ";"
    return string


# write a cylinder_x
def scone_cylinder_x(SurfaceCard):
    string = " xCylinder; radius " + str(SurfaceCard.surface_coefficients[0]) + "; "
    string += "origin ( 0.0 " + str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + "); "
    return string


# write a cylinder_y
def scone_cylinder_y(SurfaceCard):
    string = " yCylinder; radius " + str(SurfaceCard.surface_coefficients[0]) + "; "
    string += "origin (" + str(SurfaceCard.surface_coefficients[1]) + " 0 "
    string += str(SurfaceCard.surface_coefficients[2]) + "); "
    return string


# write a cylinder_z
def scone_cylinder_z(SurfaceCard):
    string = " zCylinder; radius " + str(SurfaceCard.surface_coefficients[0]) + "; "
    string += "origin (" + str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " 0); "
    return string


# write a sphere
def scone_sphere(SurfaceCard):
    string = " sphere; radius " + str(SurfaceCard.surface_coefficients[0]) + "; "
    string += "origin (" + str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + "); "
    return string


# write a general quadratic
def scone_gq(SurfaceCard):
    string = " quadratic "
    for coefficient in SurfaceCard.surface_coefficients:
        string += " " + str(coefficient) + " "
    string += "\n"
    return string


# its not clear how we deal with +-1 cones for serpent}
# write a cone along x - jaakko has implemented a special
# version for mcnp comparisons - ckx/y/z
def serpent_cone_x(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    r = SurfaceCard.surface_coefficients[3]

    if len(SurfaceCard.surface_coefficients) > 4:
        side = SurfaceCard.surface_coefficients[4]
        string = " {} {:f} {:f} {:f} {:f} {:f}\n".format("ckx", x, y, z, r, side)
    else:
        string = " {} {:f} {:f} {:f} {:f}\n".format("ckx", x, y, z, r)

    return string


# scone a cone along y
def scone_cone_y(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    r = SurfaceCard.surface_coefficients[3]

    if len(SurfaceCard.surface_coefficients) > 4:
        side = SurfaceCard.surface_coefficients[4]
        string = " {} {:f} {:f} {:f} {:f} {:f}\n".format("cky", x, y, z, r, side)
    else:
        string = " {} {:f} {:f} {:f} {:f}\n".format("cky", x, y, z, r)

    return string


# scone a cone along z
def scone_cone_z(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    r = SurfaceCard.surface_coefficients[3]

    if len(SurfaceCard.surface_coefficients) > 4:
        side = SurfaceCard.surface_coefficients[4]
        string = " {} {:f} {:f} {:f} {:f} {:f}\n".format("ckz", x, y, z, r, side)
    else:
        string = " {} {:f} {:f} {:f} {:f}\n".format("ckz", x, y, z, r)

    return string


# scone a torus x
def scone_torus_x(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    a = SurfaceCard.surface_coefficients[3]
    b = SurfaceCard.surface_coefficients[4]
    c = SurfaceCard.surface_coefficients[5]
    string = " {} {:f} {:f} {:f} {:f} {:f} {:f}\n".format("torx", x, y, z, a, b, c)
    return string


# scone a torus y
def scone_torus_y(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    a = SurfaceCard.surface_coefficients[3]
    b = SurfaceCard.surface_coefficients[4]
    c = SurfaceCard.surface_coefficients[5]
    string = " {} {:f} {:f} {:f} {:f} {:f} {:f}\n".format("tory", x, y, z, a, b, c)
    return string


# scone a torus z
def scone_torus_z(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    a = SurfaceCard.surface_coefficients[3]
    b = SurfaceCard.surface_coefficients[4]
    c = SurfaceCard.surface_coefficients[5]
    string = " {} {:f} {:f} {:f} {:f} {:f} {:f}\n".format("torz", x, y, z, a, b, c)
    return string


"""
# write a conex
def serpent_cone_x(SurfaceCard):
    
        mcnp xyz r2 -1 +1
        *
        ||
        | \
        |  \
        |   \
        |    \
        |     \
        *------*
        
    From the bounding coodinate appropriate in 
    this case - if pointing down need the lowest value
        
    
    # cone points down from xyz
    if SurfaceCard.surface_coefficients[4] == -1:
        h = abs(SurfaceCard.b_box[0])
        x = SurfaceCard.b_box[0]
    # cone point up from xyz
    if SurfaceCard.surface_coefficients[4] == 1:
        h = abs(SurfaceCard.b_box[1])
        x = SurfaceCard.b_box[1]

    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    r = h*sqrt(SurfaceCard.surface_coefficients[3])

    string = ' {} {:f} {:f} {:f} {:f} {:f}'.format("conx",x,y,z,r,h)
  
    return string

# write a cone y
def serpent_cone_y(SurfaceCard):
    
        mcnp xyz r2 -1 +1
        *
        ||
        | \
        |  \
        |   \
        |    \
        |     \
        *------*
        
    From the bounding coodinate appropriate in 
    this case - if pointing down need the lowest value
        
    
    # cone points down from xyz
    if SurfaceCard.surface_coefficients[4] == -1:
        h = abs(SurfaceCard.b_box[2])
        y = SurfaceCard.b_box[2]
    # cone point up from xyz
    if SurfaceCard.surface_coefficients[4] == 1:
        h = abs(SurfaceCard.b_box[3])
        y = SurfaceCard.b_box[3]

    x = SurfaceCard.surface_coefficients[0]
    z = SurfaceCard.surface_coefficients[2]
    r = h*sqrt(SurfaceCard.surface_coefficients[3])

    string = ' {} {:f} {:f} {:f} {:f} {:f}'.format("cony",x,y,z,r,h)
  
    return string

# write a cone z
def serpent_cone_z(SurfaceCard):
    
        mcnp xyz r2 -1 +1
        *
        ||
        | \
        |  \
        |   \
        |    \
        |     \
        *------*
        
    From the bounding coodinate appropriate in 
    this case - if pointing down need the lowest value
        
    
    # cone points down from xyz
    if SurfaceCard.surface_coefficients[4] == -1:
        h = abs(SurfaceCard.b_box[5])
        z = SurfaceCard.b_box[5]
    # cone point up from xyz
    if SurfaceCard.surface_coefficients[4] == 1:
        h = abs(SurfaceCard.b_box[6])
        z = SurfaceCard.b_box[6]

    x = SurfaceCard.surface_coefficients[0]
   y = SurfaceCard.surface_coefficients[1]
    r = h*sqrt(SurfaceCard.surface_coefficients[3])

  
    return string

"""

# write the surface description to file
def write_serpent_surface(filestream, SurfaceCard):
    # NOTE this appears to be a nice way to get a pythonic case statement
    # is it equally ugly as below?
    # return {
    #     SurfaceCard.SurfaceType["PLANE_GENERAL"]: surface_plane_write(Surface,
    #     SurfaceCard.SurfaceType["CYLINDER_Y"]: "cylinder_y\n"
    #     }.get(SurfaceCard.surface_type,"surface not supported")

    string = str(SurfaceCard.surface_id) + "{ id " + str(SurfaceCard.surface_id) + "; type "

    if SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_GENERAL"]:
        string += scone_plane_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_X"]:
        string += scone_plane_x_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_Y"]:
        string += scone_plane_y_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_Z"]:
        string += scone_plane_z_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_X"]:
        string += scone_cylinder_x(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_Y"]:
        string += scone_cylinder_y(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_Z"]:
        string += scone_cylinder_z(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["SPHERE_GENERAL"]:
        string += scone_sphere(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CONE_X"]:
        string += scone_cone_x(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CONE_Y"]:
        string += scone_cone_y(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CONE_Z"]:
        string += scone_cone_z(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["TORUS_X"]:
        string += scone_torus_x(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["TORUS_Y"]:
        string += scone_torus_y(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["TORUS_Z"]:
        string += scone_torus_z(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["GENERAL_QUADRATIC"]:
        string += scone_gq(SurfaceCard)
        filestream.write(string)
    else:
        filestream.write("surface not supported\n")
    
    string += " }\n"
    return


class SCONESurfaceCard(SurfaceCard):
    def __init__(self, card_string):
        SurfaceCard.__init__(self, card_string)

    def write(self):
        print("hello")
