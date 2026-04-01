import pygad
import copy
from base.base_math_objfunction_updated import objective
from data_input.metadata import objects, W, D, H # <-----------------------------should find another solutions.

def converting_in_object(objects, list_coordination):
    """
    Converting the solution to the class Cube, Sphare and Pyramid
    
    Arg: 
        objects are in Class Cube, Spheare and Pyramid
        
    Return:  
        object 
    
    """

    objs_copy = copy.deepcopy(objects)
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

    return - objective(objs_copy,W,D,H,500)

def genetic_algorithm(initial_population = None):
    """
    Find the best solution for the objective function
    Return: 
        tuple(list(float), objective_score)
    """

    fitness_function = fitness_func

    num_generations = 2000
    num_parents_mating = 4

    sol_per_pop = 80
    num_genes = len(objects) * 3 # for x , y axis  

    init_range_low = 0.5
    init_range_high = 28

    parent_selection_type = "sss"
    keep_parents = 1

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        fitness_func=fitness_function,
                        sol_per_pop=sol_per_pop,
                        num_genes=num_genes,
                        init_range_low=init_range_low,
                        init_range_high=init_range_high,
                        parent_selection_type=parent_selection_type,
                        keep_parents=keep_parents,
                        crossover_type=crossover_type,
                        mutation_type=mutation_type,
                        mutation_percent_genes=mutation_percent_genes,
                        initial_population=initial_population)

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