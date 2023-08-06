
# =============================================================================
# Tuning for causal tree based models
# 
# Contents
# --------
#   0. No Class
#       tune_forest
#       get_params_from_draw
#       get_tuning_output
# =============================================================================

import pandas as pd

def tune_forest(data,
                nrow_X,
                ncol_X,
                args,
                tune_parameters,
                tune_parameters_defaults,
                num_fit_trees,
                num_fit_reps,
                num_optimize_reps,
                train,
                predict_oob,
                predict_data_args):
    """
    Tune a forests

    Finds the optimal parameters to be used in training a forest.

    Parameters
    ----------
        data : 
            The data arguments (output from create_data_matrices) for the forest

        nrow_X : 
            The number of observations

        ncol_X : 
            The number of variables

        args : 
            The remaining call arguments for the forest

        tune_parameters : 
            The vector of parameter names to tune

        tune_parameters_defaults : 
            The grf default values for the vector of parameter names to tune

        num_fit_trees : 
            The number of trees in each 'mini forest' used to fit the tuning model

        num_fit_reps : 
            The number of forests used to fit the tuning model

        num_optimize_reps : 
            The number of random parameter values considered when using the model to select the optimal parameters

        train : 
            The grf forest training function

        predict_oob : 
            The grf forest oob prediction function

        predict_data_args : 
            The names of the arguments in data passed to predict_oob

    Returns
    -------
        tuning output

    @importFrom stats sd runif
    @importFrom utils capture_output
    """
    predict_oob_args = c(data[predict_data_args], num_threads = args[["num_threads"]], estimate_variance = False)
    fit_parameters = args[!names(args) in tune_parameters]
    fit_parameters[["num_trees"]] = num_fit_trees
    fit_parameters[["ci_group_size"]] = 1
    fit_parameters[["compute_oob_predictions"]] = True

    # 1. Train several mini-forests, and gather their debiased OOB error estimates.
    num_params = length(tune_parameters)
    fit_draws = matrix(runif(num_fit_reps * num_params), num_fit_reps, num_params,
                        dimnames = list(None, tune_parameters))

    small_forest_errors = apply(fit_draws, 1, function(draw) {
    draw_parameters = get_params_from_draw(nrow_X, ncol_X, draw)
    small_forest = do_call_rcpp(train, c(data, fit_parameters, draw_parameters))
    prediction = do_call_rcpp(predict_oob, c(list(forest_object = small_forest), predict_oob_args))
    error = prediction['debiased_error']

    mean(error, na.rm = True)
    })

    if any(np.isnan(small_forest_errors)):
    ValueError(
        "Could not tune forest because some small forest error estimates were NA.\n",
        "Consider increasing tuning argument num_fit_trees.")
    
    out = get_tuning_output(params = c(tune_parameters_defaults), status = "failure")
    
    return out

    if np.get_std(small_forest_errors) == 0 | np.get_std(small_forest_errors) / mean(small_forest_errors) < 1e-10:
    ValueError(
        "Could not tune forest because small forest errors were nearly constant.\n",
        "Consider increasing argument num_fit_trees.")
    
    out = get_tuning_output(params = c(tune_parameters_defaults), status = "failure")
    
    return out

    # 2. Fit the 'dice kriging' model to these error estimates.
    variance_guess = rep(var(small_forest_errors) / 2, fit_draws.shape[0])
    kriging_model = tryCatch({
    capture_output(
        model = DiceKriging::km(
        design = pd.DataFrame(fit_draws),
        response = small_forest_errors,
        noise_var = variance_guess
        )
    )
    model
    },
    error = function(e) {
    ValueError(("Dicekriging threw the following error during forest tuning: \n", e)
    return None
    })

    if np.isnan(kriging_model):
        ValueError("Forest tuning was attempted but failed. Reverting to default parameters.")
        
        out = get_tuning_output(params = c(tune_parameters_defaults), status = "failure")
    
    return out

    # 3. To determine the optimal parameter values, predict using the kriging model at a large
    # number of random values, then select those that produced the lowest error.
    optimize_draws = matrix(runif(num_optimize_reps * num_params), num_optimize_reps, num_params,
                            dimnames = list(None, tune_parameters))
    model_surface = predict(kriging_model, newdata = pd.DataFrame(optimize_draws), type = "SK")['mean']
    tuned_params = get_params_from_draw(nrow_X, ncol_X, optimize_draws)
    grid = cbind(error = c(model_surface), tuned_params)
    small_forest_optimal_draw = which.min(grid[, "error"])

    # To avoid the possibility of selection bias, re-train a moderately-sized forest
    # at the value chosen by the method above
    fit_parameters[["num_trees"]] = num_fit_trees * 4
    retrained_forest_params = grid[small_forest_optimal_draw, -1]
    retrained_forest = do_call_rcpp(train, c(data, fit_parameters, retrained_forest_params))
    retrained_forest_prediction = do_call_rcpp(predict_oob, c(list(forest_object = retrained_forest), predict_oob_args))
    retrained_forest_error = mean(retrained_forest_prediction['debiased_error'], na.rm = True)

    # 4. Train a forest with default parameters, and check its predicted error.
    # This improves our chances of not doing worse than default
    default_forest = do_call_rcpp(train, c(data, fit_parameters, tune_parameters_defaults))
    default_forest_prediction = do_call_rcpp(predict_oob, c(list(forest_object = default_forest), predict_oob_args))
    default_forest_error = mean(default_forest_prediction$debiased_error, na.rm = True)

    if (default_forest_error < retrained_forest_error):
        out = get_tuning_output(
        error = default_forest_error,
        params = tune_parameters_defaults,
        grid = None,
        status = "default"
    )
    else:
    out = get_tuning_output(
        error = retrained_forest_error,
        params = retrained_forest_params,
        grid = grid,
        status = "tuned"
    )

    return out


def get_params_from_draw(nrow_X, ncol_X, draws):
    if np.is_vector(draws):
        draws = rbind(c(draws))

    n = draws.shape[0]
    vapply(colnames(draws), function(param) {
    if param == "min_node_size"):
        return(floor(2^(draws[, param] * (log(nrow_X) / log(2) - 4))))
    
    elif (param == "sample_fraction"):
        return(0.05 + 0.45 * draws[, param])
    
    elif (param == "mtry"):
        return(ceiling(min(ncol_X, sqrt(ncol_X) + 20) * draws[, param]))
    
    elif (param == "alpha"):
        return(draws[, param] / 4)
    
    elif (param == "imbalance_penalty"):
        return(-log(draws[, param]))
    
    elif (param == "honesty_fraction"):
        return(0.5 + (0.8 - 0.5) * draws[, param]) # honesty_fraction in U(0.5, 0.8)
    
    elif (param == "honesty_prune_leaves"):
        return(ifelse(draws[, param] < 0.5, True, False))
    else:
        ValueError("Unrecognized parameter name provided: ", param)
    }, fun_value = numeric(n))


def get_tuning_output(status, params, error = None, grid = None):
  out = list(status = status, params = params, error = error, grid = grid)
  class(out) = c("tuning_output")
  
  return out