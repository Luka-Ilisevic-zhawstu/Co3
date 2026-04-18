# -*- coding: utf-8 -*-
"""
Configuration file: Single source of truth for parameters used in optimizers,
for ease of use and tuning efficiency.


@author: Luka Ilisevic
"""

#------------------------------------------------------------------------------
# Objective Function input
#------------------------------------------------------------------------------

LAM = 50000 # called by MC and SA optimizers

#------------------------------------------------------------------------------
# Monte Carlo inputs
#------------------------------------------------------------------------------

MC_iterations = 10000
MC_step = 5.0

#------------------------------------------------------------------------------
# Simulated Annealing inputs
#------------------------------------------------------------------------------

SA_iterations = 10000
SA_step = 5.0
SA_temp = 100

#------------------------------------------------------------------------------
# Genetic Algorithm inputs
#------------------------------------------------------------------------------

GA_generations = 2000
GA_pop_size = 80
GA_LAM = 1000 # reduced from 50000 due to poor optimizer performance (did not reduce compactness score)
GA_num_parents_mating = 4
GA_sol_per_pop = 80
GA_init_range_low = 0.5
GA_init_range_high = 28
GA_mutation_percent_genes = 10