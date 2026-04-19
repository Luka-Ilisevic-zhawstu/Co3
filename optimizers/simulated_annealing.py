"""
Purpose:
        
Performs a Simulated Annealing (SA) optimization to improve the spatial layout 
of objects within a bounded 3D container.

The algorithm starts from a randomly generated initial layout and iteratively 
explores neighboring solutions by applying small perturbations to individual objects. 
New candidate solutions are accepted based on an acceptance criterion that allows 
both improvements and, with decreasing probability over time, worse solutions. 
This enables the algorithm to escape local minima.

The objective function evaluates layout quality based on packing efficiency 
and constraint penalties, weighted by a parameter λ.

Parameters:

objects: list
List of objects to be placed in the container.

W, D, H: float
Dimensions of the container (width, depth, height).

lam: float
Weighting factor for penalty terms in the objective function.

n_iterations: int
Number of iterations for the optimization process.

step_size: float
Maximum magnitude of perturbation applied to objects.

temp: float
Initial temperature controlling acceptance of worse solutions.

return_trace: bool, optional
If True, returns additional optimization history.

Returns:

best: list
Best found object configuration.

best_eval: float
Objective value of the best configuration.

scores: list (optional)
History of best scores over iterations.

history: list (optional)
History of layout configurations.

"""
import math
import random

from model.initialization import random_layout
from model.perturbation import perturb_object, clone_objects
from model.objective_function import objective
from data_input.metadata import W, D, H
from data_input.parameters import LAM, SA_iterations, SA_step, SA_temp


  
def simulated_annealing(objects, W = W, D = D, H = H, 
                        lam = LAM, n_iterations = SA_iterations, step_size = SA_step, temp = SA_temp, return_trace=False):
    
#-----------------------------------------------------------------------------
# Generating an initial solution
#-----------------------------------------------------------------------------
    current = random_layout(objects, W, D, H)
    current_eval = objective(current, W, D, H, lam)
    
    best = clone_objects(current)
    best_eval = current_eval
    
    scores = [best_eval]
    history = [clone_objects(current)]

#-----------------------------------------------------------------------------
# Optimization Loop
#-----------------------------------------------------------------------------
    for i in range(n_iterations):
        # Cooling schedule (conservative)
        t = temp * (0.999 ** i)
        
        # Generate candidate solution
        candidate = clone_objects(current)
        
        idx = random.randint(0, len(candidate) - 1)
        candidate[idx] = perturb_object(candidate[idx], W, D, H, step_size)
        
        candidate_eval = objective(candidate, W, D, H, lam)
        
#-----------------------------------------------------------------------------
# Defining the acceptance rule, allowing for some worse cases at high temps
#-----------------------------------------------------------------------------
        delta = candidate_eval - current_eval
        
        if delta < 0:
            current = candidate
            current_eval = candidate_eval
        else:
            if random.random() < math.exp(-delta / t):
                current = candidate
                current_eval = candidate_eval
                
#-----------------------------------------------------------------------------
# Tracking best solution
#-----------------------------------------------------------------------------
        if current_eval < best_eval:
            best = clone_objects(current)
            best_eval = current_eval
                
        # Optional progress print
        if i % 100 == 0:
            print(f"Iteration {i}, Temperature {t:.3f}, Best Evaluation {best_eval:.5f}")
        
        
#-----------------------------------------------------------------------------
# Return results
#-----------------------------------------------------------------------------       
    if return_trace:
        return best, best_eval, scores, history

    return best, best_eval 