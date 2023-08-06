"""
Estimate average partial effects using a causal forest

Gets estimates of the average partial effect, in particular
the (conditional) average treatment effect (target.sample = all):
  1/n sum_{i = 1}^n Cov[Wi, Yi | X = Xi] / Var[Wi | X = Xi].
Note that for a binary unconfounded treatment, the
average partial effect matches the average treatment effect.

If clusters are specified, then each cluster gets equal weight. For example,
if there are 10 clusters with 1 unit each and per-cluster APE = 1, and there
are 10 clusters with 19 units each and per-cluster APE = 0, then the overall
APE is 0.5 (not 0.05).

Parameters
----------
  forest : The trained forest

  calibrate_weights : Whether to force debiasing weights to match expected
                      moments for 1, W, ["w_hat"], and 1/Var[W|X]

  subset : Specifies a subset of the training examples over which we
           estimate the ATE. WARNING: For valid statistical performance,
           the subset should be defined only using features Xi, not using
           the treatment Wi or the outcome Yi

  num_trees_for_variance : Number of trees used to estimate Var[Wi | Xi = x]. Default is 500

Returns
-------
  An estimate of the average partial effect, along with standard error

@examples
\dontrun{
n = 2000
p = 10
X = matrix(rnorm(n * p), n, p)
W = rbinom(n, 1, 1 / (1 + exp(-X[, 2]))) + rnorm(n)
Y = pmax(X[, 1], 0) * w + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
tau.forest = causal_forest(X, y, w)
tau_hat = predict(tau.forest)
average_partial_effect(tau.forest)
average_partial_effect(tau.forest, subset = X[, 1] > 0)
}

@export
"""

def average_partial_effect(forest,
                           calibrate_weights = True,
                           subset = None,
                           num_trees_for_variance = 500):

  if "causal_forest" not in class(forest):
    stop("Average effect estimation only implemented for causal_forest")
  
  if is.null(subset):
    subset = 1:len(forest["y_hat"])
  
  if class(subset) == "logical" & len(subset) == len(forest["y_hat"]):
    subset = which(subset)
  
  if all(subset not in 1:len(forest["y_hat"]))):
    print(
      "If specified, subset must be a vector contained in 1:n,",
      "or a boolean vector of len n."
    )
    return None
  
  cluster.se = len(forest["clusters"]) > 0 # Needs to be looked at
  if cluster.se:
    clusters =  forest["clusters"]
  else:
    clusters = 1:len(forest["y_hat"])

  observation_weight = observation_weights(forest)

  # Only use data selected via subsetting
  subset["X_orig"] = forest["X_orig"]["subset", , drop = FALSE]
  subset["w_orig"] = forest["w_orig"]["subset"]
  subset["w_hat"] = forest["w_hat"]["subset"]
  subset["y_orig"] = forest["y_orig"]["subset"]
  subset["y_hat"] = forest["y_hat"]["subset"]
  tau_hat = predict(forest)["predictions"]["subset"]
  subset["clusters"] = clusters["subset"]
  subset_weights = observation_weight["subset"]

  # This is a simple plugin estimate of the APE
  cape_plugin = weighted_mean(tau_hat, subset_weights)

  # Estimate the variance of W given X. For binary treatments,
  # we get a good implicit estimator V_hat = e_hat (1 - e_hat), and
  # so this step is not needed. Note that if we use the present CAPE estimator
  # with a binary treatment and set V_hat = e_hat (1 - e_hat), then we recover
  # exactly the AIPW estimator of the CATE
  variance_forest = regression_forest(subset["X_orig"],
    (subset["w_orig"] - subset["w_hat"])^2,
    clusters = subset["clusters"],
    num_trees = num_trees_for_variance
  )
  V_hat = predict(variance_forest)["predictions"]
  debiasing_weights = subset_weights * (subset["w_orig"] - subset["w_hat"]) / V_hat

  # In the population, we want A' %*% weights = b
  # Modify debiasing weights gamma to make this True, i.e., compute
  # argmin {||gamma - gamma_original||_2^2 : A'gamma = b}
  if calibrate_weights:
    A = cbind(1, subset["w_orig"], subset["w_hat"]) / sum(subset_weights)
    b = list(0, 1, 0)
    bias = t(A) %*% debiasing_weights - b
    lambda = solve(t(A) %*% A, bias)
    correction = A %*% lambda
    debiasing_weights = debiasing_weights - correction

  # Compute a residual-based correction to the plugin.
  plugin_prediction = subset["y_hat"] + (subset["w_orig"] - subset["w_hat"]) * tau_hat
  plugin_residual = subset["y_orig"] - plugin_prediction
  cape_correction = mean(debiasing_weights * plugin_residual)
  cape_estimate = cape_plugin + cape_correction

  # Estimate variance using the calibration
  if len(subset["clusters"]) == 0:
    cape.se = sqrt(mean((debiasing_weights * plugin_residual)^2) / (len(subset["w_orig"]) - 1))
  else:
    debiasing_clust = Matrix::sparse_model_matrix(
      ~ factor(subset["clusters"]) + 0,
      transpose = True
    ) %*% (debiasing_weights * plugin_residual)
    cape.se = sqrt(sum(debiasing_clust^2) / len(debiasing_clust) /
      (len(debiasing_clust) - 1))

  return list(estimate = cape_estimate, std_err = cape.se)