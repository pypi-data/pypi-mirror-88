# =============================================================================
# The Causal Forest approach
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
#       causal_forest
#       cf_predict
# =============================================================================
import pandas as pd
import numpy as np
from input_utils import validate_X, validate_sample_weights, validate_observations
from input_utils import validate_clusters, validate_samples_per_cluster, validate_num_threads
from input_utils import do_call_rcpp # (Not necessary because of shared "_" notation)
from input_utils import create_data_matrices, validate_ll_vars, validate_ll_lambda
from input_utils import validate_newdata
from regression_forest import regression_forest, regf_predict
from boosted_regression_forest import boosted_regression_forest
from tune_causal_forest import tune_causal_forest
from tune_ll_causal_forest import tune_ll_causal_forest

def causal_forest(X, y, w,
                  y_hat = None,
                  w_hat = None,
                  num_trees = 2000,
                  sample_weights = None,
                  clusters = None,
                  samples_per_cluster = None,
                  sample_fraction = 0.5,
                  mtry = min(ceiling(np.sqrt(X.shape[1]) + 20), X.shape[1]),
                  min_node_size = 5,
                  honesty = True,
                  honesty_fraction = 0.5,
                  honesty_prune_leaves = True,
                  alpha = 0.05,
                  imbalance_penalty = 0,
                  stabilize_splits = True,
                  ci_group_size = 2,
                  tune_parameters = 'none',
                  tune_num_trees = 200,
                  tune_num_reps = 50,
                  tune_num_draws = 1000,
                  compute_oob_predictions = True,
                  orthog_boosting = False,
                  num_threads = None,
                  random_seed = np.random.randint(low=0, size=1)):
    """
    Trains a causal forest that can be used to estimate
    conditional average treatment effects tau(X). When
    the treatment assignment W is binary and unconfounded,
    we have tau(X) = E[Y(1) - Y(0) | X = x], where Y(0) and
    Y(1) are potential outcomes corresponding to the two possible
    treatment states. When W is continuous, we effectively estimate
    an average partial effect Cov[Y, W | X = x] / Var[W | X = x],
    and interpret it as a treatment effect given unconfoundedness.

    Parameters
    ----------
        X : numpy.ndarray : (num_units, num_features) : int, float
            The covariates used in the causal regression

        y : numpy.ndarray
            The outcome (must be a numeric vector with no NaNs)

        w : numpy.ndarray
            The treatment assignment (must be a binary or real numeric vector with no NaNs)

        y_hat : numpy.ndarray (default=None)
            Estimates of the expected responses E[y | Xi], marginalizing
            over treatment. If y_hat = None, these are estimated using
            a separate regression forest. See section 6.1.1 of the GRF paper for
            further discussion of this quantity.

        w_hat : numpy.ndarray (default=None)
            Estimates of the treatment propensities E[w | Xi]. If w_hat = None,
            these are estimated using a separate regression forest.

        num_trees : int (default=2000)
            Number of trees grown in the forest. Note: Getting accurate
            confidence intervals generally requires more trees than
            getting accurate predictions.

        sample_weights : (default=None)
            (experimental) Weights given to each sample in estimation.
            If None, each observation receives the same weight.
            Note: To avoid introducing confounding, weights should be
            independent of the potential outcomes given X.

        clusters : (default=None)
            Vector of integers or factors specifying which cluster each observation corresponds to.

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
            The number of random parameter values considered when using the model to select the optimal parameters

        compute_oob_predictions : bool (default=True)
            Whether OOB predictions on training set should be precomputed

        orthog_boosting : bool (default=False)
            (experimental) If True, then when y_hat = None or w_hat = None,
            the missing quantities are estimated using boosted regression forests.
            The number of boosting steps is selected automatically.

        num_threads : int (default=None, which selects the maximum hardware concurrency)
            Number of threads used in training

        random_seed : 
            The seed of the C++ random number generator

    Returns
    -------
        A trained causal forest object. If tune_parameters is enabled,
        then tuning information will be included through the `tuning_output` attribute.

    Example
    -------
        # Train a causal forest.
        n = 500
        p = 10
        X = matrix(rnorm(n * p), n, p)
        W = rbinom(n, 1, 0.5)
        Y = pmax(X[, 1], 0) * w + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
        causal_forest = causal_forest(X, y, w)

        # Predict using the forest
        X_test = matrix(0, 101, p)
        X_test[, 1] = seq(-2, 2, length_out = 101)
        causal_predictions = predict(causal_forest)[X_test]

        # Predict on out-of-bag training samples
        causal_predictions = predict(causal_forest)

        # Predict with confidence intervals; growing more trees is now recommended.
        causal_forest = causal_forest(X, y, w, num_trees = 4000)
        causal_predictions = precict(causal_forest)[X_test, estimate_variance = True]

        # In some examples, pre-fitting models for y and w separately may
        # be helpful (e.g., if different models use different covariates).
        # In some applications, one may even want to get y_hat and w_hat
        # using a completely different method (e.g., boosting).
        n = 2000
        p = 20
        X = matrix(rnorm(n * p), n, p)
        tau = 1 / (1 + exp(-X[, 3]))
        w = rbinom(n, 1, 1 / (1 + exp(-X[, 1] - X[, 2])))
        y = pmax(X[, 2] + X[, 3], 0) + rowMeans(X[, 4:6]) / 2 + w * tau + rnorm(n)

        forest_w = regression_forest(X, w, tune_parameters = "all")
        w_hat = predict(forest_w)[predictions]

        forest_y = regression_forest(X, y, tune_parameters = "all")
        y_hat = forest_y[predictions]

        forest_y_varimp = variable_importance(forest_y)

        # Note: Forests may have a hard time when trained on very few variables
        # (e.g., ncol(X) = 1, 2, or 3). We recommend not being too aggressive in selection.
        selected_vars = which(forest_y_varimp / mean(forest_y_varimp) > 0.2)

        tau_forest = causal_forest(X[, selected_vars], y, w, 
                                w_hat = w_hat, y_hat = y_hat, tune_parameters = "all")
        tau_hat = predict(tau_forest)[predictions]
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

    args_orthog = list(X = X,
                       num_trees = max(50, num_trees / 4),
                       sample_weights = sample_weights,
                       clusters = clusters,
                       samples_per_cluster = samples_per_cluster,
                       sample_fraction = sample_fraction,
                       mtry = mtry,
                       min_node_size = 5,
                       honesty = True,
                       honesty_fraction = 0.5,
                       honesty_prune_leaves = honesty_prune_leaves,
                       alpha = alpha,
                       imbalance_penalty = imbalance_penalty,
                       ci_group_size = 1,
                       tune_parameters = tune_parameters,
                       num_threads = num_threads,
                       random_seed = random_seed)

    if not y_hat & orthog_boosting == False:
        forest_y = do_call(regression_forest, list(args_orthog, y = list(y)))
        y_hat = forest_y.regf_predict()['predictions']
    elif not y_hat & orthog_boosting:
        forest_y = do_call(boosted_regression_forest, list(args_orthog, y = list(y)))
        y_hat = forest_y.regf_predict()['predictions']
    elif len(y_hat) == 1:
        y_hat = np.repeat(y_hat, X.shape[0])
    elif (len(y_hat) != X.shape[0]):
        print("y_hat has incorrect length.")
        return None

    if not w_hat & orthog_boosting == False:
        forest_w = do_call(regression_forest, list(args_orthog, y = list(w)))
        w_hat = forest_w.regf_predict()['predictions']
    elif not w_hat & orthog_boosting:
        forest_w = do_call(boosted_regression_forest, list(args_orthog, y = list(w)))
        w_hat = forest_w.regf_predict()['predictions']
    elif len(w_hat) == 1:
        w_hat = np.repeat(w_hat, X.shape[0])
    elif len(w_hat) != X.shape[0]:
        print("w_hat has incorrect length.")
        return None

    y_centered = y - y_hat
    w_centered = w - w_hat
    data = create_data_matrices(X, outcome = y_centered, treatment = w_centered,
                                sample_weights = sample_weights)
    args = list(num_trees = num_trees,
                clusters = clusters,
                samples_per_cluster = samples_per_cluster,
                sample_fraction = sample_fraction,
                mtry = mtry,
                min_node_size = min_node_size,
                honesty = honesty,
                honesty_fraction = honesty_fraction,
                honesty_prune_leaves = honesty_prune_leaves,
                alpha = alpha,
                imbalance_penalty = imbalance_penalty,
                stabilize_splits = stabilize_splits,
                ci_group_size = ci_group_size,
                compute_oob_predictions = compute_oob_predictions,
                num_threads = num_threads,
                random_seed = random_seed,
                reduced_form_weight = 0)

    tuning_output = None
    if not identical(tune_parameters, "none"): # Python manner
        tuning_output = tune_causal_forest(X, y, w, y_hat, w_hat,
                                        sample_weights = sample_weights,
                                        clusters = clusters,
                                        samples_per_cluster = samples_per_cluster,
                                        sample_fraction = sample_fraction,
                                        mtry = mtry,
                                        min_node_size = min_node_size,
                                        honesty = honesty,
                                        honesty_fraction = honesty_fraction,
                                        honesty_prune_leaves = honesty_prune_leaves,
                                        alpha = alpha,
                                        imbalance_penalty = imbalance_penalty,
                                        stabilize_splits = stabilize_splits,
                                        ci_group_size = ci_group_size,
                                        tune_parameters = tune_parameters,
                                        tune_num_trees = tune_num_trees,
                                        tune_num_reps = tune_num_reps,
                                        tune_num_draws = tune_num_draws,
                                        num_threads = num_threads,
                                        random_seed = random_seed)
    
    args = modifyList(args, list(tuning_output[["params"]]))

    forest = do_call_rcpp(causal_train, list(data, args))
    forest.astype("causal_forest", "grf")
    forest["ci_group_size"] = ci_group_size
    forest["X"] = X
    forest["y"] = y
    forest["w"] = w
    forest["y_hat"] = y_hat
    forest["w_hat"] = w_hat
    forest["clusters"] = clusters
    forest["sample_weights"] = sample_weights
    forest["tunable.params"] = args[all_tunable_params]
    forest["tuning_output"] = tuning_output

    return forest


def cf_predict(forest, newdata = None,
               linear_correction_variables = None,
               ll_lambda = None,
               ll_weight_penalty = False,
               num_threads = None,
               estimate_variance = False, *args, **kwargs):
    """
    Predict with a causal forest

    Gets estimates of tau(x) using a trained causal forest.

    Parameters
    ----------
    forest : 
        The trained forest

    newdata : numpy.ndarray(num_test, num_features) : int, float
        Points at which predictions should be made. If None, makes out-of-bag
        predictions on the training set instead (i.e., provides predictions at
        Xi using only trees that did not use the i-th training example). Note
        that this matrix should have the number of columns as the training
        matrix, and that the columns must appear in the same order.

    linear_correction_variables : numpy.ndarray : optional (default=None)
        Subset of indexes for variables to be used in local
        linear prediction. If None, standard GRF prediction is used. Otherwise,
        we run a locally weighted linear regression on the included variables.
        Please note that this is a beta feature still in development, and may slow down
        prediction considerably.

    ll_lambda : float : optional (default=None)
        Ridge penalty for local linear predictions

    ll_weight_penalty : bool (default=False)
        Option to standardize ridge penalty by covariance (True), or penalize all covariates equally (False)

    num_threads : int (default=None, which selects the maximum hardware concurrency)
        Number of threads used in training

    estimate_variance : bool (default=False)
        Whether variance estimates for hat{tau}(x) are desired (for confidence intervals)

    Returns
    -------
        Vector of predictions, along with estimates of the error and
        (optionally) its variance estimates. Column 'predictions' contains estimates
        of the conditional average treatent effect (CATE). The square-root of
        column 'variance.estimates' is the standard error of CATE.
        For out-of-bag estimates, we also output the following error measures.
        First, column 'debiased_error' contains estimates of the 'R-loss' criterion,
        a quantity that is related to the True (infeasible) mean-squared error
        (See Nie and Wager 2017 for a justification). Second, column 'excess_error'
        contains jackknife estimates of the Monte-carlo error (Wager, Hastie, Efron 2014),
        a measure of how unstable estimates are if we grow forests of the same size
        on the same data set. The sum of 'debiased_error' and 'excess_error' is the raw error
        attained by the current forest, and 'debiased_error' alone is an estimate of the error
        attained by a forest with an infinite number of trees. We recommend that users grow
        enough forests to make the 'excess_error' negligible.

    Example
    -------
        # Train a causal forest.
        n = 100
        p = 10
        X = matrix(rnorm(n * p), n, p)
        w = rbinom(n, 1, 0.5)
        y = pmax(X[, 1], 0) * w + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
        causal_forest = causal_forest(X, y, w)

        # Predict using the forest.
        X_test = matrix(0, 101, p)
        X_test[, 1] = seq(-2, 2, length_out = 101)
        causal_predictions = predict(causal_forest, X_test)

        # Predict on out-of-bag training samples.
        causal_predictions = predict(causal_forest)

        # Predict with confidence intervals; growing more trees is now recommended.
        causal_forest = causal_forest(X, y, w, num_trees = 500)
        causal_predictions = predict(causal_forest, X_test, estimate_variance = True)
    """
    # If possible, use pre-computed predictions.
    if not newdata & estimate_variance == False & forest[predictions] & linear_correction_variables == False:
        computed_preds = pd.DataFrame()
        computed_preds['predictions'] = forest['predictions']
        computed_preds['debiased_error'] = forest['debiased_error']
        computed_preds['excess_error'] = forest['excess_error']
        return computed_preds

    forest_short = forest[-which(names(forest) == "X")]

    X = forest[["X"]]
    y_centered = forest[["y"]] - forest[["y_hat"]]
    w_centered = forest[["w"]] - forest[["w_hat"]]
    train_data = create_data_matrices(X, outcome = y_centered, treatment = w_centered)

    num_threads = validate_num_threads(num_threads)

    local_linear = not linear_correction_variables
    if (local_linear):
        linear_correction_variables = validate_ll_vars(linear_correction_variables, ncol(X))

    if np.isnan(ll_lambda):
        ll_regularization_path = tune_ll_causal_forest(forest, linear_correction_variables,
                                                       ll_weight_penalty, num_threads)
        ll_lambda = ll_regularization_path['lambda_min']
    else:
        ll_lambda = validate_ll_lambda(ll_lambda)

    if newdata:
        validate_newdata(newdata, forest[X])
        data = create_data_matrices(newdata)
        if not local_linear:
            ret = causal_predict(forest_short, train_data['train_matrix'], train_data['sparse_train_matrix'],
                    train_data['outcome_index'], train_data['treatment_index'], data['train_matrix'],
                    data['sparse_train_matrix'], num_threads, estimate_variance)
        else:
            ret = ll_causal_predict(forest_short, data['train_matrix'], train_data['train_matrix'], data['sparse_train_matrix'],
                    train_data['sparse_train_matrix'], train_data['outcome_index'], train_data['treatment_index'],
                    ll_lambda, ll_weight_penalty, linear_correction_variables, num_threads, estimate_variance)

    else:
        if not local_linear:
            ret = causal_predict_oob(forest_short, train_data['train_matrix'], train_data['sparse_train_matrix'],
                  train_data['outcome_index'], train_data['treatment_index'], num_threads, estimate_variance)
        else:
            ret = ll_causal_predict_oob(forest_short, train_data['train_matrix'], train_data['sparse_train_matrix'],
                  train_data['outcome_index'], train_data['treatment_index'], ll_lambda, ll_weight_penalty,
                  linear_correction_variables, num_threads, estimate_variance)

    # Convert list to data frame
    empty = sapply(ret, function(elem), len(elem) == 0)

    do_call(cbind.pd.DataFrame, ret[not empty])