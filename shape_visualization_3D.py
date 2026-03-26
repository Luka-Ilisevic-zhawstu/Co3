# -*- coding: utf-8 -*-
"""

CO3 Bioinspired Algorithms

3D Visualization of Packing Problem

This script visualizes the spatial arrangement of 3D objects (cubes, spheres,
and pyramids) within a fixed printer volume. Objects are assigned positions
in 3D space and rendered using matplotlib.

The visualization serves as a tool to inspect and validate object placement
in the context of a 3D packing optimization problem. 

"""

# --------------- Visualizing Spatial Arrangement in 3D -----------------------

import math
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection # required for final visualization

# -----------------------------------------------------------------------------

# 1. Taking Shape Classes (from Luana)

# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------
# 2. Placing Objects in Random Valid Position (TEST ONLY, NO OVERLAP DETECTION)
# -----------------------------------------------------------------------------

def random_pos(o, W, D, H):
    sx, sy, sz = o.half_size()
    x = random.uniform(sx, max(sx + 0.01, W - sx))
    y = random.uniform(sy, max(sy + 0.01, D - sy))
    z = random.uniform(sz, max(sz + 0.01, H - sz))
    return (x, y, z)

# -----------------------------------------------------------------------------
# 3. Helpers translating vertices into faces then into shapes within printing volume
# -----------------------------------------------------------------------------

def draw_cube(axes, cube, color = "navy", alpha = 0.25):
    s = cube.a/2
    x, y, z = cube.x, cube.y, cube.z
    
    # Define all corners of 3D cube (8 total), relative to length of side (s)
    vertices = [
        [x - s, y - s, z - s],
        [x + s, y - s, z - s],
        [x + s, y + s, z - s],
        [x - s, y + s, z - s],
        [x - s, y - s, z + s],
        [x + s, y - s, z + s],
        [x + s, y + s, z + s],
        [x - s, y + s, z + s],
    ]
    
    # Define surfaces based on 3D cube corners, maintaining alignment in planes
    faces = [
        [vertices[0], vertices[1], vertices[5], vertices[4]], # front face 
        [vertices[1], vertices[2], vertices[6], vertices[5]], # right face
        [vertices[2], vertices[3], vertices[7], vertices[6]], # back face
        [vertices[3], vertices[0], vertices[4], vertices[7]], # left face
        [vertices[4], vertices[5], vertices[6], vertices[7]], # top face
        [vertices[0], vertices[1], vertices[2], vertices[3]], # bottom face
    ]
    
    # Create shape within the coordinate system defined by our axes
    axes.add_collection3d(Poly3DCollection(faces, facecolors = color, edgecolors = "black", alpha = alpha))
    
def draw_sphere(axes, sphere, color="gold", alpha=0.25, resolution=20):
    
    # List angles around the whole sphere East/West (longitudinally) - > 2*pi
    theta_long = []
    
    # List angles crossing sphere North/South (latitudinally) -> pi
    phi_lat = []
    
    # Generate angles in stepsizes defined by resolution (ex. like orange cut into 20 slices vertically, and 20 pieces horizontally)
    for i in range(resolution + 1):
        theta_long.append(2 * math.pi * i / resolution)
        phi_lat.append(math.pi * i / resolution)

    xs, ys, zs = [], [], []

    # convert spherical coordinates to cartesian coordinate system
    # using formula:
    #   x = radial_dist*sin(phi)*cos(theta)
    #   y = radial_dist*sin(phi)*sin(theta)
    #   z = radial_dist*cos(phi)

    for phi in phi_lat:
        row_x, row_y, row_z = [], [], []
        for theta in theta_long:
            row_x.append(sphere.x + sphere.r * math.cos(theta) * math.sin(phi))
            row_y.append(sphere.y + sphere.r * math.sin(theta) * math.sin(phi))
            row_z.append(sphere.z + sphere.r * math.cos(phi))
        xs.append(row_x)
        ys.append(row_y)
        zs.append(row_z)

    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)
    
    axes.plot_surface(xs, ys, zs, color=color, alpha = alpha, edgecolor = "black", linewidth = 0.2)
    
def draw_pyramid(axes, pyramid, color = "limegreen", alpha = 0.25):
    
    # pyramid key parameters: x,y,z coordinates, base, height, half-base value
    x, y, z = pyramid.x, pyramid.y, pyramid.z
    b = pyramid.b
    h = pyramid.h
    half_b = b / 2

    base_z = z - h / 4
    apex_z = z + 3 * h / 4

    v1 = [x - half_b, y - half_b, base_z]
    v2 = [x + half_b, y - half_b, base_z]
    v3 = [x + half_b, y + half_b, base_z]
    v4 = [x - half_b, y + half_b, base_z]
    apex = [x, y, apex_z]

    faces = [
        [v1, v2, v3, v4],   # pyramid base
        [v1, v2, apex],
        [v2, v3, apex],
        [v3, v4, apex],
        [v4, v1, apex],
    ]

    axes.add_collection3d(Poly3DCollection(faces, facecolors = color, edgecolors = "black", alpha = alpha))


def draw_printer_box(axes, W, D, H):
    # print volumee defined as cube with eight corners
    corners = [
        [0, 0, 0],
        [W, 0, 0],
        [W, D, 0],
        [0, D, 0],
        [0, 0, H],
        [W, 0, H],
        [W, D, H],
        [0, D, H],
    ]
    
    # defining edges of print volume
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    
    # move through points to draw limits of print volume
    for i, j in edges:
        xs = [corners[i][0], corners[j][0]]
        ys = [corners[i][1], corners[j][1]]
        zs = [corners[i][2], corners[j][2]]
        axes.plot(xs, ys, zs, color = "black", linewidth = 1)    
    
# -----------------------------------------------------------------------------
# 4. Actual Visualization Function
# -----------------------------------------------------------------------------

def visualize_objects(objects, W, D, H):
    fig = plt.figure(figsize = (10, 8))
    axes = fig.add_subplot(111, projection="3d")

    draw_printer_box(axes, W, D, H)

    for obj in objects:
        if isinstance(obj, Cube):
            draw_cube(axes, obj)
        elif isinstance(obj, Sphere):
            draw_sphere(axes, obj)
        elif isinstance(obj, Pyramid):
            draw_pyramid(axes, obj)

        # mark object center
        axes.scatter(obj.x, obj.y, obj.z, color = "black", s = 20)

    axes.set_xlim(0, W)
    axes.set_ylim(0, D)
    axes.set_zlim(0, H)

    axes.set_xlabel("Width (X)")
    axes.set_ylabel("Depth (Y)")
    axes.set_zlabel("Height (Z)")
    axes.set_title("3D Printer Packing Visualization")

    # Helps reduce distortion in the visual proportions
    axes.set_box_aspect((W, D, H))

    plt.tight_layout()
    plt.show()

# ------------------------------------------------------------
# 5. Visualization Test Case
# ------------------------------------------------------------

### NOTE for Spyder best view achieved by changing:
### Tools -> Preferences -> IPython Console -> change Backend dropdown from "Inline" to Qt5

objects = [
    Cube(a = 5.0),
    Cube(a = 3.0),
    Sphere(r = 3.0),
    Sphere(r = 2.0),
    Pyramid(b = 4.0, h = 10.0),
    Pyramid(b = 3.0, h = 4.0),
]

W, D, H = 38.0, 28.4, 38.0

for o in objects:
    o.x, o.y, o.z = random_pos(o, W, D, H)
    
for o in objects:
    print(type(o).__name__, (o.x, o.y, o.z))

visualize_objects(objects, W, D, H)