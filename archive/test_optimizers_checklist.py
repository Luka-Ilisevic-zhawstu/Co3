# -*- coding: utf-8 -*-
"""
Optimizer Testing

@author: Luka Ilisevic
"""
# Test set of basic objects to ensure optimizers run during checks
from model.shapes import Cube, Sphere, Pyramid
from model.objective_function import objective
from optimizers.monte_carlo import monte_carlo_optimization
from optimizers.simulated_annealing import simulated_annealing
from optimizers.GA_random_parents import genetic_algorithm

objects = [
    Cube(a=5.0),
    Cube(a=3.0),
    Sphere(r=3.0),
    Pyramid(b=4.0, h=6.0),
]

W, D, H = 38.0, 28.4, 38.0
lam = 50000

mc_best, mc_score = monte_carlo_optimization(
    objects, W=W, D=D, H=H, lam=lam, iterations=500, step=3.0
)
print("Monte Carlo score:", mc_score)

sa_best, sa_score = simulated_annealing(
    objects, W=W, D=D, H=H, lam=lam,
    n_iterations=500, step_size=3.0, temp=30.0
)
print("Simulated Annealing score:", sa_score)

ga_best, ga_score = genetic_algorithm()
print("Genetic Algorithm score:", ga_score)

# Check if final placements of the objects in space is valid
from model.objective_function import collision

def check_validity(objs, W, D, H):
    inside_bounds = True
    total_overlap = 0.0

    for o in objs:
        sx, sy, sz = o.half_size()
        if o.x - sx < 0 or o.x + sx > W:
            inside_bounds = False
        if o.y - sy < 0 or o.y + sy > D:
            inside_bounds = False
        if o.z - sz < 0 or o.z + sz > H:
            inside_bounds = False

    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            total_overlap += collision(objs[i], objs[j])

    return inside_bounds, total_overlap

# Test:
    
print("MC validity:", check_validity(mc_best, W, D, H))
print("SA validity:", check_validity(sa_best, W, D, H))
print("GA validity:", check_validity(ga_best, W, D, H))


# Checking repeat runs, compare score distributions:
def repeat_test(name, func, runs=5):
    scores = []
    for i in range(runs):
        best_objects, score = func()
        scores.append(score)
        print(f"{name} run {i+1}: {score}")
    print(f"{name} min={min(scores)}, max={max(scores)}, avg={sum(scores)/len(scores)}")
    
repeat_test(
    "Monte Carlo",
    lambda: monte_carlo_optimization(objects, W=W, D=D, H=H, lam=lam, iterations=500, step=3.0),
)

repeat_test(
    "Simulated Annealing",
    lambda: simulated_annealing(objects, W=W, D=D, H=H, lam=lam, n_iterations=500, step_size=3.0, temp=30.0),
)

repeat_test(
    "GA",
    lambda: genetic_algorithm(),
)