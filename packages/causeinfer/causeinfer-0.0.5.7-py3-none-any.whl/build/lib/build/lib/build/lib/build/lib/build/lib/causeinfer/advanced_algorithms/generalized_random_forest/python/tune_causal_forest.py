# =============================================================================
# Tuning the Causal Forest approach
# 
# Based on
# --------
#   Athey, S.,  Tibshirani, J. & Wager, S. (2019) Generalized random forests. The Annals of Statistics, 
#   Vol. 47, No. 2 (2019), pp. 1148-1178.
#   
#   The accompanything R package: https://github.com/grf-labs/grf/tree/master/r-package/grf/
#   
#   grf documentation: https://grf-labs.github.io/grf/
#   
#   Wager, S. & Athey, S. (2018). Estimation and Inference of Heterogeneous Treatment Effects using Random Forests. 
#   Journal of the American Statistical Association, Vol. 113, 2018 - Issue 523, pp. 1228-1242.
# 
# Contents
# --------
#   0. No Class
#       tune_causal_forest
# =============================================================================

def tune_causal_forest(X, Y, W, y_hat, w_hat,
                       sample_weights = None,
                       clusters = None,
                       samples_per_cluster = None,
                       sample_fraction = 0.5,
                       mtry = min(ceiling(sqrt(ncol(X)) + 20), ncol(X)),
                       min_node_size = 5,
                       honesty = True,
                       honesty_fraction = 0.5,
                       honesty_prune_leaves = True,
                       alpha = 0.05,
                       imbalance_penalty = 0,
                       stabilize_splits = True,
                       ci_group_size = 2,
                       tune_parameters = "all",
                       tune_num_trees = 200,
                       tune_num_reps = 50,
                       tune_num_draws = 1000,
                       num_threads = None,
                       random_seed = np.random.randint(low=0, size=1)):
    """
    Causal forest tuning

    Parameters
    ----------
    X : numpy.ndarray : (num_units, num_features) : int, float
        The covariates used in the regression

    y : numpy.ndarray
        The outcomes given treatment status

    w : numpy.ndarray() : may numeric binary or real
        The treatment assignment

    y_hat : numpy.ndarray
        Estimates of the expected responses E[y | Xi], marginalizing
        over treatment. See section 6.1.1 of the GRF paper for
        further discussion of this quantity

    w_hat : numpy.ndarray
        Estimates of the treatment propensities E[w | Xi]

    sample_weights : (default=None)
        (experimental) Weights given to an observation in estimation
        If None, each observation is given the same weight

    clusters : (default=None, ignored)
        Vector of integers or factors specifying which cluster each observation corresponds to

    samples_per_cluster : (default=None)
        If sampling by cluster, the number of observations to be sampled from
        each cluster when training a tree. If None, we set samples_per_cluster to the size
        of the smallest cluster. If some clusters are smaller than samples_per_cluster,
        the whole cluster is used every time the cluster is drawn. Note that
        clusters with less than samples_per_cluster observations get relatively
        smaller weight than others in training the forest, i.e., the contribution
        of a given cluster to the final forest scales with the minimum of
        the number of observations in the cluster and samples_per_cluster.

    sample_fraction : float (default=0.5)
        Fraction of the data used to build each tree
        Note: If honesty = True, these subsamples will
        further be cut by a factor of honesty_fraction.

    mtry : int (default=\eqn{\sqrt p + 20}, p is the number of variables)
        Number of variables tried for each split

    min_node_size : int (default=5)
        A target for the minimum number of observations in each tree leaf. Note that nodes
        with size smaller than min_node_size can occur, as in the original randomForest package

    honesty : bool (default=True)
            Whether to use honest splitting (i.e., sub-sample splitting).
            For a detailed description of honesty, honesty_fraction, honesty_prune_leaves, and recommendations for
            parameter tuning, see the grf
            \href{https://grf-labs.github.io/grf/REFERENCE.html#honesty-honesty-fraction-honesty-prune-leaves}{algorithm reference}.

    honesty_fraction : float (default=0.5)
        The fraction of data that will be used for determining splits if honesty = True
        Corresponds to set J1 in the notation of the paper

    honesty_prune_leaves : bool (default=True)
        If True, prunes the estimation sample tree such that no leaves
        are empty. If FALSE, keep the same tree as determined in the splits sample (if an empty leave is encountered, that
        tree is skipped and does not contribute to the estimate). Setting this to FALSE may improve performance on
        small/marginally powered data, but requires more trees (note: tuning does not adjust the number of trees).
        Only applies if honesty is enabled.

    alpha : float (default=0.05)
        A tuning parameter that controls the maximum imbalance of a split.

    imbalance_penalty : float (default=0.0)
        A tuning parameter that controls how harshly imbalanced splits are penalized.

    stabilize_splits : bool (default=True)
        Whether or not the treatment should be taken into account when determining the imbalance of a split

    ci_group_size : int (defalt=2, must be at least 2 for confidence intervals)
        The forest will grow ci_group_size trees on each subsample

    tune_parameters : str
        A vector of parameter names to tune
        If "all": all tunable parameters are tuned by cross-validation. The following parameters are
        tunable: ("sample_fraction", "mtry", "min_node_size", "honesty_fraction",
        "honesty_prune_leaves", "alpha", "imbalance_penalty"). If honesty is FALSE the honesty.* parameters are not tuned.
        Default is "none" (no parameters are tuned).

    tune_num_trees : int (default=200)
        The number of trees in each 'mini forest' used to fit the tuning model

    tune_num_reps : int (default=50)
        The number of forests used to fit the tuning model

    tune_num_draws : int (default=1000)
        The number of random parameter values considered when using the model to select the optimal parameters. Default is 1000

    num_threads : int (default=None, which selects the maximum hardware concurrency)
        Number of threads used in training

    random_seed : 
        The seed of the C++ random number generator

    Returns
    -------
        A list consisting of the optimal parameter values ('params') along with their debiased
        error ('error')

    Example
    -------
        # Find the optimal tuning parameters.
        n = 500
        p = 10
        X = matrix(rnorm(n * p), n, p)
        w = rbinom(n, 1, 0.5)
        y = pmax(X[, 1], 0) * W + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
        y_hat = predict(regression_forest(X, y))$predictions
        w_hat = rep(0.5, n)
        params = tune_causal_forest(X, y, w, y_hat, w_hat)$params

        # Use these parameters to train a regression forest.
        tuned.forest = causal_forest(X, y, w,
        y_hat = y_hat, w_hat = w_hat, num.trees = 1000,
        min_node_size = as.numeric(params["min_node_size"]),
        sample_fraction = as.numeric(params["sample_fraction"]),
        mtry = as.numeric(params["mtry"]),
        alpha = as.numeric(params["alpha"]),
        imbalance_penalty = as.numeric(params["imbalance_penalty"])
    """
    validate_X(X)
    validate_sample_weights(sample_weights, X)
    y = validate_observations(y, X)
    w = validate_observations(w, X)
    clusters = validate_clusters(clusters, X)
    samples_per_cluster = validate_samples_per_cluster(samples_per_cluster, clusters)
    num_threads = validate_num_threads(num_threads)

    all_tunable_params = list("sample_fraction", "mtry", "min_node_size", "honesty_fraction",
                              "honesty_prune_leaves", "alpha", "imbalance_penalty")

    default_parameters = list(sample_fraction = 0.5,
                                mtry = min(ceiling(sqrt(ncol(X)) + 20), ncol(X)),
                                min_node_size = 5,
                                honesty_fraction = 0.5,
                                honesty_prune_leaves = True,
                                alpha = 0.05,
                                imbalance_penalty = 0)

    y_centered = y - y_hat
    w_centered = w - w_hat
    data = create_data_matrices(X, outcome = y_centered, treatment = w_centered,
                                sample_weights = sample_weights)
    nrow_X = X.shape[0]
    ncol_X = X.shape[1]
    args = list(clusters = clusters,
                samples_per_cluster = samples_per_cluster,
                sample_fraction = sample_fraction,
                mtry = mtry,
                min_node_size = min_node_size,
                honesty = honesty,
                honesty_fraction = honesty_fraction,
                honesty_prune_leaves = honesty_prune_leaves,
                alpha = alpha,
                stabilize_splits = stabilize_splits,
                imbalance_penalty = imbalance_penalty,
                ci_group_size = ci_group_size,
                num_threads = num_threads,
                random_seed = random_seed,
                reduced.form.weight = 0)

    if identical(tune_parameters, "all"):
        tune_parameters = all_tunable_params
    else:
        tune_parameters = unique(match.arg(tune_parameters, all_tunable_params, several.ok = True))

    if not honesty:
        tune_parameters = tune_parameters[!grepl("honesty", tune_parameters)]

    tune_parameters_defaults = default_parameters[tune_parameters]
    train = causal_train
    predict_oob = causal_predict_oob
    predict_data_args = list("train_matrix", "sparse_train_matrix", "outcome_index", "treatment_index")

    tuning_output = tune_forest(data = data,
                                nrow_X = nrow_X,
                                ncol_X = ncol_X,
                                args = args,
                                tune_parameters = tune_parameters,
                                tune_parameters_defaults = tune_parameters_defaults,
                                num_fit_trees = tune_num_trees,
                                num_fit_reps = tune_num_reps,
                                num_optimize_reps = tune_num_draws,
                                train = train,
                                predict_oob = predict_oob,
                                predict_data_args = predict_data_args)

    return tuning_output