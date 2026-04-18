# -*- coding: utf-8 -*-
"""
Perturbation function shared by Simulated Annealing and Monte Carlo Optimizers

@author: Luka Ilisevic
"""
import copy
import random

#------------------------------------------------------------------------------
# Shift objects in volume to generate test cases for optimizers to compare
#------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------
# Deep copy helper used to copy layouts in both Monte Carlo and Simulated Annealing optimizers
#------------------------------------------------------------------------------

def clone_objects(objs):
    return copy.deepcopy(objs)