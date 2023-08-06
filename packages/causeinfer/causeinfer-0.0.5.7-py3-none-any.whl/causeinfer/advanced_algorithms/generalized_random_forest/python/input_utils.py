# =============================================================================
# Input validation utilities
# 
# Contents
# --------
#   0. No Class
#       validate_X
#       validate_observations
#       validate_num_threads
#       validate_clusters
#       validate_samples_per_cluster
#       validate_boost_error_reduction
#       validate_ll_vars
#       validate_ll_lambda
#       validate_ll_path
#       validate_newdata
#       validate_sample_weights
#       create_data_matrices
#       observation_weights
#       do_call_rcpp
# =============================================================================
import pandas as pd
import numpy as np

def validate_X(X):
    if inherits(X, list("matrix", "pd.DataFrame") & not np.is_numeric(np.as_matrix(X))):
        print(
            "The feature matrix X must be numeric. GRF does not",
            "currently support non-numeric features. If factor variables",
            "are required, we recommend one of the following: Either",
            "represent the factor with a 1-vs-all expansion,",
            "(e.g., using model.matrix(~. , data=X)), or then encode the factor",
            "as a numeric via any natural ordering (e.g., if the factor is a month).",
            "For more on GRF and categorical variables see the online vignette:",
            "https://grf-labs.github.io/grf/articles/categorical_inputs.html"
        )
        return None

    if inherits(X, "Matrix") & not (inherits(X, "dgCMatrix")):
        print("Currently only sparse data of class 'dgCMatrix' is supported.")
        return None # Does this need to be changed to throw an error?

    if any(pd.isna(X)):
        print("The feature matrix X contains at least one NA.")
        return None


def validate_observations(V, X):
    if np.is_matrix(V) & ncol(V) == 1):
        V = np.array(V)
    elif type(V) != numpy.ndarray:
        print("Observations (w, y, or zs) must be vectors.")
        return None

    if not np.is_numeric(V) & not np.is_logical(V):
        print(
            "Observations (w, y, or z) must be numeric. GRF does not ",
            "currently support non-numeric observations."
        )

    if any(pd.isna(V)):
        print("The vector of observations (w, y, or z) contains at least one NA.")
        return None

    if len(V) != nrow(X):
        print("Length of observation (W, Y, or Z) does not equal nrow(X).")
        return None
    
    return V


 def validate_num_threads(num_threads):
    if np.isnan(num_threads):
        num_threads = 0
    elif not np.is_numeric(num_threads) | num_threads < 0:
        ValueError("Error: Invalid value for num_threads")

    return num_threads


def validate_clusters(clusters, X):
    if np.isnan(clusters) | len(clusters) == 0:
        return(vector(mode = "numeric", length = 0))
    if mode(clusters) != "numeric":
        ValueError("Clusters must be able to be coerced to a numeric vector.")

    clusters = np.numeric(clusters)

    if not all(clusters == floor(clusters)):
        ValueError("Clusters vector cannot contain floating point values.")
    elif len(clusters) != nrow(X):
        ValueError("Clusters vector has incorrect length.")
    else:
        # Convert to integers between 0 and n clusters
        clusters = np.numeric(np.as_factor(clusters)) - 1

    return clusters


def validate_samples_per_cluster(samples_per_cluster, clusters):
    if np.isnan(clusters) | len(clusters) == 0:
        return 0

    cluster_size_counts = pd.DataFrame(clusters)
    min_size = unname(cluster_size_counts[order(cluster_size_counts)][1])

    if np.isnan(samples_per_cluster):
        samples_per_cluster = min_size
    elif samples_per_cluster <= 0:
        ValueError("samples_per_cluster must be positive")

    return samples_per_cluster


