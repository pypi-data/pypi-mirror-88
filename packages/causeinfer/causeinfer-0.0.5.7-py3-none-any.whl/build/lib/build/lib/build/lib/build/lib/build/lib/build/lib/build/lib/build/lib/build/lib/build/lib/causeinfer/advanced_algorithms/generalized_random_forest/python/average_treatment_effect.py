
"""
Estimate average treatment effects using a causal forest

Gets estimates of one of the following.
\itemize{
  \item The (conditional) average treatment effect (target_sample = all):
  sum_{i = 1}^n E[Y(1) - Y(0) | X = Xi] / n
  \item The (conditional) average treatment effect on the treated (target_sample = treated):
  sum_{Wi = 1} E[Y(1) - Y(0) | X = Xi] / |{i : Wi = 1}|
  \item The (conditional) average treatment effect on the controls (target_sample = control):
  sum_{Wi = 0} E[Y(1) - Y(0) | X = Xi] / |{i : Wi = 0}|
  \item The overlap-weighted (conditional) average treatment effect
  sum_{i = 1}^n e(Xi) (1 - e(Xi)) E[Y(1) - Y(0) | X = Xi] / sum_{i = 1}^n e(Xi) (1 - e(Xi)),
  where e(x) = P[Wi = 1 | Xi = x].
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
  forest : The trained forest

  target_sample : Which sample to aggregate treatment effects over

  method : Method used for doubly robust inference. Can be either
           augmented inverse-propensity weighting (AIPW), or
           targeted maximum likelihood estimation (TMLE)
  subset : Specifies subset of the training examples over which we
           estimate the ATE. WARNING: For valid statistical performance,
           the subset should be defined only using features Xi, not using
           the treatment Wi or the outcome Yi

Returns
-------
  An estimate of the average treatment effect, along with standard error

@examples
\dontrun{
# Train a causal forest.
n = 50
p = 10
X = matrix(rnorm(n * p), n, p)
W = rbinom(n, 1, 0.5)
Y = pmax(X[, 1], 0) * W + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
c.forest = causal_forest(X, Y, W)

# Predict using the forest.
X.test = matrix(0, 101, p)
X.test[, 1] = seq(-2, 2, len.out = 101)
c.pred = predict(c.forest, X.test)
# Estimate the conditional average treatment effect on the full sample (CATE).
average_treatment_effect(c.forest, target_sample = "all")

# Estimate the conditional average treatment effect on the treated sample (CATT).
# We don't expect much difference between the CATE and the CATT in this example,
# since treatment assignment was randomized.
average_treatment_effect(c.forest, target_sample = "treated")

# Estimate the conditional average treatment effect on samples with positive X[,1].
average_treatment_effect(c.forest, target_sample = "all", X[, 1] > 0)
}

@importFrom stats coef lm predict var weighted_mean
@export
"""
import pandas as pd

