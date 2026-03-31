import pandas as pd
import time 
from algorithmn.GA_random_parents import genetic_algorithm
from algorithmn.monte_carlo import monte_carlo_optimization
from algorithmn.optimizer_SA import simulated_annealing
from base.objective_function import objective
import matplotlib.pyplot as plt
from utils.converting import sort_coordinate
from data_input.metadata import objects
import os
from utils.complete_visualization import visualize_and_save

def test_algorithm(algorithm, epoch):
    """
    Test algorithm and save start time, end time, objects, and scores.
    Args:
        algorithm: Algorithm function to test.
    Return:
        DataFrame with score, objects, start_time, end_time
    """

    results_dict = {"score":[], "objects":[], "start_time":[], "end_time":[]}
    for _ in range(epoch):
        results_dict["start_time"].append(time.time())
        best_coordinates, best_score = algorithm()
        results_dict["end_time"].append(time.time())
        results_dict["score"].append(best_score)
        results_dict["objects"].append(best_coordinates)
        
    return pd.DataFrame(results_dict)

epoch = 2

GA_result = test_algorithm(genetic_algorithm, epoch)
GA_result["duration(s)"] = GA_result["end_time"] - GA_result["start_time"]

# Extract and save coordinates of GA results
for i in range(epoch):
    output_dir = "output_data/picture/GA"
    os.makedirs(output_dir, exist_ok=True)

    algorithm_name = "GA"
    visualize_and_save(GA_result["objects"][i], W=38.0, D=28.4, H=38.0, output_dir = output_dir, algorithm_name = algorithm_name, epoch = i)

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


monte_carlo_result = test_algorithm(lambda: monte_carlo_optimization(objects), epoch)
monte_carlo_result["duration(s)"] = monte_carlo_result["end_time"] - monte_carlo_result["start_time"]

for i in range(epoch):

    algorithm_name = "monte_carlo"
    output_dir = f"""output_data/picture/{algorithm_name}"""
    os.makedirs(output_dir, exist_ok=True)

    visualize_and_save(monte_carlo_result["objects"][i], W=38.0, D=28.4, H=38.0, output_dir = output_dir, algorithm_name = algorithm_name, epoch = i)

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

simulated_annealing_result = test_algorithm(lambda: simulated_annealing(objects, objective), epoch)

for i in range(epoch):

    algorithm_name = "SA"
    output_dir = f"""output_data/picture/{algorithm_name}"""
    os.makedirs(output_dir, exist_ok=True)

    visualize_and_save(simulated_annealing_result["objects"][i], W=38.0, D=28.4, H=38.0, output_dir = output_dir, algorithm_name = algorithm_name, epoch = i)

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


print(GA_result["score"].describe())
print(monte_carlo_result["score"].describe())
print(simulated_annealing_result["score"].describe())