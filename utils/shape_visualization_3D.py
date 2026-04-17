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
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection # required for final visualization

from model.create_shapes import Cube, Sphere, Pyramid

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
    
def draw_sphere(axes, sphere, color="gold", alpha=0.25, resolution=12):
    
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



# -------------------------------------------------------------
# 6. Animation of geometric shapes
# -------------------------------------------------------------

def random_pos(o, W, D, H):
    sx, sy, sz = o.half_size()
    x = random.uniform(sx, W - sx)
    y = random.uniform(sy, D - sy)
    z = random.uniform(sz, H - sz)
    return (x, y, z)

def draw_layout(axes, objects, W, D, H, title="3D Printer Packing Visualization"):
    axes.clear()

    draw_printer_box(axes, W, D, H)

    for obj in objects:
        if isinstance(obj, Cube):
            draw_cube(axes, obj)
        elif isinstance(obj, Sphere):
            draw_sphere(axes, obj, resolution=12)
        elif isinstance(obj, Pyramid):
            draw_pyramid(axes, obj)

        axes.scatter(obj.x, obj.y, obj.z, color="black", s=20)

    axes.set_xlim(0, W)
    axes.set_ylim(0, D)
    axes.set_zlim(0, H)

    axes.set_xlabel("Width (X)")
    axes.set_ylabel("Depth (Y)")
    axes.set_zlabel("Height (Z)")
    axes.set_title(title)
    axes.set_box_aspect((W, D, H))


# this is optional, comment out if you do not want to see the animation and only the final positions
def animate_history(history, W, D, H, interval=200):
    fig = plt.figure(figsize=(10, 8))
    axes = fig.add_subplot(111, projection="3d")

    def update(frame_idx):
        draw_layout(
            axes,
            history[frame_idx],
            W,
            D,
            H,
            title=f"3D Printer Packing - Iteration {frame_idx}"
        )

    anim = FuncAnimation(
        fig,
        update,
        frames=len(history),
        interval=interval,
        repeat=False
    )

    plt.tight_layout()
    plt.show()
    return anim