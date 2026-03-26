from base_math_objfunction_updated import Cube, Sphere, Pyramid, objective
import pygad
import copy


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
    Pyramid(b = 5.0, h = 10.0),  
]

W, D, H = 38.0, 28.4, 38.0

def fitness_func(ga_instance,solution,solution_idx):
    objs_copy = copy.deepcopy(objects)
    for i, obj in enumerate(objs_copy):
        obj.x = solution[2*i]
        obj.y = solution[2*i+1]
        obj.z = obj.half_size[2]
    return - objective(objs_copy,W,D,H,500)

fitness_function = fitness_func

num_generations = 2000
num_parents_mating = 4

sol_per_pop = 80
num_genes = len(objects) * 2 # for x , y axis  

init_range_low = 0.5
init_range_high = 28

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "random"

mutation_type = "single_point"
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
                       mutation_percent_genes=mutation_percent_genes)

ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

import matplotlib.pyplot as plt

plt.plot(ga_instance.best_solutions_fitness)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness Verlauf")
plt.show()