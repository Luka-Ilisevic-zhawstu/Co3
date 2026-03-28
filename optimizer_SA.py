# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:01:57 2026

simulated annealing program

@author: Luka Ilisevic
"""
import math
import random
import copy

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
        # Gradually decrease temperature
        t = temp * (0.995 ** i)
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
                
        # Optional: print progress
        if i % 100 == 0:
            print(f"Iteration {i}, Temperature {t:.3f}, Best Evaluation {best_eval:.5f}")
        
        scores.append(best_eval)
        if i % 20 == 0:
            history.append(copy.deepcopy(current))
        
    return best, best_eval, scores, history