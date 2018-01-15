from SurfaceCard import SurfaceCard

class MCNPSurfaceCard(SurfaceCard):

    # TODO to add more surface definiitions, expand the list found
    # in __mcnp_surface types add the TLA for the surface, and
    # implement a __classify method, splitting on the basis of the
    # generic types - I prefer to have the types generalised e.g.
    # all planes to stored in the surface card as general planes
    
    # TODO add to this list to add more surface types
    __mcnp_surface_types = ["p","px","py","pz",
                            "s","so","sx","sy","sz"]
    # TODO add to this list to add more macrobody types
    __mcnp_macro_types = ["rpp"]
    
    # constructor
    def __init__(self,card_string):
        SurfaceCard.__init__(self,card_string)

    # determine if the surface is infinite or a macrobody
    def __mcnp_type(self,surface):
        if any(surface["type"] in s for s in self.__mcnp_surface_types):
            return "infinite"
        elif any(surface["type"] in s for s in self.__mcnp_macro_types):
            return "macrobody"
        else:
            return "unknown"
        
    # classify planes along the xy or z axes
    def __classify_xyz_planes(self,surface):
        coords = [0.]*3
        # identify plane x
        if surface["type"] == "px":
            coords[0] = float(surface["coefficients"][0])
            coords[1] = 0.
            coords[2] = 0.
            self.set_type(surface["id"],
                          SurfaceCard.SurfaceType["PLANE_X"],
                          coords)
        # identify plane y
        if surface["type"] == "py":
            coords[0] = 0.
            coords[1] = float(surface["coefficients"][0])
            coords[2] = 0.
            self.set_type(surface["id"],
                          SurfaceCard.SurfaceType["PLANE_Y"],
                          coords)
        # idenfity plane z
        if surface["type"] == "pz":
            coords[0] = 0.
            coords[1] = 0.
            coords[2] = float(surface["coefficients"][0])
            self.set_type(surface["id"],
                          SurfaceCard.SurfaceType["PLANE_Z"],
                          coords)
        return

    # classify general planes
    def __classify_general_planes(self,surface):
        coords = [0.]*4
        coords[0] = float(surface["coefficients"][0])
        coords[1] = float(surface["coefficients"][1])
        coords[2] = float(surface["coefficients"][2])
        coords[3] = float(surface["coefficients"][3])
        self.set_type(surface["id"],
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
        self.set_type(surface["id"],
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
        self.set_type(surface["id"],
                      SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                      coords)
        return
                          
    # classify spheres on x y or z axes
    def __classify_xyz_spheres(self,surface):
        coords = [0.]*4
        # identify sphere x
        if surface["type"] == "sx":
            coords[0] = float(surface["coefficients"][0])
            coords[1] = 0.
            coords[2] = 0.
            coords[3] = float(surface["coefficients"][1])
            self.set_type(surface["id"],
                          SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                          coords)
        # identify sphere y
        if surface["type"] == "sy":
            coords[0] = 0.
            coords[1] = float(surface["coefficients"][0])
            coords[2] = 0.
            coords[4] = float(surface["coefficients"][1])
            self.set_type(surface["id"],
                          SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                          coords)
        # idenfity sphere z
        if surface["type"] == "sz":
            coords[0] = 0.
            coords[1] = 0.
            coords[2] = float(surface["coefficients"][0])
            coords[3] = float(surface["coefficients"][1])
            self.set_type(surface["id"],
                          SurfaceCard.SurfaceType["SPHERE_GENERAL"],
                          coords)
        return

                          
    # classify any inifinite surface
    def __classify_surface_types(self,surface):

        surf_id = surface["id"]
        surf_type = surface["type"]
               
        # classify surface types
        if "p" in surf_type and surf_type is "p":
            self.__classify_general_planes(surface)
        if "p" in surf_type and surf_type is not "p":
            self.__classify_xyz_planes(surface)
        if "s" in surf_type and surf_type is "s":
            self.__classify_general_sphere(surface)
        if "s" in surf_type and surf_type is "so":
            self.__classify_origin_sphere(surface)
        if "s" in surf_type and surf_type is not ("s" or "so"):
            self.__classifu_xyz_sphere(surface)
        # TODO add more logic one for each surface type        
        return

    # classify the surface type
    def classify(self):
        tokens = self.text_string.split()

        surface = {}                
        surface["id"] = int(tokens[0])
        surface["type"] = tokens[1]
        surface["coefficients"] = tokens[2:]

        if self.__mcnp_type(surface) == "infinite":
            self.__classify_surface_types(surface)
        elif self.mcnp_type(surface) == "macrobody":
            self.__classify_macrobody_type(surface)
        else:
            print("unknown type")

    # write the mcnp form of the general plane
    def __write_plane_general(self):
        string = ""
        string += str(self.surface_id) + " "
        string += "p "
        string += str(self.surface_coefficients[0]) + " "
        string += str(self.surface_coefficients[1]) + " "
        string += str(self.surface_coefficients[2]) + " "
        string += str(self.surface_coefficients[3]) + "\n"
        print (string)

    # generic write method
    def write(self):
        if self.surface_type == self.SurfaceType["PLANE_GENERAL"]:
            self.__write_plane_general()
            
