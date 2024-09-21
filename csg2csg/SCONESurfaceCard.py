#!/usr/env/python3

from csg2csg.SurfaceCard import SurfaceCard
from math import sqrt, atan, degrees

# write the general form of a plane
def scone_plane_string(SurfaceCard):
    string = " plane; coeffs ( " 
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + "); } \n"
    return string


# write the specific x form of the plane
def scone_plane_x_string(SurfaceCard):
    string = " xPlane; x0 " + str(SurfaceCard.surface_coefficients[3]) 
    string += "; } \n"
    return string


# write the specific y form of the plane
def scone_plane_y_string(SurfaceCard):
    string = " yPlane; y0 " + str(SurfaceCard.surface_coefficients[3])
    string += "; } \n"
    return string


# write the specific z form of the plane
def scone_plane_z_string(SurfaceCard):
    string = " zPlane; z0 " + str(SurfaceCard.surface_coefficients[3])
    string += "; } \n"
    return string


# write a cylinder_x
def scone_cylinder_x(SurfaceCard):
    string = " xCylinder; radius " + str(SurfaceCard.surface_coefficients[0])
    string += "; origin ( 0.0 " + str(SurfaceCard.surface_coefficients[1])
    string += " " + str(SurfaceCard.surface_coefficients[2]) + "); } \n"
    return string


# write a cylinder_y
def scone_cylinder_y(SurfaceCard):
    string = " yCylinder; radius " + str(SurfaceCard.surface_coefficients[0])
    string += "; origin (" + str(SurfaceCard.surface_coefficients[1]) + " 0 "
    string += str(SurfaceCard.surface_coefficients[2]) + "); } \n"
    return string


# write a cylinder_z
def scone_cylinder_z(SurfaceCard):
    string = " zCylinder; radius " + str(SurfaceCard.surface_coefficients[0])
    string += "; origin (" + str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " 0); } \n"
    return string


# write a sphere
def scone_sphere(SurfaceCard):
    string = " sphere; origin (" + str(SurfaceCard.surface_coefficients[0])
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + "); radius "
    string += str(SurfaceCard.surface_coefficients[3]) + "; } \n"
    return string


# write a general quadratic
def scone_gq(SurfaceCard):
    string = " quadric; coeffs ( "
    for coefficient in SurfaceCard.surface_coefficients:
        string += " " + str(coefficient) + " "
    string += "); } \n"
    return string


def scone_cone_x(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    t2 = SurfaceCard.surface_coefficients[3]
    sign = SurfaceCard.surface_coefficients[4]

    # Do trigonometry to convert mcnp tangent squared, t2, into 
    # angle and determine hMin and hMax.
    # If sign is negative, hMax = vertex = 0, hMin = -10E10
    # If sign is positive, hMin = vertex = 0, hMax = 10E10
    # A bit of a fudge for now.
    # Assume no truncation, like in MCNP
    if sign < 0:
        hMin = -1E10
        hMax = 0
    else:
        hMin = 0
        hMax = 1E10

    angle = math.degrees(math.atan(math.sqrt(t2)))

    string = " {} {:f} {:f} {:f} {}\n".format(
            " xCone; vertex (", x, y, z," ); ")
    string += "angle " + str(angle) + "; hMin " + str(hMin)
    string += "; hMax " + str(hMax) + "; } \n"

    return string


# scone a cone along y
def scone_cone_y(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    t2 = SurfaceCard.surface_coefficients[3]
    sign = SurfaceCard.surface_coefficients[4]

    # Do trigonometry to convert mcnp tangent squared, t2, into 
    # angle and determine hMin and hMax.
    # If sign is negative, hMax = vertex = 0, hMin = -10E10
    # If sign is positive, hMin = vertex = 0, hMax = 10E10
    # A bit of a fudge for now.
    # Assume no truncation, like in MCNP
    if sign < 0:
        hMin = -1E10
        hMax = 0
    else:
        hMin = 0
        hMax = 1E10

    angle = math.degrees(math.atan(math.sqrt(t2)))

    string = " {} {:f} {:f} {:f} {}\n".format(
            " yCone; vertex (", x, y, z," ); ")
    string += "angle " + str(angle) + "; hMin " + str(hMin)
    string += "; hMax " + str(hMax) + "; } \n"

    return string


# scone a cone along z
def scone_cone_z(SurfaceCard):
    x = SurfaceCard.surface_coefficients[0]
    y = SurfaceCard.surface_coefficients[1]
    z = SurfaceCard.surface_coefficients[2]
    t2 = SurfaceCard.surface_coefficients[3]
    sign = SurfaceCard.surface_coefficients[4]

    # Do trigonometry to convert mcnp tangent squared, t2, into 
    # angle and determine hMin and hMax.
    # If sign is negative, hMax = vertex = 0, hMin = -10E10
    # If sign is positive, hMin = vertex = 0, hMax = 10E10
    # A bit of a fudge for now.
    # Assume no truncation, like in MCNP
    if sign < 0:
        hMin = -1E10
        hMax = 0
    else:
        hMin = 0
        hMax = 1E10

    angle = math.degrees(math.atan(math.sqrt(t2)))

    string = " {} {:f} {:f} {:f} {}\n".format(
            " zCone; vertex (", x, y, z," ); ")
    string += "angle " + str(angle) + "; hMin " + str(hMin)
    string += "; hMax " + str(hMax) + "; } \n"

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
def write_scone_surface(filestream, SurfaceCard):

    string = str(SurfaceCard.surface_id) + " { id "  
    string += str(SurfaceCard.surface_id) + "; type "

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
    elif SurfaceCard.surface_type is SurfaceCard.SurfaceType["GENERAL_QUADRATIC"]:
        string += scone_gq(SurfaceCard)
        filestream.write(string)
    else:
        filestream.write("surface not supported\n")
    
    return

