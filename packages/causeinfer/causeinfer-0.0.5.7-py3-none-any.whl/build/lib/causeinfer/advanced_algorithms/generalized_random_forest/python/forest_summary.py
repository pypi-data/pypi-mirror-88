# =============================================================================
# Forest Summary
# 
# Based on
# --------
#   Chernozhukov, Victor, Mert Demirer, Esther Duflo, and Ivan Fernandez-Val.
#   "Generic Machine Learning Inference on Heterogenous Treatment Effects in
#   Randomized Experiments." arXiv preprint arXiv:1712.04802 (2017).
# 
# Contents
# --------
#   0. No Class
#       test_calibration
#       best_linear_projection
# =============================================================================
import pandas as pd
import statsmodels.api as sm

def test_calibration(forest):
    """
    Omnibus evaluation of the quality of the random forest estimates via calibration.

    Test calibration of the forest. Computes the best linear fit of the target
    estimand using the forest prediction (on held-out data) as well as the mean
    forest prediction as the sole two regressors. A coefficient of 1 for
    `mean_forest_prediction` suggests that the mean forest prediction is correct,
    whereas a coefficient of 1 for `differential_forest_prediction` additionally suggests
    that the forest has captured heterogeneity in the underlying signal.
    The p-value of the `differential_forest_prediction` coefficient
    also acts as an omnibus test for the presence of heterogeneity: If the coefficient
    is significantly greater than 0, then we can reject the null of
    no heterogeneity.

    Parameters
    ----------
        forest : The trained forest

    Returns
    -------
        A heteroskedasticity-consistent test of calibration

    Example
    -------
        n = 800
        p = 5
        X = matrix(rnorm(n * p), n, p)
        w = rbinom(n, 1, 0.25 + 0.5 * (X[, 1] > 0))
        y = pmax(X[, 1], 0) * w + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
        forest = causal_forest(X, y, w)
        test_calibration(forest)
    """
    observation_weight = observation_weights(forest)
    if len(forest['clusters']) > 0:
        clusters = forest['clusters']
    else:
        clusters = list(range(len(observation_weight)+1))[1:]

    if forest.__getattribute__('regression_forest'):
        preds = predict(forest)['predictions']
        mean_pred = weighted_mean(preds, observation_weight)
        df_forest = pd.DataFrame(target = unname(forest['y']), #???
                                 mean_forest_prediction = mean_pred,
                                 differential_forest_prediction = preds - mean_pred)

    elif forest.__getattribute__('causal_forest'):
        preds = predict(forest)['predictions']
        mean_pred = weighted_mean(preds, observation_weight)
        df_forest = pd.DataFrame(target = unname(forest['y'] - forest['y_hat']),
                                 mean_forest_prediction = unname(forest['w'] - forest['w_hat']) * mean_pred,
                                 differential_forest_prediction = unname(forest['w'] - forest['w_hat']) * (preds - mean_pred))
    else:
        print("Calibration check not supported for this type of forest.")
        return None

    best_linear_predictor = sm.WLS(endog=df_forest['target'], exog=df_forest['mean_forest_prediction']+df_forest['differential_forest_prediction'], weights = observation_weight)
    blp_summary = lmtest::coeftest(best_linear_predictor,vcov = sandwich::vcovCL,
                                   type = "HC3", cluster = clusters)

    attr(blp_summary, "method") =
    print("Best linear fit using forest predictions (on held-out data)",
          "as well as the mean forest prediction as regressors, along",
          "with one-sided heteroskedasticity-robust (HC3) SEs",
          sep = "\n"
    )
    # convert to one-sided p-values
    dimnames(blp_summary)[[2]][4] = gsub("[|]", "", dimnames(blp_summary)[[2]][4])
    blp_summary[, 4] = ifelse(blp_summary[, 3] < 0, 1 - blp_summary[, 4] / 2, blp_summary[, 4] / 2)
    blp_summary


 def best_linear_projection(forest, covariates = None, subset = None):
    """
    Estimate the best linear projection of a conditional average treatment effect
    using a causal forest.

    Let tau(Xi) = E[y(1) - y(0) | X = Xi] be the CATE, and Ai be a vector of user-provided
    covariates. This function provides a (doubly robust) fit to the linear model

    tau(Xi) ~ beta_0 + Ai * beta

    Procedurally, we do so be regressing doubly robust scores derived from the causal
    forest against the Ai. Note the covariates Ai may consist of a subset of the Xi,
    or they may be distince The case of the null model tau(Xi) ~ beta_0 is equivalent
    to fitting an average treatment effect via AIPW.

    Parameters
    ----------
        forest : 
            The trained forest

        covariates : np.ndarray : optional (default=None)
            The covariates we want to project the CATE onto

        subset : np.ndarray (num_subset_units,) : optional (default=None)
            Specifies subset of the training examples over which we
            estimate the ATE. WARNING: For valid statistical performance,
            the subset should be defined only using features Xi, not using
            the treatment Wi or the outcome Yi

    Returns
    -------
    An estimate of the best linear projection, along with coefficient standard errors.

    Example
    -------
        n = 800
        p = 5
        X = matrix(rnorm(n * p), n, p)
        w = rbinom(n, 1, 0.25 + 0.5 * (X[, 1] > 0))
        y = pmax(X[, 1], 0) * w + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
        forest = causal_forest(X, y, w)
        best_linear_projection(forest, X[,1:2])
    """
    # Check call for cluster standard errors
    if len(forest['clusters']) > 0:
        cluster_se = True

    if "causal_forest" not in class(forest):
        print("`best_linear_projection` is only implemented for `causal_forest`")
        return None

    if not subset:
        subset = list(range(len(forest['y_hat'])+1))[1:]

    if class(subset) == "logical" & len(subset) == len(forest['y_hat']):
        subset = which(subset)

    if not all(subset in list(range(len(forest['y_hat'])+1))[1:]):
    print(
        "If specified, subset must be a vector contained in 1:n,",
        "or a boolean vector of length n."
        )

    if cluster_se:
    clusters = forest['clusters']
    else:
        clusters = list(range(len(forest['y'])+1))[1:]
    
    observation_weight = observation_weights(forest)

    # Only use data selected via subsetting.
    subset_w = forest[w[subset]] # Subset is indexing
    subset_w_hat = forest[w_hat[subset]]
    subset_y = forest[y[subset]]
    subset_y_hat = forest[y_hat[subset]]
    tau_hat_pointwise = predict(forest)[predictions[subset]]
    subset.clusters = clusters[subset]
    subset_weights = observation_weight[subset]

    if min(subset_w_hat) <= 0.01 & max(subset_w_hat) >= 0.99:
        rng = range(subset_w_hat)
        print(
        "Estimated treatment propensities take values between ",
        round(rng[1], 3), " and ", round(rng[2], 3),
        " and in particular get very close to 0 and 1."
        )

    # Compute doubly robust scores
    mu_w_hat = subset_y_hat + (subset_w - subset_w_hat) * tau_hat_pointwise
    gamma_hat = tau_hat_pointwise \
              + (subset_w - subset_w_hat) \
              / (subset_w_hat * (1 - subset_w_hat)) \
              * (subset_y - mu_w_hat)

    if covariates:
        if (nrow(covariates) == len(forest['y'])):
            covariate_subset = covariates[subset,]
        elif nrow(covariates) == len(subset):
            covariate_subset = covariates
        else:
            print("The number of rows of covariates does not match the number of training examples.")
            return None

        if not colnames(covariate_subset):
            colnames(covariate_subset) = paste0("covariates", 1:ncol(covariates))
        DF = pd.DataFrame(target = gamma_hat, covariate_subset)
    else:
        df_gamma = pd.DataFrame(target = gamma_hat)

    blp_ols = lm(target ~ ., weights = subset_weights, data = df_gamma)
    blp_summary = lmtest::coeftest(blp_ols,
                                    vcov = sandwich::vcovCL,
                                    type = "HC3",
                                    cluster = subset.clusters
    )
    attr(blp_summary, "method") =
    
    print("Best linear projection of the conditional average treatment effect.",
            "Confidence intervals are cluster- and heteroskedasticity-robust (HC3)",
            sep="\n")

    blp_summary