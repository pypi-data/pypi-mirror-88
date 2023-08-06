# =============================================================================
# Function for computing average partial effects of CF and GRF models
# 
# Contents
# --------
#   0. No Class
#      average_partial_effect 
# =============================================================================
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from input_utils import observation_weights
from causal_forest import cf_predict
from regression_forest import regression_forest, regf_predict

def average_partial_effect(forest,
                           calibrate_weights = True,
                           subset = None,
                           num_trees_for_variance = 500):
    """
    Estimate average partial effects using a causal forest

    Gets estimates of the average partial effect, in particular
    the (conditional) average treatment effect (target_sample = all):
    1/n sum_{i = 1}^n Cov[wi, yi | X = Xi] / Var[wi | X = Xi].
    Note that for a binary unconfounded treatment, the
    average partial effect matches the average treatment effect.

    If clusters are specified, then each cluster gets equal weight. For example,
    if there are 10 clusters with 1 unit each and per-cluster APE = 1, and there
    are 10 clusters with 19 units each and per-cluster APE = 0, then the overall
    APE is 0.5 (not 0.05).

    Parameters
    ----------
        forest : 
            The trained forest

        calibrate_weights : bool (default=True)
            Whether to force debiasing weights to match expected moments for 1, w, ["w_hat"], and 1/Var[w|X]

        subset : np.ndarray (num_subset_units,)
            Specifies a subset of the training examples over which we
            estimate the ATE. WARNING: For valid statistical performance,
            the subset should be defined only using features Xi, not using
            the treatment wi or the outcome yi

        num_trees_for_variance : int (default=500)
            Number of trees used to estimate Var(wi | Xi = x). Default is 500

    Returns
    -------
        An estimate of the average partial effect, along with standard the error

    Example
    -------
        n = 2000
        p = 10
        X = matrix(rnorm(n * p), n, p)
        W = rbinom(n, 1, 1 / (1 + exp(-X[, 2]))) + rnorm(n)
        Y = pmax(X[, 1], 0) * w + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
        tau.forest = causal_forest(X, y, w)
        tau_hat = predict(tau.forest)
        average_partial_effect(tau.forest)
        average_partial_effect(tau.forest, subset = X[, 1] > 0)
    """
    try:
        forest.__getattribute__('causal_forest')
    except AttributeError:
        raise AttributeError('Average effect estimation only implemented for causal_forest.')

    if not subset:
        subset = list(range(len(forest["y_hat"])+1))[1:]

    elif type(subset[0]) == 'bool' & len(subset) == len(forest["y_hat"]):
        subset = [i for i in list(range(len(forest["y_hat"]))) if subset[i]==True]

    if all(subset not in list(range(len(forest["y_hat"])))):
        ValueError(
            "If specified, subset must be a vector contained in 1:n,",
            "or a boolean vector of len n."
        )

    if len(forest["clusters"]) > 0:
        clusters =  forest["clusters"]
    else:
        clusters = list(range(len(forest["y_hat"])+1))[1:]

    observation_weight = observation_weights(forest)

    # Only use data selected via subsetting
    subset["X"] = forest["X"].loc[subset, :]
    subset["w"] = forest["w"].loc[subset, :]
    subset["w_hat"] = forest["w_hat"].loc[subset, :]
    subset["y"] = forest["y"].loc[subset, :]
    subset["y_hat"] = forest["y_hat"].loc[subset, :]
    tau_hat = [i for i, e in enumerate(cf_predict(forest)["predictions"]) if e in subset]
    subset_clusters = [i for i, e in enumerate(clusters) if e in subset]
    subset_weights = [i for i, e in enumerate(observation_weight) if e in subset]

    # This is a simple plugin estimate of the APE
    cape_plugin = np.average(tau_hat, weights=subset_weights)

    # Estimate the variance of W given X. For binary treatments,
    # we get a good implicit estimator V_hat = e_hat (1 - e_hat), and
    # so this step is not needed. Note that if we use the present CAPE estimator
    # with a binary treatment and set V_hat = e_hat (1 - e_hat), then we recover
    # exactly the AIPW estimator of the CATE
    variance_forest = regression_forest(subset["X"], # Need to adapt and convert regression_forest
                                        (subset["w"] - subset["w_hat"])^2,
                                        clusters = subset["clusters"],
                                        num_trees = num_trees_for_variance
                                        )
    V_hat = rf_predict(variance_forest)["predictions"]
    debiasing_weights = subset_weights * (subset["w"] - subset["w_hat"]) / V_hat

    # In the population, we want A' %*% weights = b
    # Modify debiasing weights gamma to make this True, i.e., compute
    # argmin {||gamma - gammainal||_2^2 : A'gamma = b}
    if calibrate_weights:
        A = subset.iloc[:, ["w", "w_hat"]] / sum(subset_weights)
        b = list(0, 1, 0)
        bias = np.dot(A.T, debiasing_weights) - b
        weights_lambda = np.linalg.solve(np.dot(A.T, A), bias)
        correction = np.dot(A, weights_lambda)
        debiasing_weights = debiasing_weights - correction

    # Compute a residual-based correction to the plugin.
    plugin_prediction = subset["y_hat"] + (subset["w"] - subset["w_hat"]) * tau_hat
    plugin_residual = subset["y"] - plugin_prediction
    # For conditional average partial effects
    cape_correction = np.mean(debiasing_weights * plugin_residual)
    cape_estimate = cape_plugin + cape_correction

    # Estimate variance using the calibration
    if len(subset_clusters) == 0:
        cape_se = np.sqrt(np.mean((debiasing_weights * plugin_residual)^2) / (len(subset["w"]) - 1))
    else:
        debiasing_clust = np.dot(csr_matrix(pd.Series(subset_clusters, dtype="category") + 0,).T, 
                                (debiasing_weights * plugin_residual))
        cape_se = np.sqrt(sum(debiasing_clust^2) \
                  / len(debiasing_clust) \
                  / (len(debiasing_clust) - 1))

    return list(estimate = cape_estimate, std_err = cape_se)