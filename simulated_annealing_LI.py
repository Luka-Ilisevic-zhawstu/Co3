# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:02:12 2026

The goal of this program is to 

@author: Luka Ilisevic
"""

### 1. Draw Shapes

import math
import random
import copy


"""
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



def objective(objs, W = 38.0, D = 28.4, H = 38.0, lam = 50):
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

"""
4.0 Object sizes and print space
"""
# standard group
objects = [

    Cube(a = 5.0),

    Cube(a = 5.0),

    Cube(a = 5.0),

    Cube(a = 5.0),

    Cube(a = 15.0),

    Sphere(r = 3.0),

    Sphere(r = 3.0),

    Sphere(r = 8.0),

    Pyramid(b = 4.0, h = 10.0),

    Pyramid(b = 5.0, h = 10.0),

    Pyramid(b = 5.0, h = 10.0)
    
    ]

W, D, H = 38.0, 28.4, 38.0

""" 
5.0 Random placement of objects in space with random_pos and track placement with random_layout
"""

def random_pos(o, W = 38.0, D = 28.4, H = 38.0):
    sx, sy, sz = o.half_size()
    x = random.uniform(sx, max(sx+0.01, W-sx))
    y = random.uniform(sy, max(sy+0.01, D-sy))
    z = random.uniform(sz, max(sz+0.01, H-sz))
    return (x, y, z)

def random_layout(objects, W = 38.0, D = 28.4, H = 38.0):
    layout = copy.deepcopy(objects)
    for o in layout:
        o.x, o.y, o.z = random_pos(o, W, D, H)
    return layout



"""
6.0 Integrate into simulated annealing algorithm (using Michelle's perturb_objects function to change position)
"""
def perturb_object(o, W = 38.0, D = 28.4, H = 38.0, step = 2.0):
    new_o = copy.deepcopy(o)
    
    # randomly move objects in x,y,z-direction
    new_o.x += random.uniform(-step, step)
    new_o.y += random.uniform(-step, step)
    new_o.z += random.uniform(-step, step)
    
    # keep object inside the box
    sx, sy, sz = new_o.half_size()
    
    new_o.x = min(max(new_o.x, sx), W - sx)
    new_o.y = min(max(new_o.y, sy), D - sy)
    new_o.z = min(max(new_o.z, sz), H - sz)
    
    return new_o


def perturb_layout(layout, W = 38.0, D = 28.4, H = 38.0, step = 2.0):
    candidate = copy.deepcopy(layout)
    
    #choose one random object to move
    idx = random.randint(0, len(candidate) - 1)
    candidate[idx] = perturb_object(candidate[idx], W, D, H, step)
    
    return candidate
    
def simulated_annealing(objects, objective,  W = 38.0, D = 28.4, H = 38.0, 
                        lam = 500, n_iterations = 1000, step_size = 2.0, temp = 10):
    
    # Random layout
    current = random_layout(objects, W, D, H)
    current_eval = objective(current, W, D, H, lam)
    
    best = copy.deepcopy(current)
    best_eval = current_eval
    
    scores = [best_eval]
    history = [copy.deepcopy(current)]
    
    for i in range(n_iterations):
        # Continuously decrease temperature
        t = temp / float(i + 1)
        # Generate candidate soluation
        
        candidate = perturb_layout(current, W, D, H, step_size)
        candidate_eval = objective(candidate, W, D, H, lam)
        
        delta = candidate_eval - current_eval

        if delta < 0:
            current = candidate
            current_eval = candidate_eval
        else:
            if random.random() < math.exp(-delta / t):
                current = candidate
                current_eval = candidate_eval

        if current_eval < best_eval:
                best = copy.deepcopy(current)
                best_eval = current_eval
        
        if candidate_eval < current_eval: 
            current = candidate
            current_eval = candidate_eval
            
            if candidate_eval < best_eval:
                best = copy.deepcopy(candidate)
                best_eval = candidate_eval
                
        # Optional: print progress
        if i % 100 == 0:
            print(f"Iteration {i}, Temperature {t:.3f}, Best Evaluation {best_eval:.5f}")
        
        scores.append(best_eval)
        history.append(copy.deepcopy(current))
    return best, best_eval, scores

"""
Implementing the algorithm
"""

n_iterations = 1000
step_size = 0.1
temp = 10.0
lam = 500

best, score, scores = simulated_annealing(
    objects,
    objective,
    W = 38.0,
    D = 28.4,
    H = 38.0,
    lam = lam,
    n_iterations = n_iterations,
    step_size = step_size,
    temp = temp
    )

print("Best Score: ", score)
for i, o in enumerate(best, start = 1):
    print(f"Object {i}: {type(o).__name__}, x={o.x:2f}, y={o.y:2f}, z={o.z:2f}")