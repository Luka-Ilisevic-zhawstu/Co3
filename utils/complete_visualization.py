"""
Complete Visualization and Coordinate Export Function

Single function that handles:
- 3D visualization of objects
- Saving figures with algorithm-specific naming
- Extracting object coordinates, names, and volumes
- Saving coordinates to CSV
"""

import os
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from model.shapes import Cube, Sphere, Pyramid


# -----------------------------------------------------------------------------
#    Complete visualization, saving, and coordinate extraction in one function.
    
#    Args:
#        objects: List of shape objects to visualize
#        W: Width of printer box
#        D: Depth of printer box
#        H: Height of printer box
#        output_dir: Directory to save output (e.g., "picture/GA")
#        algorithm_name: Name of algorithm (e.g., "GA", "Monte_Carlo", "Simulated_Annealing")
#        epoch: Epoch number for file naming
#------------------------------------------------------------------------------

def visualize_and_save(objects, W, D, H, output_dir, algorithm_name, epoch):

    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    axes = fig.add_subplot(111, projection="3d")
    
    # Draw printer box boundaries
    corners = [
        [0, 0, 0], [W, 0, 0], [W, D, 0], [0, D, 0],
        [0, 0, H], [W, 0, H], [W, D, H], [0, D, H],
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    for i, j in edges:
        xs = [corners[i][0], corners[j][0]]
        ys = [corners[i][1], corners[j][1]]
        zs = [corners[i][2], corners[j][2]]
        axes.plot(xs, ys, zs, color="black", linewidth=1)
    
    # Draw objects and collect coordinate data
    object_names = []
    xs = []
    ys = []
    zs = []
    volumes = []
    
    for obj in objects:
        # Draw Cube
        if isinstance(obj, Cube):
            s = obj.a / 2
            x, y, z = obj.x, obj.y, obj.z
            vertices = [
                [x - s, y - s, z - s], [x + s, y - s, z - s],
                [x + s, y + s, z - s], [x - s, y + s, z - s],
                [x - s, y - s, z + s], [x + s, y - s, z + s],
                [x + s, y + s, z + s], [x - s, y + s, z + s],
            ]
            faces = [
                [vertices[0], vertices[1], vertices[5], vertices[4]],
                [vertices[1], vertices[2], vertices[6], vertices[5]],
                [vertices[2], vertices[3], vertices[7], vertices[6]],
                [vertices[3], vertices[0], vertices[4], vertices[7]],
                [vertices[4], vertices[5], vertices[6], vertices[7]],
                [vertices[0], vertices[1], vertices[2], vertices[3]],
            ]
            axes.add_collection3d(Poly3DCollection(faces, facecolors="navy", edgecolors="black", alpha=0.25))
            object_names.append("Cube")
            volumes.append(obj.a ** 3)
        
        # Draw Sphere
        elif isinstance(obj, Sphere):
            theta_long = [2 * math.pi * i / 12 for i in range(13)]
            phi_lat = [math.pi * i / 12 for i in range(13)]
            xs_sphere, ys_sphere, zs_sphere = [], [], []
            for phi in phi_lat:
                row_x, row_y, row_z = [], [], []
                for theta in theta_long:
                    row_x.append(obj.x + obj.r * math.cos(theta) * math.sin(phi))
                    row_y.append(obj.y + obj.r * math.sin(theta) * math.sin(phi))
                    row_z.append(obj.z + obj.r * math.cos(phi))
                xs_sphere.append(row_x)
                ys_sphere.append(row_y)
                zs_sphere.append(row_z)
            axes.plot_surface(np.array(xs_sphere), np.array(ys_sphere), np.array(zs_sphere), 
                            color="gold", alpha=0.25, edgecolor="black", linewidth=0.2)
            object_names.append("Sphere")
            volumes.append((4/3) * math.pi * (obj.r ** 3))
        
        # Draw Pyramid
        elif isinstance(obj, Pyramid):
            x, y, z = obj.x, obj.y, obj.z
            half_b = obj.b / 2
            base_z = z - obj.h / 4
            apex_z = z + 3 * obj.h / 4
            v1 = [x - half_b, y - half_b, base_z]
            v2 = [x + half_b, y - half_b, base_z]
            v3 = [x + half_b, y + half_b, base_z]
            v4 = [x - half_b, y + half_b, base_z]
            apex = [x, y, apex_z]
            faces = [[v1, v2, v3, v4], [v1, v2, apex], [v2, v3, apex], [v3, v4, apex], [v4, v1, apex]]
            axes.add_collection3d(Poly3DCollection(faces, facecolors="limegreen", edgecolors="black", alpha=0.25))
            object_names.append("Pyramid")
            volumes.append((1/3) * (obj.b ** 2) * obj.h)
        
        # Mark object center
        axes.scatter(obj.x, obj.y, obj.z, color="black", s=20)
        xs.append(obj.x)
        ys.append(obj.y)
        zs.append(obj.z)
    
    # Set axis properties
    axes.set_xlim(0, W)
    axes.set_ylim(0, D)
    axes.set_zlim(0, H)
    axes.set_xlabel("Width (X)")
    axes.set_ylabel("Depth (Y)")
    axes.set_zlabel("Height (Z)")
    axes.set_title("3D Printer Packing Visualization")
    axes.set_box_aspect((W, D, H))
    
    # Save figure
    plt.tight_layout()
    image_filename = f"{output_dir}/{algorithm_name}_{epoch}.png"
    plt.savefig(image_filename, dpi=300)
    plt.close()
    print(f"✓ Image saved: {image_filename}")
    
