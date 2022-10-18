default_params = {
    "pop_size": 1000,
    "max_degree": 8,
    "select_pressure": 0.01,
    "evo_rate": [0.95, 0.01, 0.02, 0.02]    # crossover, subtree mutation, point mutation, hoist mutation
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
    "select_pressure": 0.02,
    "evo_rate": [0.95, 0.01, 0.02, 0.02]
}

gp_tournmant_lowpressure_params = {
    "pop_size": 1000,
    "max_degree": 8,
    "select_pressure": 0.005,
    "evo_rate": [0.95, 0.01, 0.02, 0.02]    # crossover, subtree mutation, point mutation, hoist mutation
}

params_list = [default_params, hc_params, gp_roulette_params, gp_tournmant_lowpressure_params]

N_GENERATION = 150
