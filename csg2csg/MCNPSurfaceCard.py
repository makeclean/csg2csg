from csg2csg.SurfaceCard import SurfaceCard
from csg2csg.Vector import add,subtract,cross
from csg2csg.MCNPFormatter import mcnp_line_formatter

import numpy as np

# NOTES: Right now Cones are stored in the MCNP form - x y z R2

def boundary_condition(boundaryCondition):

    if boundaryCondition == SurfaceCard.BoundaryCondition["TRANSMISSION"]:
        boundary = ""
    if boundaryCondition == SurfaceCard.BoundaryCondition["VACUUM"]:
        boundary = ""
    if boundaryCondition == SurfaceCard.BoundaryCondition["REFLECTING"]:
        boundary = "*"
    if boundaryCondition == SurfaceCard.BoundaryCondition["WHITE"]:
        boundary = "+"

    return boundary

# function to determine if the card is a surface
# card or not
def is_surface_card(line):
    # tokenise the line
    surface_card = line.split()
    if len(surface_card) == 0 or surface_card[0] == "\n":
        return False
    # test if first item is an int
    try:
        int(surface_card[0])
    except TypeError:
        print (surface_card[0]," cannot be converted to float")
        return False

    # test if the second entry is an int
    try:
        int(surface_card[1])
        # then we are type with a transform
    except:
        # otherwise we are a normal surface type
        pass

    return True

# determine if surface has a transform or not
def surface_has_transform(line):
    # tokenise the line
    tokens = line.split()
    try:
        # try turning the second token into a float
        # since the line "1 2 PX" will convert
        # but 1 PX will fail 
        float(tokens[1])
    except:
        return False

    return True

# write the mcnp form of the general plane
def mcnp_plane_string(SurfaceCard):
    string = "p "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the mcnp form of the x plane
def mcnp_plane_x(SurfaceCard):
    string = "px "
    string += str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the mcnp form of the y plane
def mcnp_plane_y(SurfaceCard):
    string = "py "
    string += str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the mcnp form of the z plane
def mcnp_plane_z(SurfaceCard):
    string = "pz "
    string += str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the mcnp form of an cylinder aligned along the x axis
def mcnp_cylinder_x(SurfaceCard):
    string = "c/x "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + "\n"
    return string

# write the mcnp form of an cylinder aligned along the x axis
def mcnp_cylinder_y(SurfaceCard):
    string = "c/y "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + "\n"
    return string

# write the mcnp form of an cylinder aligned along the z axis
def mcnp_cylinder_z(SurfaceCard):
    string = "c/z "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + "\n"
    return string

# write the mcnp form of an cone aligned along the x axis
def mcnp_cone_x(SurfaceCard):
    string = "k/x "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + " " 
    string += str(SurfaceCard.surface_coefficients[4]) + "\n"
    return string

# write the mcnp form of an cone aligned along the y axis
def mcnp_cone_y(SurfaceCard):
    string = "k/y "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + " " 
    string += str(SurfaceCard.surface_coefficients[4]) + "\n"
    return string

# write the mcnp form of an cone aligned along the z axis
def mcnp_cone_z(SurfaceCard):
    string = "k/z "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + " "
    string += str(SurfaceCard.surface_coefficients[4]) + "\n"
    return string

# write the mcnp form of an arbitrary sphere
def mcnp_sphere(SurfaceCard):
    string = "s "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + "\n"
    return string

# write the mcnp form of an arbitrary gq
def mcnp_gq(SurfaceCard):
    string = "gq "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + " "
    string += str(SurfaceCard.surface_coefficients[4]) + " "
    string += str(SurfaceCard.surface_coefficients[5]) + " "
    string += str(SurfaceCard.surface_coefficients[6]) + " "
    string += str(SurfaceCard.surface_coefficients[7]) + " "
    string += str(SurfaceCard.surface_coefficients[8]) + " "
    string += str(SurfaceCard.surface_coefficients[9]) + "\n"
    return string

# write the mcnp form of an arbitrary sphere
def mcnp_tx(SurfaceCard):
    string = "tx "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + " "
    string += str(SurfaceCard.surface_coefficients[4]) + " "
    string += str(SurfaceCard.surface_coefficients[5]) + "\n"
    return string

