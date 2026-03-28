# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:55:29 2026

Main Program that runs all the other programs

@author: Luka Ilisevic
"""

from optimizer_SA import simulated_annealing
from shape_visualization_3D import animate_history
from create_shapes import Cube, Sphere, Pyramid
from objective_function import objective

def plot_scores(scores):
    fig = plt.figure(figsize=(8, 5))
    axes = fig.add_subplot(111)
    axes.plot(range(len(scores)), scores)
    axes.set_xlabel("Iteration")
    axes.set_ylabel("Best Objective Value")
    axes.set_title("Optimizer Score Over Time")
    axes.grid(True)
    plt.tight_layout()
    plt.show()
    
    

# standard test set
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

best, best_eval, scores, history = simulated_annealing(
    objects,
    objective,
    W=W,
    D=D,
    H=H,
    lam=5000,
    n_iterations=5000,
    step_size=4.0,
    temp=30.0
)

anim = animate_history(history, W, D, H, interval=100)