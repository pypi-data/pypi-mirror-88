recipe = {

    'advi_use': False,
    'vi_family': "rnvp",

    "full_step_search": True,
    "full_step_search_scaling": False,
    'step_size': 0.01,
    'step_size_range': [0.01, 0.001, 0.0001],
    'max_iters': 100,
    'optimizer': 'adam',
    'M_iw_train': 1,
    'M_iw_sample': 5,
    'grad_estimator': "DReG",
    'per_iter_sample_budget': 100,

    'LI': False,

    'evaluation_fn': "IWELBO",

    'rnvp_num_transformations':  10,
    'rnvp_num_hidden_units':  16,
    'rnvp_num_hidden_layers':  2,
    'rnvp_params_init_scale':  0.01,

    'fix_sample_budget': False,
}