def mcnp_ty(SurfaceCard):
    string = "ty "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + " "
    string += str(SurfaceCard.surface_coefficients[4]) + " "
    string += str(SurfaceCard.surface_coefficients[5]) + "\n"
    return string

def mcnp_tz(SurfaceCard):
    string = "tz "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + " "
    string += str(SurfaceCard.surface_coefficients[3]) + " "
    string += str(SurfaceCard.surface_coefficients[4]) + " "
    string += str(SurfaceCard.surface_coefficients[5]) + "\n"
    return string

# generic write method
def write_mcnp_surface(filestream, SurfaceCard):
    
    string = boundary_condition(SurfaceCard.boundary_condition)

    string += str(SurfaceCard.surface_id) + " "
    
    if SurfaceCard.surface_type == SurfaceCard.SurfaceType["PLANE_GENERAL"]:
        string += mcnp_plane_string(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["PLANE_X"]:
        string += mcnp_plane_x(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["PLANE_Y"]:
        string += mcnp_plane_y(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["PLANE_Z"]:
        string += mcnp_plane_z(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CYLINDER_X"]:
        string += mcnp_cylinder_x(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CYLINDER_Y"]:
        string += mcnp_cylinder_y(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CYLINDER_Z"]:
        string += mcnp_cylinder_z(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CONE_X"]:
        string += mcnp_cone_x(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CONE_Y"]:
        string += mcnp_cone_y(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["CONE_Z"]:
        string += mcnp_cone_z(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["SPHERE_GENERAL"]:
        string += mcnp_sphere(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["GENERAL_QUADRATIC"]:
        string += mcnp_gq(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["TORUS_X"]:
        string += mcnp_tx(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["TORUS_Y"]:
        string += mcnp_ty(SurfaceCard)
    elif SurfaceCard.surface_type == SurfaceCard.SurfaceType["TORUS_Z"]:
        string += mcnp_tz(SurfaceCard)
    else:
        string += "Unknown surface type"
        
    filestream.write(mcnp_line_formatter(string))
    
    return

class MCNPSurfaceCard(SurfaceCard):

    # TODO to add more surface definiitions, expand the list found
    # in __mcnp_surface types add the TLA for the surface, and
    # implement a __classify method, splitting on the basis of the
    # generic types - I prefer to have the types generalised e.g.
    # all planes to stored in the surface card as general planes
    
    # TODO add to this list to add more surface types
    __mcnp_surface_types = ["p","px","py","pz",
                            "s","so","sx","sy","sz",
                            "cx","cy","cz","c/x","c/y","c/z",
                            "kx","ky","kz","k/x","k/y","k/z",
                            "tx","ty","tz",
                            "gq","sq",
                            "x","y","z"]
    # TODO add to this list to add more macrobody types
    __mcnp_macro_types = ["rpp","box","sph","rcc"]

    verbosity = False
    
    # constructor
    def __init__(self,card_string, verbose = False):
        SurfaceCard.__init__(self,card_string)
        self.classify()

    # determine if the surface is infinite or a macrobody
    def __mcnp_type(self,surface):

        if any(surface["type"] in s for s in self.__mcnp_surface_types):
            return "infinite"
        elif any(surface["type"] in s for s in self.__mcnp_macro_types):
            return "macrobody"
        else:
            print ("surface type ", surface["type"] , " unknown")
            return "unknown"
        
    # classify planes along the xy or z axes
    def __classify_xyz_planes(self,surface):
        coords = [0.]*4
        # identify plane x
        if surface["type"] == "px":
            coords[0] = 1.
            coords[1] = 0.
            coords[2] = 0.
            coords[3] = float(surface["coefficients"][0])

            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["PLANE_X"],
                          coords)
        # identify plane y
        if surface["type"] == "py":
            coords[0] = 0.
            coords[1] = 1.
            coords[2] = 0.
            coords[3] = float(surface["coefficients"][0])

            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["PLANE_Y"],
                          coords)
        # idenfity plane z
        if surface["type"] == "pz":
            coords[0] = 0.
            coords[1] = 0.
            coords[2] = 1.
            coords[3] = float(surface["coefficients"][0])

            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["PLANE_Z"],
                          coords)
        return

    # classify general planes
    def __classify_general_planes(self,surface):
        coords = [0.]*4
        if len(surface["coefficients"]) == 9:
            
            a = [surface["coefficients"][0],
                 surface["coefficients"][1],
                 surface["coefficients"][2]]
            b = [surface["coefficients"][3],
                 surface["coefficients"][4],
                 surface["coefficients"][5]]
            c = [surface["coefficients"][6],
                 surface["coefficients"][7],
                 surface["coefficients"][8]]

            s = surface["coefficients"]
            s = [float(i) for i in s]

            order = [[0,1,2],
                     [1,2,0],
                     [2,0,1]]

            for i in range(3):
                j = order[i][1]
                k = order[i][2]
                coords[i] =  s[j]*(s[k+3] - s[k+6]) + s[j+3]*(s[k+6] - s[k]) \
                           + s[j+6]*(s[k] - s[k+3])
                coords[3] += s[i]*(s[j+3]*s[k+6] - s[j+6]*s[k+3])

            coeff = 0.
            for i in range(3,-1,-1):
                if coeff == 0. and coords[i] != 0.:
                    coeff = 1./coords[i]
                coords[i] *= coeff

            # determine plane by 3 sets of xyz coords
        elif len(surface["coefficients"]) == 4:
            coords[0] = float(surface["coefficients"][0])
            coords[1] = float(surface["coefficients"][1])
            coords[2] = float(surface["coefficients"][2])
            coords[3] = float(surface["coefficients"][3])
        else:
            print (surface["coefficients"])
            raise Exception('Surface with id {} does not have enough coefficents'.format(surface["id"]))
             
        self.set_type(surface["id"],surface["transform"],
                      SurfaceCard.SurfaceType["PLANE_GENERAL"],
                      coords)
        return

    # classify general sphere
    def __classify_general_sphere(self,surface):
        coords = [0.] * 4
        coords[0] = float(surface["coefficients"][0])
        coords[1] = float(surface["coefficients"][1])
        coords[2] = float(surface["coefficients"][2])
        coords[3] = float(surface["coefficients"][3])
        self.set_type(surface["id"],surface["transform"],
                      SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                      coords)
        return
    
    # classify sphere on the origin
    def __classify_origin_sphere(self,surface):
        coords = [0.] * 4
        coords[0] = 0.
        coords[1] = 0.
        coords[2] = 0.
        coords[3] = float(surface["coefficients"][0])
        self.set_type(surface["id"],surface["transform"],
                      SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                      coords)
        return
                          
    # classify spheres on x y or z axes
    def __classify_xyz_sphere(self,surface):
        coords = [0.]*4
        # identify sphere x
        if surface["type"] == "sx":
            coords[0] = float(surface["coefficients"][0])
            coords[1] = 0.
            coords[2] = 0.
            coords[3] = float(surface["coefficients"][1])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                          coords)
        # identify sphere y
        if surface["type"] == "sy":
            coords[0] = 0.
            coords[1] = float(surface["coefficients"][0])
            coords[2] = 0.
            coords[3] = float(surface["coefficients"][1])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                          coords)
        # idenfity sphere z
        if surface["type"] == "sz":
            coords[0] = 0.
            coords[1] = 0.
            coords[2] = float(surface["coefficients"][0])
            coords[3] = float(surface["coefficients"][1])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                          coords)
        return

    # identify cylinder parallel
    def __classify_cylinder_parallel(self, surface):
        coords = [0.] * 3
        if surface["type"] == "c/x":
            coords[0] = float(surface["coefficients"][0])
            coords[1] = float(surface["coefficients"][1])
            coords[2] = float(surface["coefficients"][2])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CYLINDER_X"],
                          coords)
        if surface["type"] == "c/y":
            coords[0] = float(surface["coefficients"][0])
            coords[1] = float(surface["coefficients"][1])
            coords[2] = float(surface["coefficients"][2])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CYLINDER_Y"],
                          coords)
        if surface["type"] == "c/z":
            coords[0] = float(surface["coefficients"][0])
            coords[1] = float(surface["coefficients"][1])
            coords[2] = float(surface["coefficients"][2])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CYLINDER_Z"],
                          coords)
        return

    # classify as cylinder lying on an axis
    def __classify_cylinder_on_axis(self, surface):
        coords = [0.] * 3
        if surface["type"] == "cx":
            coords[0] = 0.
            coords[1] = 0.
            coords[2] = float(surface["coefficients"][0])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CYLINDER_X"],
                          coords)
        if surface["type"] == "cy":
            coords[0] = 0.
            coords[1] = 0.
            coords[2] = float(surface["coefficients"][0])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CYLINDER_Y"],
                          coords)
        if surface["type"] == "cz":
            coords[0] = 0.
            coords[1] = 0.
            coords[2] = float(surface["coefficients"][0])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CYLINDER_Z"],
                          coords)
        return

    # classify cylinder off axis
    def __classify_cone_parallel(self, surface):
        coords = [0.] * 5
        coords[0] = float(surface["coefficients"][0])
        coords[1] = float(surface["coefficients"][1])
        coords[2] = float(surface["coefficients"][2])
        coords[3] = float(surface["coefficients"][3])
        # this picks up if we have a -1 specified or not
        if len(surface["coefficients"]) == 5:
            coords[4] = float(surface["coefficients"][4])

        if surface["type"] == "k/x":
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CONE_X"],
                          coords)
        if surface["type"] == "k/y":
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CONE_Y"],
                          coords)
        if surface["type"] == "k/z":
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CONE_Z"],
                          coords)
        return

    # classify surface as a cone
    def __classify_cone_on_axis(self, surface):
        coords = [0.] * 5
        if surface["type"] == "kx":
            coords[0] = float(surface["coefficients"][0])
            coords[1] = 0.
            coords[2] = 0.
            coords[3] = float(surface["coefficients"][1])
            # this picks up if we have a -1 specified or not
            if len(surface["coefficients"]) == 3:
                coords[4] = float(surface["coefficients"][2])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CONE_X"],
                          coords)
        if surface["type"] == "ky":
            coords[0] = 0.
            coords[1] = float(surface["coefficients"][0])
            coords[2] = 0.
            coords[3] = float(surface["coefficients"][1])
            # this picks up if we have a -1 specified or not
            if len(surface["coefficients"]) == 3:
                coords[4] = float(surface["coefficients"][2])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CONE_Y"],
                          coords)
        if surface["type"] == "kz":
            coords[0] = 0.
            coords[1] = 0.
            coords[2] = float(surface["coefficients"][0])
            coords[3] = float(surface["coefficients"][1])
            # this picks up if we have a -1 specified or not
            if len(surface["coefficients"]) == 3:
                coords[4] = float(surface["coefficients"][2])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["CONE_Z"],
                          coords)
        return

    def __classify_gq(self, surface):
        coords = [0.] * 10

        if surface["type"] == "gq":
            for i in range(10):
                coords[i] = float(surface["coefficients"][i])
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["GENERAL_QUADRATIC"],
                          coords)
        elif surface["type"] == "sq":
            a = float(surface["coefficients"][0])
            b = float(surface["coefficients"][1])
            c = float(surface["coefficients"][2])

            d = float(surface["coefficients"][3])
            e = float(surface["coefficients"][4])
            f = float(surface["coefficients"][5])

            x_bar = float(surface["coefficients"][7])
            y_bar = float(surface["coefficients"][8])
            z_bar = float(surface["coefficients"][9])

            g = (2*d) - (2*a*x_bar)
            h = (2*e) - (2*b*y_bar)
            j = (2*f) - (2*c*z_bar)

            k = (a*(x_bar**2)) + (b*(y_bar**2)) + (c*(z_bar**2)) - (2*d*x_bar) - (2*e*y_bar) - (2*f*z_bar) + float(surface["coefficients"][6])
            
            coords[0] = a
            coords[1] = b
            coords[2] = c
            coords[3] = 0.
            coords[4] = 0.
            coords[5] = 0.
            coords[6] = g
            coords[7] = h
            coords[8] = j
            coords[9] = k
                                    
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["GENERAL_QUADRATIC"],
                          coords)
            
        return

    # classify as torus
    def __classify_torus(self,surface):
        coords = [0.] * 6
        for i in range(6):
            coords[i] = float(surface["coefficients"][i])
        if surface["type"] == "tx":
            self.set_type(surface["id"], surface["transform"],
                          SurfaceCard.SurfaceType["TORUS_X"],
                          coords)
        if surface["type"] == "ty":
            self.set_type(surface["id"], surface["transform"],
                          SurfaceCard.SurfaceType["TORUS_Y"],
                          coords)
        if surface["type"] == "tz":
            self.set_type(surface["id"], surface["transform"],
                          SurfaceCard.SurfaceType["TORUS_Z"],
                          coords)
        return

    # classify as a box surface
    def __classify_box(self,surface):
        
        vx = float(surface["coefficients"][0])
        vy = float(surface["coefficients"][1])
        vz = float(surface["coefficients"][2])

        a1x = float(surface["coefficients"][3])
        a1y = float(surface["coefficients"][4])
        a1z = float(surface["coefficients"][5])

        a2x = float(surface["coefficients"][6])
        a2y = float(surface["coefficients"][7])
        a2z = float(surface["coefficients"][8])

        a3x = float(surface["coefficients"][9])
        a3y = float(surface["coefficients"][10])
        a3z = float(surface["coefficients"][11])

        # if this is true we can degenerate into a rpp type macrobody
        if a1y == 0. and a1z == 0. and a2x == 0. and a2z == 0. and a3x == 0. and a3y == 0.:
            coords = [0.]*6
            coords[0] = vx
            coords[1] = vx + a1x
            coords[2] = vy
            coords[3] = vy + a2y
            coords[4] = vz
            coords[5] = vz + a3z
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["MACRO_RPP"],
                          coords)
        # we cant, its aligned along some arbitrary axis
        else:
            coords = [0.]*12
            coords[0] = vx
            coords[1] = vy
            coords[2] = vz
            coords[3] = a1x
            coords[4] = a1y
            coords[5] = a1z
            coords[6] = a2x
            coords[7] = a2y
            coords[8] = a2z          
            coords[9] = a3x
            coords[10] = a3y
            coords[11] = a3z
            self.set_type(surface["id"],surface["transform"],
                          SurfaceCard.SurfaceType["MACRO_BOX"],
                          coords)          
        return

    # classify macrobody  as a sphere
    def __classify_sph(self,surface):
        coords = [0.] * 4
        coords[0] = float(surface["coefficients"][0])
        coords[1] = float(surface["coefficients"][1])
        coords[2] = float(surface["coefficients"][2])
        coords[3] = float(surface["coefficients"][3])
        self.set_type(surface["id"],surface["transform"],
                      SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                      coords)
        return

    # classify macrobody as a rpp
    def __classify_rpp(self,surface):
        coords = [0.]*6
        for i in range(6):
            coords[i] = float(surface["coefficients"][i])
        self.set_type(surface["id"],surface["transform"],
                      SurfaceCard.SurfaceType["MACRO_RPP"],
                      coords)
        return

    # classify macrobody as rcc
    def __classify_rcc(self,surface):
        coords = [0.] * 7
        for i in range(7):
            coords[i] = float(surface["coefficients"][i])
        self.set_type(surface["id"],surface["transform"],
                      SurfaceCard.SurfaceType["MACRO_RCC"],
                      coords)
        return

    def __define_edp_1coord(self,surface,coords,direction):
        return

    def __define_edp_2coord(self,surface,coords,direction):
        # plane
        if coords[0][0] == coords[1][0]:
            surface["coefficients"] = [coords[0][0]]
            surface["type"] = "p" + direction
            self.__classify_xyz_planes(surface)
        # cylinder
        elif coords[0][1] == coords[1][1]:
            surface["coefficients"] = [coords[0][1]]
            surface["type"] = "c" + direction
            self.__classify_cylinder_on_axis(surface)
        # cone
        else:
            # note coords are ri ri pairs
            dx = coords[1][1]-coords[0][1] 
            dy = coords[1][0]-coords[0][0] 

            grad = dy/dx
            offset = coords[1][0] - (grad*coords[1][1])

            angle = (-1/grad)**2

            # decide if we want the up or down part of the
            # cone since one sheet is used
            if grad < 0:
                up_or_down = -1
            else:
                up_or_down =  1

            surface["coefficients"] = [offset,angle,up_or_down]
            surface["type"] = "k"+direction            
            self.__classify_cone_on_axis(surface)

        return

    # classify edp surface
    def __classify_edp(self,surface):

        if len(surface["coefficients"]) == 2:
            coords = [float(surface["coefficients"][0]), float(surface["coefficients"][1])]

            if surface["type"] == "x":       
                self.__define_edp_1coord(surface,coords,"x")
            elif surface["type"] == "y":
                self.__define_edp_1coord(surface,coords,"y")
            elif surface["type"] == "z":
                self.__define_edp_1coord(surface,coords,"z")
            else:
                raise Exception('Could not determine surface type {}'.format(surface["type"]))

        elif len(surface["coefficients"]) == 4:
            coords1 = [float(surface["coefficients"][0]), float(surface["coefficients"][1])]
            coords2 = [float(surface["coefficients"][2]), float(surface["coefficients"][3])]

            coords = [coords1,coords2]

            if surface["type"] == "x":       
                self.__define_edp_2coord(surface,coords,"y")
            elif surface["type"] == "y":
                self.__define_edp_2coord(surface,coords,"y")
            elif surface["type"] == "z":
                self.__define_edp_2coord(surface,coords,"z")
            else:
                raise Exception('Could not determine surface type {}'.format(surface["type"]))

    # classify any inifinite surface
    def __classify_surface_types(self,surface):

        surf_id = surface["id"]
        surf_type = surface["type"]
               
        # classify surface types
        if "p" in surf_type and surf_type is "p":
            self.__classify_general_planes(surface)
        elif "p" in surf_type and surf_type is not "p":
            self.__classify_xyz_planes(surface)
        elif "s" in surf_type:
            if surf_type == "so":
                self.__classify_origin_sphere(surface)
            elif any(char in surf_type for char in ['x','y','z']):
                self.__classify_xyz_sphere(surface)
            elif "q" in surf_type:
                self.__classify_gq(surface) # this is intentional
            elif surf_type is "s":
                self.__classify_general_sphere(surface)
            else:
                print ("im a sphere that I dont understand")
        elif "c" in surf_type and "/" in surf_type:
            self.__classify_cylinder_parallel(surface)
        elif "c" in surf_type and "/" not in surf_type:
            self.__classify_cylinder_on_axis(surface)
        elif "k" in surf_type and "/" in surf_type:
            self.__classify_cone_parallel(surface)
        elif "k" in surf_type and "/" not in surf_type:
            self.__classify_cone_on_axis(surface)
        elif "g" in surf_type and "q" in surf_type:
            self.__classify_gq(surface)
        elif "t" in surf_type and any(s in surf_type for s in ["x","y","z"]):
            self.__classify_torus(surface)
        elif "box" in surf_type:
            self.__classify_box(surface)
        elif "rpp" in surf_type:
            self.__classify_rpp(surface)
        elif "sph" in surf_type:
            self.__classify_sph(surface)
        elif "rcc" in surf_type:
            self.__classify_rcc(surface)
        elif "x" or "y" or "z" in surf_type:
            self.__classify_edp(surface)
        else:
            raise Exception('Could not classify surface type {}'.format(surf_type))

    # classify any inifinite surface
    def __classify_macrobody_types(self,surface):

        surf_id = surface["id"]
        surf_type = surface["type"]
        
        if "box" in surf_type:
            self.__classify_box(surface)
        elif "rpp" in surf_type:
            self.__classify_rpp(surface)
        elif "sph" in surf_type:
            self.__classify_sph(surface)
        elif "rcc" in surf_type:
            self.__classify_rcc(surface)
        else:
            print ("Could not classify surface")
            sys.exit(1)
            
        # TODO add more logic one for each surface type        
        return

    # classify the surface type
    def classify(self):
        # first extract $ comment
        if "$" in self.text_string:
            pos = self.text_string.find("$")
            #its possible that the comment is in the middle of 
            # concatenated lines
            self.comment = self.text_string[pos:]
            self.text_string = self.text_string[0:pos]          
        
        tokens = self.text_string.split()

        surface = {}    
        if ("*" in tokens[0]):
            surface["id"] = int(tokens[0].replace("*",""))
            surface["boundary_condition"] = SurfaceCard.BoundaryCondition["REFLECTING"]
        else:            
            surface["id"] = int(tokens[0])

        if surface_has_transform(self.text_string):
            surface["transform"] = tokens[1]
            surface["type"] = tokens[2]
            surface["coefficients"] = tokens[3:]
        else:
            surface["transform"] = 0
            surface["type"] = tokens[1]
            surface["coefficients"] = tokens[2:]
        
        if self.__mcnp_type(surface) == "infinite":
            self.__classify_surface_types(surface)
        elif self.__mcnp_type(surface) == "macrobody":
            self.__classify_macrobody_types(surface)
        else:
            print("unknown type")     

    # apply the transform to the surface
    def transform(self, MCNPTransform):
        # do nothing if needs be
        if self.surface_transform == 0:
            return

        a = self.surface_coefficients[0]
        b = self.surface_coefficients[1]
        c = self.surface_coefficients[2]
        d = self.surface_coefficients[3]
        e = self.surface_coefficients[4]
        f = self.surface_coefficients[5]
        g = self.surface_coefficients[6]
        h = self.surface_coefficients[7]
        j = self.surface_coefficients[8]
        k = self.surface_coefficients[9]

        A = [[k,   g/2, h/2, j/2],
            [g/2,  a,   d/2, f/2],
            [h/2,  d/2, b,   e/2],
            [j/2,  f/2, e/2, c]]

        dx = -MCNPTransform.shift[0]
        dy = -MCNPTransform.shift[1]
        dz = -MCNPTransform.shift[2]

        # form the b matrix
        b1 = MCNPTransform.v1[0]
        b2 = MCNPTransform.v1[1]
        b3 = MCNPTransform.v1[2]
        b4 = MCNPTransform.v2[0]
        b5 = MCNPTransform.v2[1]
        b6 = MCNPTransform.v2[2]
        b7 = MCNPTransform.v3[0]
        b8 = MCNPTransform.v3[1]
        b9 = MCNPTransform.v3[2]

        # set the translate to 0
        dx = 0 
        dy = 0
        dz = 0

        trf = [[1,0,0,0], 
               [dx,b1,b2,b3],
               [dy,b4,b5,b6],
               [dz,b7,b8,b9]]

        # first do rotation
        tmp = np.matmul(A,trf)
        tmpr = np.matmul(np.transpose(trf),tmp)

        # now do translation
        dx = -MCNPTransform.shift[0]
        dy = -MCNPTransform.shift[1]
        dz = -MCNPTransform.shift[2]

        trf = [[1,0,0,0], 
               [dx,1,0,0],
               [dy,0,1,0],
               [dz,0,0,1]]

        tmp = np.matmul(tmpr,trf)
        tmpr = np.matmul(np.transpose(trf),tmp)

        self.surface_coefficients[0] = tmpr[1][1]
        self.surface_coefficients[1] = tmpr[2][2]
        self.surface_coefficients[2] = tmpr[3][3]
        self.surface_coefficients[3] = tmpr[1][2] + tmpr[2][1]
        self.surface_coefficients[4] = tmpr[3][2] + tmpr[2][3]
        self.surface_coefficients[5] = tmpr[1][3] + tmpr[3][1]
        self.surface_coefficients[6] = tmpr[1][0] + tmpr[0][1]
        self.surface_coefficients[7] = tmpr[2][0] + tmpr[0][2]
        self.surface_coefficients[8] = tmpr[3][0] + tmpr[0][3]
        self.surface_coefficients[9] = tmpr[0][0] 

        return