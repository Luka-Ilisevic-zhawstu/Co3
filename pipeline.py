"""
Execute a stochastic optimization algorithm repeatedly and record performance metrics.

Purpose:

This function is used to evaluate stochastic optimization algorithms over multiple
independent runs. Since such algorithms may produce different results each time
due to random initialization or probabilistic search behavior, repeated execution
allows a more reliable assessment of solution quality and computational cost.

For each run, the function records:
    - the best objective score returned by the algorithm
    - the corresponding object layout
    - the start time of the run
    - the end time of the run

Parameters:

algorithm : callable
    Optimization function to evaluate. It must return:
        (best_coordinates, best_score)
    where `best_coordinates` represents the resulting object layout and
    `best_score` is the corresponding objective value.
epoch : int
    Number of independent runs to perform.

Returns:

pandas.DataFrame
    A DataFrame containing one row per run with the following columns:
        - score: objective value of the best solution
        - objects: resulting object layout
        - start_time: timestamp at the beginning of the run
        - end_time: timestamp at the end of the run
"""

import pandas as pd
import time
from data_input.metadata import W, D, H
from optimizers.GA_random_parents import genetic_algorithm
from optimizers.monte_carlo import monte_carlo_optimization
from optimizers.simulated_annealing import simulated_annealing
from utils.converting import sort_coordinate
from data_input.metadata import objects
import os
from utils.complete_visualization import visualize_and_save

def test_algorithm(algorithm, epoch):

    results_dict = {"score":[], "objects":[], "start_time":[], "end_time":[]}
    for _ in range(epoch):
        results_dict["start_time"].append(time.time())
        best_coordinates, best_score = algorithm()
        results_dict["end_time"].append(time.time())
        results_dict["score"].append(best_score)
        results_dict["objects"].append(best_coordinates)
        
    return pd.DataFrame(results_dict)

epoch = 2

#------------------------------------------------------------------------------
# Genetic Algorithm Benchmark
#------------------------------------------------------------------------------

GA_result = test_algorithm(genetic_algorithm, epoch)
GA_result["duration(s)"] = GA_result["end_time"] - GA_result["start_time"]

# Extract and save coordinates of GA results
for i in range(epoch):
    output_dir = "output_data/picture/GA"
    os.makedirs(output_dir, exist_ok=True)

    algorithm_name = "GA"
    visualize_and_save(GA_result["objects"][i], W=W, D=D, H=H, output_dir = output_dir, algorithm_name = algorithm_name, epoch = i)

    GA_coords = sort_coordinate(GA_result["objects"][i])
    GA_coords_df = pd.DataFrame({
        "Object_Name": GA_coords[3],
        "X": GA_coords[0],
        "Y": GA_coords[1],
        "Z": GA_coords[2],
        "Volume": GA_coords[4]
    })
    
    output_dir = "output_data/object_coordinate/GA"
    os.makedirs(output_dir, exist_ok=True)
    GA_coords_df.to_csv(f"{output_dir}/GA_coordinates_{i}.csv", index=False)

#------------------------------------------------------------------------------
# Monte Carlo Benchmark
#------------------------------------------------------------------------------

monte_carlo_result = test_algorithm(lambda: monte_carlo_optimization(objects), epoch)
monte_carlo_result["duration(s)"] = monte_carlo_result["end_time"] - monte_carlo_result["start_time"]

for i in range(epoch):

    algorithm_name = "monte_carlo"
    output_dir = f"""output_data/picture/{algorithm_name}"""
    os.makedirs(output_dir, exist_ok=True)

    visualize_and_save(monte_carlo_result["objects"][i], W=W, D=D, H=H, output_dir = output_dir, algorithm_name = algorithm_name, epoch = i)

    monte_carlo_coords = sort_coordinate(monte_carlo_result["objects"][i])
    monte_carlo_df = pd.DataFrame({
        "Object_Name": monte_carlo_coords[3],
        "X": monte_carlo_coords[0],
        "Y": monte_carlo_coords[1],
        "Z": monte_carlo_coords[2],
        "Volume": monte_carlo_coords[4]
    })
    
    output_dir = "output_data/object_coordinate/monte_carlo"
    os.makedirs(output_dir, exist_ok=True)
    monte_carlo_df.to_csv(f"{output_dir}/monte_carlo_coordinates_{i}.csv", index=False)

#------------------------------------------------------------------------------
# Simulated Annealing Benchmark
#------------------------------------------------------------------------------

simulated_annealing_result = test_algorithm(lambda: simulated_annealing(objects), epoch)

for i in range(epoch):

    algorithm_name = "SA"
    output_dir = f"""output_data/picture/{algorithm_name}"""
    os.makedirs(output_dir, exist_ok=True)

    visualize_and_save(simulated_annealing_result["objects"][i], W=W, D=D, H=H, output_dir = output_dir, algorithm_name = algorithm_name, epoch = i)

    SA_coords = sort_coordinate(simulated_annealing_result["objects"][i])
    SA_df = pd.DataFrame({
        "Object_Name": SA_coords[3],
        "X": SA_coords[0],
        "Y": SA_coords[1],
        "Z": SA_coords[2],
        "Volume": SA_coords[4]
    })
    
    output_dir = f"output_data/object_coordinate/{algorithm_name}"
    os.makedirs(output_dir, exist_ok=True)
    SA_df.to_csv(f"{output_dir}/SA_coordinates_{i}.csv", index=False)

#------------------------------------------------------------------------------
# For each run:
#    -> Visualize object placement in space
#    -> Convert object coordinates into structured format
#    -> Save results as CSV for further analysis
#------------------------------------------------------------------------------

print(GA_result["score"].describe())
print(monte_carlo_result["score"].describe())
print(simulated_annealing_result["score"].describe())