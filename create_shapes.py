# -*- coding: utf-8 -*-
"""
Use this to generate 3D shapes used in the simulations

@author: Luka Ilisevic
"""

import math

"""
1. Objects
Containes the volume of the object as also the half_size of them
as they are needed to check whether the boundaries are correct or it there we're some
collisions
------------------------------------------------------------
"""
class Cube:
    def __init__(self, a):
        self.a = a                      #side length
        self.x = self.y = self.z = 0.0  #position
    
    def volume(self): 
        #V = a^3
        return (self.a ** 3)
    
    def half_size(self):
        # A cube extends a/2 in every direction from its center
        s = self.a /2
        return (s, s, s)
    
class Sphere:
    def __init__(self, r):
        self.r = r                      #radius
        self.x = self.y = self.z = 0.0

    def volume(self):
        #V = (4/3)*pi*r^3
        return ((4/3)* math.pi * self.r ** 3)
    
    def half_size(self):
        #A sphere extends excatly r in every direction from its center
        return (self.r, self.r, self.r)
    
class Pyramid:
    def __init__(self, b, h):
        self.b = b                      #base length
        self.h = h                      #height    
        self.x = self.y = self.z = 0.0
    
    def volume(self):
        #V = (1/3)* b^2*h
        return ((1/3)* self.b ** 2 * self.h)
    
    def half_size(self):
        #The center of a pyramid is at h/4 from tha base,
        # so it extends 3/4*h upward and 1/4*h downward
        return (self.b/2, self.b/2, self.h*3/4)
