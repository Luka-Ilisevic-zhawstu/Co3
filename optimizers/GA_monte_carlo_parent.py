from optimizers.monte_carlo import monte_carlo_optimization
from optimizers.GA_random_parents import genetic_algorithm
from data_input.metadata import objects
from utils.converting import convert_object_into_list


def GA_montecarlo_parent():
    """
    Use Monte Carlo optimization to generate parents and then put the 80 outputs into genetic algorithm
    """
    epoch = 80
    initial_population = []

    for _ in range(epoch):
        best_coordinates, _ = monte_carlo_optimization(objects)
        list_coordinates = convert_object_into_list(best_coordinates)
        initial_population.append(list_coordinates)
    
    return genetic_algorithm(initial_population)

