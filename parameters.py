default_params = {
    "pop_size": 1000,
    "max_degree": 8,
    "select_pressure": 0.01,
    "evo_rate": [0.9, 0.02, 0.04, 0.04]    # crossover, subtree mutation, point mutation, hoist mutation
}

hc_params = {
    "pop_size": 1000,
    "max_degree": 8,
    "select_pressure": 0.01,
    "evo_rate": [0, 0.2, 0.6, 0.2]
}

gp_roulette_params = {
    "pop_size": 1000,
    "max_degree": 8,
    "select_pressure": 0.05,
    "evo_rate": [0.9, 0.02, 0.04, 0.04]
}

params_list = [default_params, hc_params, gp_roulette_params]

N_GENERATION = 150
