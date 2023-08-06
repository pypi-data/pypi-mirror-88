# =============================================================================
# Function for computing average treatment effects of CF and GRF models
# 
# Contents
# --------
#   0. No Class
#      average_treatment_effect 
# =============================================================================
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import statsmodels.api as sm
from statsmodels.stats import sandwich_covariance
from input_utils import observation_weights
from causal_forest import cf_predict

def average_treatment_effect(forest,
                             target_sample = 'all',
                             method = 'AIPW',
                             subset = None):
    """
    Estimate average treatment effects using a causal forest

    Gets estimates of one of the following.
    \itemize{
    \item The (conditional) average treatment effect (target_sample = all):
    sum_{i = 1}^n E[y(1) - y(0) | X = Xi] / n
    \item The (conditional) average treatment effect on the treated (target_sample = treated):
    sum_{wi = 1} E[y(1) - y(0) | X = Xi] / |{i : wi = 1}|
    \item The (conditional) average treatment effect on the controls (target_sample = control):
    sum_{wi = 0} E[y(1) - y(0) | X = Xi] / |{i : wi = 0}|
    \item The overlap-weighted (conditional) average treatment effect
    sum_{i = 1}^n e(Xi) (1 - e(Xi)) E[y(1) - y(0) | X = Xi] / sum_{i = 1}^n e(Xi) (1 - e(Xi)),
    where e(x) = P[wi = 1 | Xi = x].
    }
    This last estimand is recommended by Li, Morgan, and Zaslavsky (JASA, 2017)
    in case of poor overlap (i.e., when the propensities e(x) may be very close
    to 0 or 1), as it doesn't involve dividing by estimated propensities.

    If clusters are specified, then each cluster gets equal weight. For example,
    if there are 10 clusters with 1 unit each and per-cluster ATE = 1, and there
    are 10 clusters with 19 units each and per-cluster ATE = 0, then the overall
    ATE is 0.5 (not 0.05).

    Parameters
    ----------
        forest : 
            The trained forest

        target_sample : str (default=all, also: treated, control, overlap)
            Which sample to aggregate treatment effects over

        method : str (default= AIPW, also: TMLE)
            Method used for doubly robust inference. Can be either
            augmented inverse-propensity weighting (AIPW), or
            targeted maximum likelihood estimation (TMLE)

        subset : np.ndarray (num_subset_units,)
            Specifies subset of the training examples over which we
            estimate the ATE. WARNING: For valid statistical performance,
            the subset should be defined only using features Xi, not using
            the treatment wi or the outcome yi

    Returns
    -------
        An estimate of the average treatment effect, along with standard error

    Example
    -------
        # Train a causal forest
        n = 50
        p = 10
        X = matrix(rnorm(n * p), n, p)
        w = rbinom(n, 1, 0.5)
        y = pmax(X[, 1], 0) * w + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
        causal_forest = causal_forest(X, y, w)

        # Predict using the forest.
        X_test = matrix(0, 101, p)
        X_test[, 1] = seq(-2, 2, len.out = 101)
        causal_predictions = causal_forest.predict(X_test)
        # Estimate the conditional average treatment effect on the full sample (CATE).
        causal_forest.average_treatment_effect(target_sample = "all")

        # Estimate the conditional average treatment effect on the treated sample (CATT).
        # We don't expect much difference between the CATE and the CATT in this example,
        # since treatment assignment was randomized.
        causal_forest.average_treatment_effect(target_sample = "treated")

        # Estimate the conditional average treatment effect on samples with positive X[,1].
        causal_forest.average_treatment_effect(target_sample = "all", X[, 1] > 0)
    """
                             
    target_sample = match_arg(target_sample) # Find Python equivalent
    method = match_arg(method)
    cluster_se = len(forest["clusters"]) > 0

    try:
        forest.__getattribute__('causal_forest')
    except AttributeError:
        raise AttributeError('Average effect estimation only implemented for causal_forest.')

    if cluster_se & method == "TMLE":
        print("TMLE has not yet been implemented with clustered observations.")
        return None

    if not subset:
        subset = list(range(len(forest["y_hat"])+1))[1:]

    if type(subset[0]) == 'bool' & len(subset) == len(forest["y_hat"]):
        subset = [i for i in list(range(len(forest["y_hat"]))) if subset[i]==True]

    if all(subset not in list(range(len(forest["y_hat"])))):
        ValueError(
            "If specified, subset must be a vector contained in 1:n,",
            "or a boolean vector of len n."
        )

    if cluster_se:
        clusters = forest["clusters"]
    else:
        clusters = list(range(len(forest["y_hat"])))

    observation_weight = observation_weights(forest)

    # Only use data selected via subsetting.
    subset_w = forest["w"].loc[subset, :]
    subset_w_hat = forest["w_hat"].loc[subset, :]
    subset_y = forest["y"].loc[subset, :]
    subset_y_hat = forest["y_hat"].loc[subset, :]
    tau_hat_pointwise = [i for i, e in enumerate(cf_predict(forest)["predictions"]) if e in subset]
    subset_clusters = [i for i, e in enumerate(clusters) if e in subset]
    subset_weights = [i for i, e in enumerate(observation_weight) if e in subset]

    # Address the overlap case separately, as this is a very different estimation problem.
    # The method argument (AIPW vs TMLE) is ignored in this case, as both methods are effectively
    # the same here. Also, note that the overlap-weighted estimator generalizes naturally to the
    # non-binary W case -- see, e.g., Robinson (Econometrica, 1988) -- and so we do not require
    # W to be binary here.

    if target_sample == "overlap":
        w_residual = subset_w - subset_w_hat
        y_residual = subset_y - subset_y_hat
        weighted_least_squares = sm.WLS(endog=y_residual, exog=w_residual, weights = subset_weights)
        tau_ols = weighted_least_squares.fit()
        tau_est = tau_ols.params[0]

        # Compute clustered covariance standard errors
        if cluster_se:
            tau_se = np.sqrt(sandwich_covariance(tau_ols, cluster = subset_clusters)[2, 2]) # Check [2,2]
        else:
            tau_se = np.sqrt(sandwich_covariance.cov_hac(tau_ols)[2, 2])

            return(list(estimate = tau_est, std_err = tau_se))

    if all(item not in subset_w for item in list(0, 1)):
        ValueError(
            "Average treatment effect estimation only implemented for binary treatment.",
            "See `average_partial_effect` for continuous treatments w."
        )

    if min(subset_w_hat) <= 0.01 & max(subset_w_hat) >= 0.99: 
        rng = range(subset_w_hat)
        print(
            "Estimated treatment propensities take values between ",
            round(rng[1], 3), " and ", round(rng[2], 3),
            " and in particular get very close to 0 and 1. ",
            "In this case, using `target_sample=overlap`, or filtering data as in ",
            "Crump, Hotz, Imbens, and Mitnik (Biometrika, 2009) may be helpful."
        )
    elif min(subset_w_hat) <= 0.01 & target_sample != "treated":
        print(
            "Estimated treatment propensities go as low as ",
            round(min(subset_w_hat), 3), " which means that treatment ",
            "effects for some controls may not be well identified. ",
            "In this case, using `target_sample=treated` may be helpful."
        )
    elif max(subset_w_hat) >= 0.99 & target_sample != "control": 
        print(
            "Estimated treatment propensities go as high as ",
            round(max(subset_w_hat), 3), " which means that treatment ",
            "effects for some treated units may not be well identified. ",
            "In this case, using `target_sample=control` may be helpful."
        )

    control_idx = [i for i in list(range(len(subset_w))) if subset_w[i]==0]
    treated_idx = [i for i in list(range(len(subset_w))) if subset_w[i]==1]

    # Compute naive average effect estimates (notice that this uses OOB)
    if target_sample == "all":
        tau_avg_raw = np.average(tau_hat_pointwise, weights=subset_weights)
    elif target_sample == "treated":
        tau_avg_raw = np.average(tau_hat_pointwise[treated_idx],
                                 weights=subset_weights[treated_idx]
        )
    elif (target_sample == "control"):
        tau_avg_raw = np.average(tau_hat_pointwise[control_idx],
                                 weights=subset_weights[control_idx]
        )
    else:
        print("Invalid target sample.")
        return None

    # Get estimates for the regress surfaces E[y|X, w=0/1]
    y_hat_0 = subset_y_hat - subset_w_hat * tau_hat_pointwise
    y_hat_1 = subset_y_hat + (1 - subset_w_hat) * tau_hat_pointwise

    if method == "TMLE":
        loaded = requireNamespace("sandwich", quietly = True) # Python equivalent
        if not loaded:
            print("To use TMLE, please install the package `sandwich`. Using AIPW instead.")
            method = "AIPW"

    # Now apply a doubly robust correction
    if method == "AIPW":

    # Compute normalized inverse-propensity-type weights gamma
        if (target_sample == "all"):
            gamma_control_raw = 1 / (1 - subset_w_hat[control_idx])
            gamma_treated_raw = 1 / subset_w_hat[treated_idx]
        elif (target_sample == "treated"):
            gamma_control_raw = subset_w_hat[control_idx] / (1 - subset_w_hat[control_idx])
            gamma_treated_raw = np.repeat(1, len(treated_idx))
        elif (target_sample == "control"):
            gamma_control_raw = np.repeat(1, len(control_idx))
            gamma_treated_raw = (1 - subset_w_hat[treated_idx]) / subset_w_hat[treated_idx]
        else:
            ValueError("Invalid target sample.")

        gamma = np.repeat(0, len(subset_w))
        gamma[control_idx] = gamma_control_raw / \
            sum(subset_weights[control_idx] * gamma_control_raw) * \
            sum(subset_weights)
        gamma[treated_idx] = gamma_treated_raw / \
            sum(subset_weights[treated_idx] * gamma_treated_raw) * \
            sum(subset_weights)

        dr_correction_all = subset_w * gamma * (subset_y - y_hat_1) \
                        - (1 - subset_w) * gamma * (subset_y - y_hat_0)
        dr_correction = np.average(dr_correction_all, weights=subset_weights)

        if (cluster_se):
            correction_clust = np.dot(csr_matrix(pd.Series(subset_clusters, dtype="category") + 0,).T, 
                                      (dr_correction_all * subset_weights))
            sigma2_hat = sum(correction_clust^2) / sum(subset_weights)^2 * \
                        len(correction_clust) / (len(correction_clust) - 1)
        else:
            sigma2_hat = np.mean(dr_correction_all^2) / (len(dr_correction_all) - 1)

    elif method == "TMLE":
    
        if target_sample == "all":
            A = 1 / (1 - subset_w_hat[subset_w == 0])
            B = subset_y[subset_w == 0] - y_hat_0[subset_w == 0]
            ols_0 = sm.OLS(endog=B, exog=A)
            ols_0_results = ols_0.fit()
            eps_tmle_robust_0 = ols_0_results.params[0]

            A = 1 / subset_w_hat[subset_w == 1]
            B = subset_y[subset_w == 1] - y_hat_1[subset_w == 1]
            ols_1 = sm.OLS(endog=B, exog=A)
            ols_1_results = ols_1.fit()
            eps_tmle_robust_1 = ols_1_results.params[0]

            delta_tmle_robust_0 = cf_predict(eps_tmle_robust_0, newdata = pd.DataFrame(A = np.mean(1 / (1 - subset_w_hat))))
            delta_tmle_robust_1 = cf_predict(eps_tmle_robust_1, newdata = pd.DataFrame(A = np.mean(1 / subset_w_hat)))
            dr_correction = delta_tmle_robust_1 - delta_tmle_robust_0
            
            # Use robust SE
            if cluster_se:
                sigma2_hat = sandwich_covariance(eps_tmle_robust_0, 
                                                cluster = subset_clusters[subset_w == 0]) * np.mean(1 / (1 - subset_w_hat))^2  \
                           + sandwich_covariance(eps_tmle_robust_1,
                                                 cluster = subset_clusters[subset_w == 1]) * np.mean(1 / subset_w_hat)^2
            
            else:
                sigma2_hat = sandwich_covariance(eps_tmle_robust_0) * np.mean(1 / (1 - subset_w_hat))^2 \
                           +  sandwich_covariance(eps_tmle_robust_1) * np.mean(1 / subset_w_hat)^2

        elif target_sample == "treated":
            A = subset_w_hat[subset_w == 0] / (1 - subset_w_hat[subset_w == 0])
            B = subset_y[subset_w == 0] - y_hat_0[subset_w == 0]
            ols_0 = sm.OLS(endog=B, Exog=A)
            ols_0_results = ols_0.fit()
            eps_tmle_robust_0 = ols_0_results.params[0]

            new_center = np.numericmean(subset_w_hat[subset_w == 1] / (1 - subset_w_hat[subset_w == 1]))
            delta_tmle_robust_0 = cf_predict(eps_tmle_robust_0,
                                          newdata = pd.DataFrame(A = new_center))

            dr_correction = -delta_tmle_robust_0
            if cluster_se:
                s_0 = sandwich_covariance(eps_tmle_robust_0, 
                                          cluster = subset_clusters[subset_w == 0]) * new_center^2
                delta_1 = np.dot(csr_matrix(pd.Series(subset_clusters[subset_w == 1], dtype="category") + 0,).T, 
                                 (subset_y[subset_w == 1] - y_hat_1[subset_w == 1]))
                s_1 = sum(delta_1^2) / sum(subset_w == 1) / (sum(subset_w == 1) - 1)
                sigma2_hat = s_0 + s_1
            else:
                sigma2_hat = sandwich_covariance(eps_tmle_robust_0) * new_center^2 \
                           + np.var(subset_y[subset_w == 1] - y_hat_1[subset_w == 1]) / sum(subset_w == 1)

        elif target_sample == "control":
            A = (1 - subset_w_hat[subset_w == 1]) / subset_w_hat[subset_w == 1]
            B = subset_y[subset_w == 1] - y_hat_1[subset_w == 1]
            ols_1 = sm.OLS(endog=B, exog=A)
            ols_1_results = ols_1.fit()
            eps_tmle_robust_1 = ols_1_results.params[0]

            new_center = np.mean((1 - subset_w_hat[subset_w == 0]) / subset_w_hat[subset_w == 0])
            delta_tmle_robust_1 = cf_predict(eps_tmle_robust_1, newdata = pd.DataFrame(A = new_center))

            dr_correction = delta_tmle_robust_1
            if cluster_se:
                delta_0 = np.dot(csr_matrix(pd.Series(subset_clusters[subset_w == 0], dtype="category") + 0,).T, 
                                 (subset_y[subset_w == 0] - y_hat_1[subset_w == 0]))
                s_0 = sum(delta_0^2) / sum(subset_w == 0) / (sum(subset_w == 0) - 1)
                s_1 = sandwich_covariance(eps_tmle_robust_1, 
                                          cluster = subset_clusters[subset_w == 1]) * new_center^2
                sigma2_hat = s_0 + s_1
            else:
                sigma2_hat = np.var(subset_y[subset_w == 0] - y_hat_0[subset_w == 0]) / sum(subset_w == 0) \
                           + sandwich_covariance(eps_tmle_robust_1) * new_center^2
        else:
            ValueError("Invalid target sample.")

    else:
        ValueError("Invalid method.")

    tau_avg = tau_avg_raw + dr_correction
    tau_se = np.sqrt(sigma2_hat)

    return list(estimate = tau_avg, std_err = tau_se)