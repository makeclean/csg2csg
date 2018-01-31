from SurfaceCard import SurfaceCard
from Vector import add,subtract,cross

# NOTES: Right now Cones are stored in the MCNP form - x y z R2

# function to determine if the card is a surface
# card or not
def is_surface_card(line):
    # tokenise the line
    surface_card = line.split()
    if len(surface_card) == 0 or surface_card[0] == "\n":
        return False
    print(surface_card)
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

# write the mcnp form of an arbitrary sphere
def mcnp_gq(SurfaceCard):
    string = "gq "
    string += str(SurfaceCard.surface_coefficients[0]) + " "
    string += str(SurfaceCard.surface_coefficients[1]) + " "
    string += str(SurfaceCard.surface_coefficients[2]) + "\n      "
    string += str(SurfaceCard.surface_coefficients[3]) + " "
    string += str(SurfaceCard.surface_coefficients[4]) + " "
    string += str(SurfaceCard.surface_coefficients[5]) + "\n      "
    string += str(SurfaceCard.surface_coefficients[6]) + " "
    string += str(SurfaceCard.surface_coefficients[7]) + " "
    string += str(SurfaceCard.surface_coefficients[8]) + "\n      "
    string += str(SurfaceCard.surface_coefficients[9]) + "\n"
    return string

# generic write method
def write_mcnp_surface(filestream, SurfaceCard):
    
    string = str(SurfaceCard.surface_id) + " "
    
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
    else:
        string += "Unknown surface type"
        
    filestream.write(string)
    
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
                            "gq","sq"]
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

            # floatify
            a = [float(i) for i in a]
            b = [float(i) for i in b]
            c = [float(i) for i in c]
            # form basis vectors
            v1 = subtract(a,b)
            v2 = subtract(c,b)
            # get normal
            norm = cross(v1,v2)
            # determine offset using point
            d = 0
            d += norm[0]*a[0]
            d += norm[1]*a[1]
            d += norm[2]*a[2]

            # define the equation of plane
            coords[0] = norm[0]
            coords[1] = norm[1]
            coords[2] = norm[2]
            coords[3] = -d
            
            # determine plane by 3 sets of xyz coords
        elif len(surface["coefficients"]) == 4:
            coords[0] = float(surface["coefficients"][0])
            coords[1] = float(surface["coefficients"][1])
            coords[2] = float(surface["coefficients"][2])
            coords[3] = float(surface["coefficients"][3])
        else:
             print("surface with id " + surface["id"],surface["transform"] + " does not have \
             enough coefficients")
             sys.exit(1)     
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
        elif "box" in surf_type:
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
        tokens = self.text_string.split()

        surface = {}                
        surface["id"] = int(tokens[0])
        print (surface["id"])

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

            