def validate_boost_error_reduction(boost_error_reduction) {
    if boost_error_reduction < 0 | boost_error_reduction > 1:
        ValueError("boost_error_reduction must be between 0 and 1")

    return boost_error_reduction


def validate_ll_vars(linear_correction_variables, num_cols):
    if np.isnan(linear_correction_variables):
        linear_correction_variables = list(range(num_cols+1))[1:]

    if min(linear_correction_variables) < 1:
        ValueError("Linear correction variables must take positive integer values.")
    elif max(linear_correction_variables) > num_cols):
        ValueError("Invalid range of correction variables.")
    elif not np.is_vector(linear_correction_variables) | not all(linear_correction_variables == floor(linear_correction_variables)):
        ValueError("Linear correction variables must be a vector of integers.")

    return linear_correction_variables


def validate_ll_lambda(ll_lambda):
    if ll_lambda < 0:
        ValueError("Lambda cannot be negative.")
    elif not np.is_numeric(ll_lambda) | len(ll_lambda) > 1):
        ValueError("Lambda must be a scalar.")

    return ll_lambda


def validate_ll_path(lambda_path):
    if np.isnan(lambda_path):
        lambda_path = c(0, 0.001, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1, 10)

    elif (min(lambda_path) < 0):
        ValueError("Lambda values cannot be negative.")
    elif not np.is_numeric(lambda_path):
        ValueError("Lambda values must be numeric.")
    
    return lambda_path


def validate_newdata(newdata, X):
    if newdata.shape[1] != X.shape[1]:
        ValueError("newdata must have the same number of columns as the training matrix.")

    return validate_X(newdata)


def validate_sample_weights(sample_weights, X):
    if not np.isnan(sample_weights):
        if len(sample_weights) != X.shape[0]:
            ValueError("sample_weights has incorrect length")
        if any(sample_weights < 0):
            ValueError("sample_weights must be nonnegative")

    return sample_weights


#' @importFrom Matrix Matrix cBind
#' @importFrom methods new
def create_data_matrices(X, outcome = None, treatment = None,
                         instrument = None, sample_weights = False):
  
    default_data = matrix(nrow = 0, ncol = 0)
    sparse_data = new("dgCMatrix", Dim = c(0L, 0L))

    out = list()
    i = 1
    if not np.isnan(outcome):
        out[["outcome_index"]] = X.shapep[1] + i
    
    if not np.isnan(treatment):
        i = i + 1
        out[["treatment_index"]] = X.shapep[1] + i
    
    if not np.isnan(instrument):
        i = i + 1
        out[["instrument_index"]] = X.shapep[1] + i
    
    if sample_weights != False:
        i = i + 1
        out[["sample_weight_index"]] = X.shapep[1] + i
        if np.isnan(sample_weights):
            out[["use_sample_weights"]] = False
        else:
            out[["use_sample_weights"]] = True
    else:
        sample_weights = None

    if inherits(X, "dgCMatrix") & X.shape[0] > 1:
        sparse_data = cbind(X, outcome, treatment, instrument, sample_weights)
    else:
        X = np.as_matrix(X)
        default_data = np.as_matrix(cbind(X, outcome, treatment, instrument, sample_weights))
    
    out[["train_matrix"]] = default_data
    out[["sparse_train_matrix"]] = sparse_data

    return out


def observation_weights(forest):
    if forest['sample_weights'] == None:
        sample_weights = rep(1, len(forest['y']))
    else:
        sample_weights = forest['sample_weights'] * len(forest['y']) / sum(forest['sample_weights'])

    if len(forest['clusters']) == 0:
        observation_weight = sample_weights
    else:
        cluster_factor = np.to_factor(forest['clusters'])
        inverse_counts = 1 / np.numeric(Matrix::colSums(Matrix::sparse_model_matrix(~ cluster_factor + 0)))
        observation_weight = sample_weights * inverse_counts[np.numeric(cluster_factor)]

    return observation_weight


# All the bindings argument names (C++) have underscores: sample_weights, train_matrix, etc.
# On the original R side each variable name is written as sample.weights, train.matrix, etc.
# On the python side, the underscores are maintained - this function is not necessary in CauseInfwe.
# This function simply replaces the underscores in the passed argument names with dots.
def do_call_rcpp(what, args, quote = False, envir = parent.frame()):
    """Not necessary, as Python and CPP naming criteria are the same"""
    names(args) = gsub("\\.", "_", names(args))
    do.call(what, args, quote, envir)