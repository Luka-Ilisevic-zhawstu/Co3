"""
Genetic Algorithm for 3D object placement optimization.

This module applies a Genetic Algorithm (GA) to optimize the placement
of objects within a bounded 3D workspace. Each candidate solution is
encoded as a flat list of object center coordinates:

    [x1, y1, z1, x2, y2, z2, ..., xn, yn, zn]

The Genetic Algorithm searches for coordinate combinations that minimize
the objective function, which includes:
    - occupied volume
    - overlap penalties
    - boundary violation penalties

Because PyGAD is designed to maximize a fitness function, the objective
value is multiplied by -1 so that minimizing the objective becomes
equivalent to maximizing fitness.
"""

import pygad
from model.perturbation import clone_objects
from model.objective_function import objective
from data_input.metadata import objects, W, D, H
from data_input.parameters import (
    GA_LAM, 
    GA_generations, 
    GA_num_parents_mating,
    GA_sol_per_pop,
    GA_init_range_low,
    GA_init_range_high,
    GA_mutation_percent_genes,
    )


def converting_in_object(objects, list_coordination):
    """
    Converting the solution to the class Cube, Sphare and Pyramid
    
    Arg: 
        objects are in Class Cube, Spheare and Pyramid
        
    Return:  
        object 
    
    """

    objs_copy = clone_objects(objects)
    for i,  o in enumerate(objs_copy):
        o.x = list_coordination[3*i]
        o.y = list_coordination[3*i+1]
        o.z = list_coordination[3*i+2]

    return objs_copy


def fitness_func(ga_instance, solution, solution_idx):
    """
    Changing the output of objective function to positive
    Arg:
        ga_instance (None) = No input expected only to fulfill the requirement of a fitness_function to pygad 
        solution (list(float)) = automatically filled by pygad to test the solution
        solution_idx (None) = No input expected only to fulfill the requirement of a fitness_function to pygad

    Return:
        float negative score

    """
    objs_copy = converting_in_object(objects, solution)

    return - objective(objs_copy, W, D, H, GA_LAM)

def genetic_algorithm(initial_population = None):
    """
    Find the best solution for the objective function
    Return: 
        tuple(list(float), objective_score)
    """

    num_genes = len(objects) * 3

    ga_instance = pygad.GA(
        num_generations=GA_generations,
        num_parents_mating=GA_num_parents_mating,
        fitness_func=fitness_func,
        sol_per_pop=GA_sol_per_pop,
        num_genes=num_genes,
        init_range_low=GA_init_range_low,
        init_range_high=GA_init_range_high,
        parent_selection_type="sss",
        keep_parents=1,
        crossover_type="single_point",
        mutation_type="random",
        mutation_percent_genes=GA_mutation_percent_genes,
        initial_population=initial_population
    )

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    #print("Parameters of the best solution : {solution}".format(solution=solution))
    #print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

    solution = converting_in_object(objects, solution)

    return  solution, (-solution_fitness) 


#import matplotlib.pyplot as plt

#plt.plot(ga_instance.best_solutions_fitness)
#plt.xlabel("Generation")
#plt.ylabel("Fitness")
#plt.title("Fitness Verlauf")
#plt.show()