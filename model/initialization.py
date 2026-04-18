# -*- coding: utf-8 -*-
"""
Random Position

Returns a random valid position inside the print volume.
Wichtig damit man die Figuren "verschieben" kann, die richtige/passende Positionierung
der unterschiedlichen Figuren

""" 

import random
import copy
from data_input.metadata import W, D, H

def random_pos(o, W, D, H):
    sx, sy, sz = o.half_size()
    x = random.uniform(sx, max(sx+0.01, W-sx))
    y = random.uniform(sy, max(sy+0.01, D-sy))
    z = random.uniform(sz, max(sz+0.01, H-sz))
    return (x, y, z)

def random_layout(objects, W = W, D = D, H = H):
    layout = copy.deepcopy(objects)
    for o in layout:
        o.x, o.y, o.z = random_pos(o, W, D, H)
    return layout