#!/usr/env/python3

from SurfaceCard import SurfaceCard
from math import sqrt

# write the general form of a plane
def fluka_plane_string(SurfaceCard):
    a = SurfaceCard.surface_coefficients[0]
    b = SurfaceCard.surface_coefficients[1]
    c = SurfaceCard.surface_coefficients[2]
    d = SurfaceCard.surface_coefficients[3]
    mag = a**2 + b**2 + c**2
    x_p = a*(a*0. + b*0. + c*0. + d) / mag
    y_p = b*(a*0. + b*0. + c*0. + d) / mag
    z_p = c*(a*0. + b*0. + c*0. + d) / mag
        
    string = "PLA S" + str(SurfaceCard.surface_id) + " "
    string += str(a) + " "
    string += str(b) + " "
    string += str(c) + " "
    string += str(x_p) + " "
    string += str(y_p) + " "
    string += str(z_p) + " "
    string +=  "\n"
    
    return string

# write the specific x form of the plane
def fluka_plane_x_string(SurfaceCard):
    string = "YZP S" + str(SurfaceCard.surface_id) + " " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the specific y form of the plane
def fluka_plane_y_string(SurfaceCard):
    string = "XZP S" + str(SurfaceCard.surface_id) + " " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the specific z form of the plane
def fluka_plane_z_string(SurfaceCard):
    string = "XYP S" + str(SurfaceCard.surface_id) + " " + str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write a cylinder_x
def fluka_cylinder_x(SurfaceCard):
    string = "XCC S" + str(SurfaceCard.surface_id) + " " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += "\n"
    return string

# write a cylinder_y
def fluka_cylinder_y(SurfaceCard):
    string = "YCC S" + str(SurfaceCard.surface_id) + " " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += "\n"
    return string

# write a cylinder_z
def fluka_cylinder_z(SurfaceCard):
    string = "ZCC S" + str(SurfaceCard.surface_id) + " " + str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += "\n"
    return string

# write a sphere
def fluka_sphere(SurfaceCard):
    string = "SPH S" + str(SurfaceCard.surface_id) + " " +  str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3])
    string += "\n"
    return string

# write a general quadratic
def fluka_gq(SurfaceCard):
    string = "QUA S" + str(SurfaceCard.surface_id)
    ax2 = SurfaceCard.surface_coefficients[0]
    by2 = SurfaceCard.surface_coefficients[1]
    cz2 = SurfaceCard.surface_coefficients[2]
    
    dxy = SurfaceCard.surface_coefficients[3]
    eyz = SurfaceCard.surface_coefficients[4]
    fzx = SurfaceCard.surface_coefficients[5]

    gx = SurfaceCard.surface_coefficients[6]
    hy = SurfaceCard.surface_coefficients[7]
    jz = SurfaceCard.surface_coefficients[8]

    k = SurfaceCard.surface_coefficients[9]

    string += " " + str(ax2) + " "
    string += " " + str(by2) + " "
    string += " " + str(cz2) + " "

    # fluka wants dxy fzx eyz 

    string += " " + str(dxy) + " "
    string += " " + str(fzx) + " "
    string += " " + str(eyz) + " "

    string += " " + str(gx) + " "
    string += " " + str(hy) + " "
    string += " " + str(jz) + " "

    string += " " + str(k) + " "
    
    string += "\n"
    return string

# its not clear how we deal with +-1 cones for fluka}
# write a cone along x
def fluka_cone_x(SurfaceCard):
    """
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
    """    

    # maybe use QUA instead? - meets the requirement of being
    # infinite surfaces allows for -1/+1/0
   
    # cone points down from xyz
    if SurfaceCard.surface_coefficients[4] == -1:
        x = SurfaceCard.b_box[0]
        h = abs(SurfaceCard.b_box[0]) + SurfaceCard.surface_coefficients[0]
    # cone points up from xyz
    if SurfaceCard.surface_coefficients[4] == 1:
        x = SurfaceCard.b_box[1]
        h = -1.*(SurfaceCard.b_box[1] - SurfaceCard.surface_coefficients[0])

    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    r = abs(h)*sqrt(SurfaceCard.surface_coefficients[3])

    # maybe change to use proper formatting statements
    string = "TRC S"+ str(SurfaceCard.surface_id) + " " + \
             str(x) + " " + str(y) + " " + str(z) + " " + \
             + str(h) + " 0. 0. " + str(r) + " 0.0\n" 

    return string

