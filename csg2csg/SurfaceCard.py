from csg2csg.Card import Card
from enum import Enum

import numpy as np

class SurfaceCard(Card):
    """ Class for the storage of the generic SurfaceCard type
    Methods for the generation of flat geometry surface card data
    should be place here. Classes needing to write flat 
    surface card data should be implemented in its own
    CodeSurfaceCard.py file
    """
    
    class BoundaryCondition(Enum):
        TRANSMISSION = 0
        VACUUM = 1
        REFLECTING = 2
        PERIODIC = 3
        WHITE = 4
    
    class SurfaceType(Enum):
        PLANE_GENERAL = 0
        PLANE_X = 1
        PLANE_Y = 2
        PLANE_Z = 3
        CYLINDER_X = 4
        CYLINDER_Y = 5
        CYLINDER_Z = 6
        SPHERE_GENERAL = 7
        CONE_X = 8
        CONE_Y = 9
        CONE_Z = 10
        TORUS_X = 11
        TORUS_Y = 12
        TORUS_Z = 13
        GENERAL_QUADRATIC = 14
        MACRO_RPP = 15
        MACRO_BOX = 16
        MACRO_RCC = 17
    
    # constructor for building a surface card
    def __init__(self,card_string):
        self.surface_type = 0
        self.surface_id = 0
        self.surface_transform = 0
        self.surface_coefficients = []
        self.boundary_condition = self.BoundaryCondition["TRANSMISSION"] 
        self.comment = ""
        self.b_box = [0,0,0,0,0,0] # b 
        Card.__init__(self,card_string)

    def __str__(self):
        string = "SurfaceCard: \n"
        string += "Surface ID " + str(self.surface_id)+"\n"
        string += "Transform ID " + str(self.surface_transform) + "\n"
        string += "Surface Type " + str(self.surface_type)+"\n"
        string += "Surface Coefficients " + str(self.surface_coefficients)+"\n"
        string += "Boundary Condition " + str(self.boundary_condition)+"\n"
        string += "Comment: " + str(self.comment)+"\n"
        return string
        
    def set_type(self, surf_id, surf_transform, surf_type, coords):
        self.surface_id = surf_id
        self.surface_transform = surf_transform
        self.surface_type = surf_type
        self.surface_coefficients = coords
        
    # test if the current surface is a macrobody or not
    def is_macrobody(self):
        if self.surface_type == self.SurfaceType['MACRO_RPP']:
            return True
        if self.surface_type == self.SurfaceType['MACRO_BOX']:
            return True
        if self.surface_type == self.SurfaceType['MACRO_RCC']:
            return True
        return False
    
    # get the bounding box 
    def bounding_box(self):
        # bounding box return value
        b_box = [0,0,0,0,0,0]

        if self.surface_type == self.SurfaceType['PLANE_X']:
            b_box[0] = self.surface_coefficients[3]
            b_box[1] = self.surface_coefficients[3]
        elif self.surface_type == self.SurfaceType['PLANE_Y']:
            b_box[2] = self.surface_coefficients[3]
            b_box[3] = self.surface_coefficients[3]
        elif self.surface_type == self.SurfaceType['PLANE_Z']:
            b_box[4] = self.surface_coefficients[3]
            b_box[5] = self.surface_coefficients[3]
        elif self.surface_type == self.SurfaceType['CYLINDER_X']:
            b_box[2] = self.surface_coefficients[0] - self.surface_coefficients[2]
            b_box[3] = self.surface_coefficients[0] + self.surface_coefficients[2]
            b_box[4] = self.surface_coefficients[1] - self.surface_coefficients[2]
            b_box[5] = self.surface_coefficients[1] + self.surface_coefficients[2]
        elif self.surface_type == self.SurfaceType['CYLINDER_Y']:
            b_box[0] = self.surface_coefficients[0] - self.surface_coefficients[2]
            b_box[1] = self.surface_coefficients[0] + self.surface_coefficients[2]
            b_box[4] = self.surface_coefficients[1] - self.surface_coefficients[2]
            b_box[5] = self.surface_coefficients[1] + self.surface_coefficients[2]
        elif self.surface_type == self.SurfaceType['CYLINDER_Z']:
            b_box[0] = self.surface_coefficients[0] - self.surface_coefficients[2]
            b_box[1] = self.surface_coefficients[0] + self.surface_coefficients[2]
            b_box[2] = self.surface_coefficients[1] - self.surface_coefficients[2]
            b_box[3] = self.surface_coefficients[1] + self.surface_coefficients[2]
        elif self.surface_type == self.SurfaceType['SPHERE_GENERAL']:
            b_box[0] = self.surface_coefficients[0] - self.surface_coefficients[3]
            b_box[1] = self.surface_coefficients[0] + self.surface_coefficients[3]
            b_box[2] = self.surface_coefficients[1] - self.surface_coefficients[3]
            b_box[3] = self.surface_coefficients[1] + self.surface_coefficients[3]
            b_box[4] = self.surface_coefficients[2] - self.surface_coefficients[3]
            b_box[5] = self.surface_coefficients[2] + self.surface_coefficients[3]
        return b_box

    # turn the surface into a gq type in preparation for transformation
    def generalise(self):
        a = 0 ; b = 0 ; c = 0 ; d = 0 ; e = 0 ; 
        f = 0 ; g = 0 ; h = 0 ; j = 0 ; k = 0 
        
        # note the -ve sign is due to the special way that MCNP defines
        # planes (in difference to say FLUKA)
        if self.surface_type == self.SurfaceType['PLANE_X']:
            g = 1.0
            k = -1.0*self.surface_coefficients[3]
        elif self.surface_type == self.SurfaceType['PLANE_Y']:
            h = 1.0
            k = -1.0*self.surface_coefficients[3]            
        elif self.surface_type == self.SurfaceType['PLANE_Z']:
            j = 1.0
            k = -1.0*self.surface_coefficients[3]            
        elif self.surface_type == self.SurfaceType['PLANE_GENERAL']:
            g = self.surface_coefficients[0]            
            h = self.surface_coefficients[1]
            j = self.surface_coefficients[2]
            k = -1.0*self.surface_coefficients[3]            
        # all spheres are general
        elif self.surface_type == self.SurfaceType['SPHERE_GENERAL']:
            a = 1 ; b = 1 ; c = 1 ; d = 0 ; e = 0 ; f = 0;
            g = -2*self.surface_coefficients[0]
            h = -2*self.surface_coefficients[1]
            j = -2*self.surface_coefficients[2]
            k = self.surface_coefficients[0]**2 + self.surface_coefficients[1]**2 \
                + self.surface_coefficients[2]**2 - self.surface_coefficients[3]**2
        # todo need to check cylinder equation
        elif self.surface_type == self.SurfaceType['CYLINDER_X']:
            b = 1 
            c = 1
            h = -2*self.surface_coefficients[0]
            j = -2*self.surface_coefficients[1]
            k = self.surface_coefficients[0]**2 + self.surface_coefficients[1]**2 - self.surface_coefficients[2]**2
        elif self.surface_type == self.SurfaceType['CYLINDER_Y']:
            a = 1 
            c = 1
            g = -2*self.surface_coefficients[0]
            j = -2*self.surface_coefficients[1]
            k = self.surface_coefficients[0]**2 + self.surface_coefficients[1]**2 - self.surface_coefficients[2]**2
        elif self.surface_type == self.SurfaceType['CYLINDER_Z']:
            a = 1 
            b = 1
            g = -2*self.surface_coefficients[0]
            h = -2*self.surface_coefficients[1]
            k = self.surface_coefficients[0]**2 + self.surface_coefficients[1]**2 - self.surface_coefficients[2]**2
        # todo check cone equation
        elif self.surface_type == self.SurfaceType['CONE_X']:
            a = -1*self.surface_coefficients[3]
            b = 1
            c = 1
            g =  2*self.surface_coefficients[0]*self.surface_coefficients[3]
            h = -2*self.surface_coefficients[1]
            j = -2*self.surface_coefficients[2]
            k = -self.surface_coefficients[3]*self.surface_coefficients[0]**2 + self.surface_coefficients[1]**2 + self.surface_coefficients[2]**2
        elif self.surface_type == self.SurfaceType['CONE_Y']:
            a = 1
            b = -1*self.surface_coefficients[3]
            c = 1
            g = -2*self.surface_coefficients[0]
            h =  2*self.surface_coefficients[1]*self.surface_coefficients[3]
            j = -2*self.surface_coefficients[2]
            k = self.surface_coefficients[0]**2 - self.surface_coefficients[3]*self.surface_coefficients[1]**2 + self.surface_coefficients[2]**2
        elif self.surface_type == self.SurfaceType['CONE_Z']:
            a = 1
            b = 1
            c = -1*self.surface_coefficients[3]
            g = -2*self.surface_coefficients[0]
            h = -2*self.surface_coefficients[1]
            j = 2*self.surface_coefficients[2]*self.surface_coefficients[3]
            k = self.surface_coefficients[0]**2 + self.surface_coefficients[1]**2 - self.surface_coefficients[2]**2*self.surface_coefficients[3]
        elif self.surface_type == self.SurfaceType['GENERAL_QUADRATIC']:
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
        else:
            print ("could not classify surface", self.surface_id)


        new_surface_coefficients = [0.]*10

        new_surface_coefficients[0] = a
        new_surface_coefficients[1] = b
        new_surface_coefficients[2] = c
        new_surface_coefficients[3] = d
        new_surface_coefficients[4] = e
        new_surface_coefficients[5] = f
        new_surface_coefficients[6] = g
        new_surface_coefficients[7] = h
        new_surface_coefficients[8] = j
        new_surface_coefficients[9] = k

        # dont forget to turn the type into a gq
        self.surface_type = self.SurfaceType['GENERAL_QUADRATIC'] 
        self.surface_coefficients = new_surface_coefficients
        return 

    def simplify(self):
        if(self.surface_type != self.SurfaceType['GENERAL_QUADRATIC']):
            return  
        # then its a plane!
        if all( value == 0. for value in self.surface_coefficients[0:5]) :
            self.surface_coefficients[0] = self.surface_coefficients[6]
            self.surface_coefficients[1] = self.surface_coefficients[7]
            self.surface_coefficients[2] = self.surface_coefficients[8]
            self.surface_coefficients[3] = -1.*self.surface_coefficients[9]
            self.surface_coefficients = self.surface_coefficients[0:4]
            self.surface_type = self.SurfaceType['PLANE_GENERAL']
        elif all( value == 0. for value in self.surface_coefficients[0:7]) :
            self.surface_coefficients[0] = 0.0
            self.surface_coefficients[1] = 0.0
            self.surface_coefficients[2] = 1.0
            self.surface_coefficients[3] = -1.*self.surface_coefficients[9]
            self.surface_coefficients = self.surface_coefficients[0:4]
            self.surface_type = self.SurfaceType['PLANE_Z']
        else:
            return

    """ translate a given surface by a distance coords
    """
    def translation(self,coords):
        self.generalise()
        # now do translation
        dx = -coords[0]
        dy = -coords[1]
        dz = -coords[2]

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

        trf = [[1,0,0,0], 
               [dx,1,0,0],
               [dy,0,1,0],
               [dz,0,0,1]]

        tmp = np.matmul(A,trf)
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

    # apply the transform to the surface
    def transform(self, rotation_matrix):
        self.generalise()
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

        # form the b matrix
        b1 = rotation_matrix[0][0]
        b2 = rotation_matrix[0][1]
        b3 = rotation_matrix[0][2]
        b4 = rotation_matrix[1][0]
        b5 = rotation_matrix[1][1]
        b6 = rotation_matrix[1][2]
        b7 = rotation_matrix[2][0]
        b8 = rotation_matrix[2][1]
        b9 = rotation_matrix[2][2]

        trf = [[1,0,0,0], 
               [0,b1,b2,b3],
               [0,b4,b5,b6],
               [0,b7,b8,b9]]

        # first do rotation
        tmp = np.matmul(A,trf)
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
