import random

from model.initialization import random_layout
from model.perturbation import perturb_object, clone_objects
from model.objective_function import objective
from data_input.metadata import W, D, H
from data_input.parameters import LAM, MC_iterations, MC_step


# ------------------------------------------------------------
# Monte Carlo optimizer
# ------------------------------------------------------------
def monte_carlo_optimization(objects, W=W, D=D, H=H , lam=LAM, iterations=MC_iterations, step=MC_step):
    #random.seed(seed)

    # start from random placement, aligned with SA to use random_layout()
    current = random_layout(objects, W, D, H)

    current_score = objective(current, W, D, H, lam)

    best = clone_objects(current)
    best_score = current_score

    history = [best_score]

    for it in range(iterations):
        candidate = clone_objects(current)

        # choose one random object to move
        idx = random.randint(0, len(candidate) - 1)
        candidate[idx] = perturb_object(candidate[idx], W, D, H, step)

        candidate_score = objective(candidate, W, D, H, lam)

        # accept only if better
        if candidate_score < current_score:
            current = candidate
            current_score = candidate_score

            if candidate_score < best_score:
                best = clone_objects(candidate)
                best_score = candidate_score

        history.append(best_score)
        
    return best, best_score #, history da nur die besten appended --> nicht die volle history