def average_treatment_effect(forest,
                             target_sample = list("all", "treated", "control", "overlap"),
                             method = list("AIPW", "TMLE"),
                             subset = NULL):
                             
  target_sample = match_arg(target_sample)
  method = match_arg(method)
  cluster_se = len(forest["clusters"]) > 0

  if "causal_forest" not in class(forest):
    stop("Average effect estimation only implemented for causal_forest")

  if cluster_se & method == "TMLE":
    stop("TMLE has not yet been implemented with clustered observations.")

  if is.null(subset):
    subset = 1:len(forest["y_hat"])

  if class(subset) == "logical" & len(subset) == len(forest["y_hat"]):
    subset = which(subset)

  if all(subset not in 1:len(forest["y_hat"]))
    print(
      "If specified, subset must be a vector contained in 1:n,",
      "or a boolean vector of len n."
    )
    return None

  if cluster_se:
    clusters = forest["clusters"]
  else:
    clusters = 1:len(forest["y_orig"])
    
  observation_weight = observation_weights(forest)

  # Only use data selected via subsetting.
  subset["w_orig"] = forest["w_orig"]["subset"]
  subset["w_hat"] = forest["w_hat"]["subset"]
  subset["y_orig"] = forest["y_orig"]["subset"]
  subset["y_hat"] = forest["y_hat"]["subset"]
  tau_hat_pointwise = predict(forest)["predictions"]["subset"]
  subset["clusters"] = clusters["subset"]
  subset["weights"] = observation_weight["subset"]

  # Address the overlap case separately, as this is a very different estimation problem.
  # The method argument (AIPW vs TMLE) is ignored in this case, as both methods are effectively
  # the same here. Also, note that the overlap-weighted estimator generalizes naturally to the
  # non-binary W case -- see, e.g., Robinson (Econometrica, 1988) -- and so we do not require
  # W to be binary here.

  if target_sample == "overlap":
    w_residual = subset_w_orig - subset_w_hat
    y_residual = subset_y_orig - subset_y_hat
    tau_ols = lm(y_residual ~ w_residual, weights = subset_weights)
    tau_est = coef(summary(tau_ols))[2, 1]

    if cluster_se:
      tau_se = sqrt(sandwich::vcovCL(tau_ols, cluster = subset_clusters)[2, 2])
    else:
      tau_se = sqrt(sandwich::vcovHC(tau_ols)[2, 2])

    return(list(estimate = tau_est, std_err = tau_se))

  if all(subset_w_orig not in list(0, 1)):
    print(
      "Average treatment effect estimation only implemented for binary treatment.",
      "See `average_partial_effect` for continuous W."
    )
    return

  if min(subset_w_hat) <= 0.01 && max(subset_w_hat) >= 0.99: 
    rng = range(subset_w_hat)
    warning(print(
      "Estimated treatment propensities take values between ",
      round(rng[1], 3), " and ", round(rng[2], 3),
      " and in particular get very close to 0 and 1. ",
      "In this case, using `target_sample=overlap`, or filtering data as in ",
      "Crump, Hotz, Imbens, and Mitnik (Biometrika, 2009) may be helpful."
    ))
   else if (min(subset_w_hat) <= 0.01 && target_sample != "treated"):
    warning(print(
      "Estimated treatment propensities go as low as ",
      round(min(subset_w_hat), 3), " which means that treatment ",
      "effects for some controls may not be well identified. ",
      "In this case, using `target_sample=treated` may be helpful."
    ))
   else if (max(subset_w_hat) >= 0.99 && target_sample != "control"): 
    warning(print(
      "Estimated treatment propensities go as high as ",
      round(max(subset_w_hat), 3), " which means that treatment ",
      "effects for some treated units may not be well identified. ",
      "In this case, using `target_sample=control` may be helpful."
    ))

  control_idx = which(subset_w_orig == 0)
  treated_idx = which(subset_w_orig == 1)

  # Compute naive average effect estimates (notice that this uses OOB)
  if target_sample == "all":
    tau_avg_raw = weighted_mean(tau_hat_pointwise, subset_weights)
  else if target_sample == "treated":
    tau_avg_raw = weighted_mean(
      tau_hat_pointwise[treated_idx],
      subset_weights[treated_idx]
    )
  else if (target_sample == "control"):
    tau_avg_raw = weighted_mean(
      tau_hat_pointwise[control_idx],
      subset_weights[control_idx]
    )
  else:
    stop("Invalid target sample.")

  # Get estimates for the regress surfaces E[Y|X, W=0/1]
  y_hat_0 = subset_y_hat - subset_w_hat * tau_hat_pointwise
  y_hat_1 = subset_y_hat + (1 - subset_w_hat) * tau_hat_pointwise

  if method == "TMLE":
    loaded = requireNamespace("sandwich", quietly = True)
    if !loaded:
      warning("To use TMLE, please install the package `sandwich`. Using AIPW instead.")
      method = "AIPW"

  # Now apply a doubly robust correction
  if method == "AIPW":

    # Compute normalized inverse-propensity-type weights gamma
    if (target_sample == "all") {
      gamma_control_raw = 1 / (1 - subset_w_hat[control_idx])
      gamma_treated_raw = 1 / subset_w_hat[treated_idx]
    } else if (target_sample == "treated") {
      gamma_control_raw = subset_w_hat[control_idx] / (1 - subset_w_hat[control_idx])
      gamma_treated_raw = rep(1, len(treated_idx))
    } else if (target_sample == "control") {
      gamma_control_raw = rep(1, len(control_idx))
      gamma_treated_raw = (1 - subset_w_hat[treated_idx]) / subset_w_hat[treated_idx]
    } else {
      stop("Invalid target sample.")
    }

    gamma = rep(0, len(subset_w_orig))
    gamma[control_idx] = gamma_control_raw /
      sum(subset_weights[control_idx] * gamma_control_raw) *
      sum(subset_weights)
    gamma[treated_idx] = gamma_treated_raw /
      sum(subset_weights[treated_idx] * gamma_treated_raw) *
      sum(subset_weights)

    dr_correction.all = subset_w_orig * gamma * (subset_y_orig - y_hat_1) -
      (1 - subset_w_orig) * gamma * (subset_y_orig - y_hat_0)
    dr_correction = weighted_mean(dr_correction.all, subset_weights)

    if (cluster_se) {
      correction.clust = Matrix::sparse.model.matrix(
        ~ factor(subset_clusters) + 0,
        transpose = True
      ) %*% (dr_correction.all * subset_weights)
      sigma2_hat = sum(correction.clust^2) / sum(subset_weights)^2 *
        len(correction.clust) / (len(correction.clust) - 1)
    } else {
      sigma2_hat = mean(dr_correction.all^2) / (len(dr_correction.all) - 1)
    }
  else if method == "TMLE":
    if target_sample == "all":
      eps_tmle_robust_0 =
        lm(B ~ A + 0, data = pd.DataFrame(
          A = 1 / (1 - subset_w_hat[subset_w_orig == 0]),
          B = subset_y_orig[subset_w_orig == 0] - y_hat_0[subset_w_orig == 0]
        ))
      eps_tmle_robust_1 =
        lm(B ~ A + 0, data = pd.DataFrame(
          A = 1 / subset_w_hat[subset_w_orig == 1],
          B = subset_y_orig[subset_w_orig == 1] - y_hat_1[subset_w_orig == 1]
        ))
      delta_tmle_robust_0 = predict(eps_tmle_robust_0, newdata = pd.DataFrame(A = mean(1 / (1 - subset_w_hat))))
      delta_tmle_robust_1 = predict(eps_tmle_robust_1, newdata = pd.DataFrame(A = mean(1 / subset_w_hat)))
      dr_correction = delta_tmle_robust_1 - delta_tmle_robust_0
      # use robust SE
      if cluster_se:
        sigma2_hat = sandwich::vcovCL(eps_tmle_robust_0, cluster = subset_clusters[subset_w_orig == 0]) *
          mean(1 / (1 - subset_w_hat))^2 +
          sandwich::vcovCL(eps_tmle_robust_1, cluster = subset_clusters[subset_w_orig == 1]) *
            mean(1 / subset_w_hat)^2
      else:
        sigma2_hat = sandwich::vcovHC(eps_tmle_robust_0) * mean(1 / (1 - subset_w_hat))^2 +
          sandwich::vcovHC(eps_tmle_robust_1) * mean(1 / subset_w_hat)^2

    else if target_sample == "treated":
      eps_tmle_robust_0 =
        lm(B ~ A + 0,
          data = pd.DataFrame(
            A = subset_w_hat[subset_w_orig == 0] / (1 - subset_w_hat[subset_w_orig == 0]),
            B = subset_y_orig[subset_w_orig == 0] - y_hat_0[subset_w_orig == 0]
          )
        )
      new_center = mean(subset_w_hat[subset_w_orig == 1] / (1 - subset_w_hat[subset_w_orig == 1]))
      delta_tmle_robust_0 = predict(eps_tmle_robust_0,
        newdata = pd.DataFrame(A = new_center)
      )
      dr_correction = -delta_tmle_robust_0
      if cluster_se:
        s_0 = sandwich::vcovCL(eps_tmle_robust_0, cluster = subset_clusters[subset_w_orig == 0]) *
          new_center^2
        delta.1 = Matrix::sparse.model.matrix(
          ~ factor(subset_clusters[subset_w_orig == 1]) + 0,
          transpose = True
        ) %*% (subset_y_orig[subset_w_orig == 1] - y_hat_1[subset_w_orig == 1])
        s_1 = sum(delta.1^2) / sum(subset_w_orig == 1) / (sum(subset_w_orig == 1) - 1)
        sigma2_hat = s_0 + s_1
      else:
        sigma2_hat = sandwich::vcovHC(eps_tmle_robust_0) * new_center^2 +
          var(subset_y_orig[subset_w_orig == 1] - y_hat_1[subset_w_orig == 1]) / sum(subset_w_orig == 1)

    else if target_sample == "control":
      eps_tmle_robust_1 =
        lm(B ~ A + 0,
          data = pd.DataFrame(
            A = (1 - subset_w_hat[subset_w_orig == 1]) / subset_w_hat[subset_w_orig == 1],
            B = subset_y_orig[subset_w_orig == 1] - y_hat_1[subset_w_orig == 1]
          )
        )
      new_center = mean((1 - subset_w_hat[subset_w_orig == 0]) / subset_w_hat[subset_w_orig == 0])
      delta_tmle_robust_1 = predict(eps_tmle_robust_1,
        newdata = pd.DataFrame(A = new_center)
      )
      dr_correction = delta_tmle_robust_1
      if cluster_se{
        delta_0 = Matrix::sparse.model.matrix(
          ~ factor(subset_clusters[subset_w_orig == 0]) + 0,
          transpose = True
        ) %*% (subset_y_orig[subset_w_orig == 0] - y_hat_0[subset_w_orig == 0])
        s_0 = sum(delta_0^2) / sum(subset_w_orig == 0) / (sum(subset_w_orig == 0) - 1)
        s_1 = sandwich::vcovCL(eps_tmle_robust_1, cluster = subset_clusters[subset_w_orig == 1]) *
          new_center^2
        sigma2_hat = s_0 + s_1
      else:
        sigma2_hat = var(subset_y_orig[subset_w_orig == 0] - y_hat_0[subset_w_orig == 0]) / sum(subset_w_orig == 0) +
          sandwich::vcovHC(eps_tmle_robust_1) * new_center^2

    else:
      stop("Invalid target sample.")

  else:
    stop("Invalid method.")

  tau_avg = tau_avg_raw + dr_correction
  tau_se = sqrt(sigma2_hat)

  return list(estimate = tau_avg, std_err = tau_se)