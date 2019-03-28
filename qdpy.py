from qdpy import algorithms, containers, benchmarks, plots
from data import *

# Create container and algorithm. Here we use MAP-Elites, by illuminating a Grid container by evolution.
grid = containers.Grid(shape=(200,200), max_items_per_bin=1, fitness_domain=((0., 250.),), features_domain=((0., 250.), (0., 250.)))
algo = algorithms.RandomSearchMutPolyBounded(grid, budget=60000, batch_size=500, dimension=2, optimisation_task="minimisation",ind_domain= (0., 250.), eta=100)

# Create a logger to pretty-print everything and generate output data files
logger = algorithms.AlgorithmLogger(algo)

# Define evaluation function
eval_fn = algorithms.partial(distance, nb_features = len(grid.shape))

# Run illumination process !
best = algo.optimise(eval_fn)
print(best)

# Print results info
# print(algo.summary())

# Plot the results
# plots.default_plots_grid(logger)

# print("All results are available in the '%s' pickle file." % logger.final_filename)