# fluka a cone along y
def fluka_cone_y(SurfaceCard):
    # cone points down from xyz
    if SurfaceCard.surface_coefficients[4] == -1:
        y = SurfaceCard.b_box[2]
        h = abs(SurfaceCard.b_box[2]) + SurfaceCard.surface_coefficients[1]
    # cone point up from xyz
    if SurfaceCard.surface_coefficients[4] == 1:
        y = SurfaceCard.b_box[3]
        h = -1.*(SurfaceCard.b_box[3] - SurfaceCard.surface_coefficients[1])

    x = SurfaceCard.surface_coefficients[0]
    z = SurfaceCard.surface_coefficients[2]
    r = abs(h)*sqrt(SurfaceCard.surface_coefficients[3])
    
    # maybe change to use proper formatting statements
    string = "TRC S"+ str(SurfaceCard.surface_id) + " " + \
             str(x) + " " + str(y) + " " + str(z) + " " + \
             "0. " + str(h) + " 0. " + str(r) + " 0.0\n" 
    
    return string

# fluka a cone along z
def fluka_cone_z(SurfaceCard):
    
    # cone points down from xyz
    if SurfaceCard.surface_coefficients[4] == -1:
        z = SurfaceCard.b_box[5] 
        h = abs(SurfaceCard.b_box[5]) + SurfaceCard.surface_coefficients[2])
    # cone point up from xyz
    if SurfaceCard.surface_coefficients[4] == 1:
        z = SurfaceCard.b_box[6]
        h = -1.*(SurfaceCard.b_box[6] - SurfaceCard.surface_coefficients[2])

    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    r = abs(h)*sqrt(SurfaceCard.surface_coefficients[3])

    # maybe change to use proper formatting statements
    string = "TRC S"+ str(SurfaceCard.surface_id) + " " + \
              str(x) + " " + str(y) + " " + str(z) + " " + \
              "0. 0. " + str(h) + " " + str(r) + " 0.0\n" 

    return string

# maybe add auto expand torus to cones?
# very few codes support tori due to numerical reasons
# have previously had success defining torus as sets of cones
#

# fluka a torus x
def fluka_torus_x(SurfaceCard):
    string = "Surface TORUS_X not supported" 
    return string

# fluka a torus y
def fluka_torus_y(SurfaceCard):
    string = "Surface TORUS_Y not supported"
    return string

# fluka a torus z
def fluka_torus_z(SurfaceCard):
    string = "Surface TORUS_Z not supported"
    return string


# write the surface description to file
def write_fluka_surface(filestream, SurfaceCard):
   # NOTE this appears to be a nice way to get a pythonic case statement
   # is it equally ugly as below?
   # return {
   #     SurfaceCard.SurfaceType["PLANE_GENERAL"]: surface_plane_write(Surface,
   #     SurfaceCard.SurfaceType["CYLINDER_Y"]: "cylinder_y\n"
   #     }.get(SurfaceCard.surface_type,"surface not supported")

    #string = "surf " + str(SurfaceCard.surface_id)
    string = "" 
    if SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_GENERAL"]:
        string += fluka_plane_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_X"]:
        string += fluka_plane_x_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_Y"]:
        string += fluka_plane_y_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["PLANE_Z"]:
        string += fluka_plane_z_string(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_X"]:
        string += fluka_cylinder_x(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_Y"]:
        string += fluka_cylinder_y(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CYLINDER_Z"]:
        string += fluka_cylinder_z(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["SPHERE_GENERAL"]:
        string += fluka_sphere(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CONE_X"]:
        string += fluka_cone_x(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CONE_Y"]:
        string += fluka_cone_y(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["CONE_Z"]:
        string += fluka_cone_z(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["TORUS_X"]:
        string += fluka_torus_x(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["TORUS_Y"]:
        string += fluka_torus_y(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["TORUS_Z"]:
        string += fluka_torus_z(SurfaceCard)
        filestream.write(string)
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["GENERAL_QUADRATIC"]:
        string += fluka_gq(SurfaceCard)
        filestream.write(string)
    else:
        filestream.write("surface not supported\n")
    return

# Surface Card Class
class FLUKASurfaceCard(SurfaceCard):
    def __init__(self, card_string):
        SurfaceCard.__init__(self, card_string)

    def write(self):
        print ('hello')
