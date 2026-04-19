"""
Collision detection and objective function for 3D layout optimization.

1. Collision Detection
----------------------
This module evaluates whether two objects overlap in space. The collision
calculation depends on the combination of object shapes:

- Sphere + Sphere:
    Exact collision detection is performed using the Euclidean distance
    between the centers of the two spheres.

- Any other shape combination:
    Collision is approximated using an Axis-Aligned Bounding Box (AABB)
    approach. In this case, objects are treated as rectangular bounding
    boxes aligned with the coordinate axes.

The collision function returns the overlap amount:
    - 0.0  -> no collision
    - >0.0 -> objects overlap

For sphere-sphere collisions, the overlap is computed as:

    overlap = (r1 + r2) - distance(center1, center2)

For AABB-based collisions, overlap is determined independently along the
x-, y-, and z-axes. A collision exists only if overlap occurs on all
three axes. The returned overlap value is the minimum overlap depth
across the three directions.

2. Objective Function
---------------------
The objective of the optimization is to minimize the volume occupied by
a set of 3D objects inside a predefined printer workspace.

The optimization seeks compact object arrangements while enforcing two
geometric constraints:
    1. Objects must not overlap
    2. Objects must remain within the printer boundaries

The objective function is defined as:

    f = occupied_volume + lam * penalty

where:

    penalty = overlap_penalty + boundary_penalty

The parameter `lam` (lambda) controls the strength of constraint
enforcement:
    - small lam: more emphasis on compactness
    - large lam: more emphasis on feasible, non-overlapping placements

In this implementation, high penalty values are used to strongly
discourage invalid placements outside the build volume or intersecting
object configurations.
"""
import math
from model.shapes import Sphere # included for sphere-specific collision detection

def collision(obj1, obj2):
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