# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:55:29 2026

Main Program that runs all the other programs

@author: Luka Ilisevic
"""

from optimizers.simulated_annealing import simulated_annealing
from utils.shape_visualization_3D import animate_history
from model.create_shapes import Cube, Sphere, Pyramid
from model.objective_function import objective
import matplotlib.pyplot as plt

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
    lam=50000,
    n_iterations=5000,
    step_size=4.0,
    temp=30.0,
    return_trace=True
)

anim = animate_history(history, W, D, H, interval=100)