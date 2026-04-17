# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:57:17 2026

This defines the objective function and the physical space that is being used

@author: Luka Ilisevic
"""

"""
2. Collision Detection
we need to check if two objects overlap. the method how we do 
that depends on the shape combination.

Sphere + Shpere -> exact eucladean distance check
Combination of everything else -> Axis-Aligned Bounding Box

Returns: overlap amount
if 0.0 = no collision (objects do not touch)
if > 0.0 = collision 
------------------------------------------------------------
"""
import math
from model.shapes import Sphere #<------------- what is this for?

def collision (obj1, obj2):
    #sphere + sphere
    #Two spheres overlap if the distance between their centers
    #is less than the sum of their radii

    #distance = sqrt(dx^2 + dy^2 +dz^2)
    #overlap = (r1 + r2) - distance

    if isinstance(obj1, Sphere) and isinstance(obj2, Sphere):
        dist = math.sqrt(((obj1.x - obj2.x)**2) + ((obj1.y - obj2.y)**2) + ((obj1.z - obj2.z)**2))
        return max(0.0, (obj1.r + obj2.r)- dist)
    
    #All the other combinations
    #The object are treated as boxes. Two boxes overlap if they overlap on all three axes.
    #The overlap depth is the smallest overlapp across the three axes.

    sx1, sy1, sz1 = obj1.half_size()
    sx2, sy2, sz2 = obj2.half_size()

    overlap_x = ((sx1 + sx2) - abs(obj1.x - obj2.x))
    overlap_y = ((sy1 + sy2) - abs(obj1.y - obj2.y))
    overlap_z = ((sz1 + sz2) - abs(obj1.z - obj2.z))

    if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
        return (min(overlap_x, overlap_y, overlap_z))
    return 0.0


"""
3. Objective Function
What we want to do: 
- Minimize the volume occupied by 3D objects in a theoretical 3D printer volume
    
Ensure placement of objects within bounds of the theoretical printer volume without overlap -> penalties
- the overlap penalty (contstraint 1: objects must not overlap)
- the boundary penalty (constraint 2: objects must stay inside)

Formula:
 f = occupied_vol + lam * (overlap_penalty + boundary_penalty)

The parameter lam (lambda) controls how strictly contraints are enforced. 
Higher lam = algorithm prioritizes valid placements over minimizing empty space.

A perfect solution has no constraint violations at all
Penalty-Formulierung wird in studien gebracuht bei irregulären packing, 
da man ein algorithmus keine Regeln versteht, macht man das verstosse hoche werte ergeben,
weil wir das minimum wollen ist klar dases dann nicht sauber ist

------------------------------------------------------------
"""

def occupied_space(objs):
    
    # initialize minimum object vertex coordinates in control volume
    min_x = float("inf")
    min_y = float("inf")
    min_z = float("inf")
    
    # initialize maximum object vertex coordinates in control volume
    max_x = float("-inf")
    max_y = float("-inf")
    max_z = float("-inf")
    
    # loop over all defined objects
    for o in objs:
        # defining side variable based on object class (half_size) for each axis
        sx, sy, sz = o.half_size()
        
        # calculate minimum x,y and z coordinate of objects subtracting 
        # side variable (sx) from midpoint coordinate (o.x) of each object
        min_x = min(min_x, o.x - sx) # keep smaller value comparing stored minimum (min_x) vs current object's minimum (o.x - sx) 
        min_y = min(min_y, o.y - sy)
        min_z = min(min_z, o.z - sz)
        
        # calculate maximum x, y and z coordiante of objects adding side variable (sx)
        # to midpoint coordinate (o.x) of each object
        max_x = max(max_x, o.x + sx) # keep larger value comparing stored maximum (max_x) vs current object's maximum (o.x + sx)
        max_y = max(max_y, o.y + sy)
        max_z = max(max_z, o.z + sz)
    
    # calculate largest volume containing all 3D objects (caculating square volume/control volume)
    occupied_vol = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)
    return occupied_vol



def objective(objs, W, D, H, lam):
    # volume of the bounding box occupied by all objects
    
    occupied_vol = occupied_space(objs)
    
    penalty = 0.0

    # constraint 1: overlap penalty
    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            penalty += collision(objs[i], objs[j])**2

    # constraint 2: boundary penalty
    for o in objs:
        sx, sy, sz = o.half_size()

        penalty += max(0, sx - o.x)**2
        penalty += max(0, o.x + sx - W)**2

        penalty += max(0, sy - o.y)**2
        penalty += max(0, o.y + sy - D)**2

        penalty += max(0, sz - o.z)**2
        penalty += max(0, o.z + sz - H)**2

    return occupied_vol + lam * penalty