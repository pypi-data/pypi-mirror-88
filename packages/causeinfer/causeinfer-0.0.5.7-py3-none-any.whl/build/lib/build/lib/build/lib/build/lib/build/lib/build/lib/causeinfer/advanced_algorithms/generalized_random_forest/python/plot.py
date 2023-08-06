# =============================================================================
# Plotting functions
# 
# Contents
# --------
#   0. No Class
#       create_dot_body
#       export_graphviz
#       plot_grf_tree
# =============================================================================

def create_dot_body(tree, index = 1):
    """
    Writes each node information
    If it is a leaf node: show it in different color, show number of samples, show leaf id
    If it is a non-leaf node: show its splitting variable and splitting value

    Parameters
    ----------
        tree : the tree to convert
        index : the index of the current node
    """
    node = tree['nodes'][[index]]

    # Leaf case: print label only
    if (node['is_leaf']):
        num_samples = length(node['samples'])
        leaf_stats_text = ""
        if(np.isnotnull(node['leaf_stats'])):
            leaf_stats_text = paste("\n", paste(names(node['leaf_stats']), unname(node['leaf_stats']), sep = " = ", collapse = "\n"))
        
        line_label = paste(index - 1, ' [shape=box,style=filled,color=".7 .3 1.0" , label="size = ',
                            num_samples, leaf_stats_text, '"];')
        return(line_label)

    # Non-leaf case: print label, child edges
    if (np.isnotnull(node['left_child'])):
        edge = paste(index - 1, "->", node['left_child'] - 1)
        if (index == 1):
            edge_info_left = paste(edge, '[labeldistance=2.5, labelangle=45, headlabel="True"];')
        else:
            edge_info_left = paste(edge, " ;")

    else:
        edge_info_right = NULL

    if (np.isnotnull(node['right_child'])):
        edge = paste(index - 1, "->", node['right_child'] - 1)
        if (index == 1):
            edge_info_right = paste(edge, '[labeldistance=2.5, labelangle=-45, headlabel="False"]')
        else:
            edge_info_right = paste(edge, " ;")

    else:
        edge_info_right = NULL

    variable_name = tree.columns(node['split_variable'])
    node_info = paste(index - 1, '[label="', variable_name, "<=", round(node['split_value'], 2), '"] ;')

    this_lines = paste(node_info,
                       edge_info_left,
                       edge_info_right,
                       sep = "\n")

    left_child_lines = ifelse(np.isnotnull(node['left_child']),
                              create_dot_body(tree, index = node['left_child']), None)

    right_child_lines = ifelse(np.isnotnull(node['right_child']),
                               create_dot_body(tree, index = node['right_child']), None)

    lines = paste(this_lines, left_child_lines, right_child_lines, sep = "\n")

    return lines


def export_graphviz(tree):
    """
    Export a tree in DOT format.
    This function generates a GraphViz representation of the tree, which is then written into `dot_string`.
    
    Parameters
    ----------
        tree : 
            the tree to convert
    """
    header = "digraph nodes { \n node [shape=box] ;"
    footer = "}"
    body = create_dot_body(tree)

    dot_string = print(header, body, footer, sep = "\n")

    return(dot_string)


def plot_grf_tree(x, *args, **kwargs):
    """
    Plot a GRF tree object.
    
    Parameters
    ----------
        x : 
            The tree to plot

    Example
    -------
        # Save the plot of a tree in the causal forest.
        install.packages("DiagrammeR")
        install.packages("DiagrammeRsvg")
        n = 500
        p = 10
        X = matrix(rnorm(n * p), n, p)
        w = rbinom(n, 1, 0.5)
        y = pmax(X[, 1], 0) * w + X[, 2] + pmin(X[, 3], 0) + rnorm(n)
        causal_forest = causal_forest(X, y, w)
        # Save the first tree in the forest as plot.svg
        tree_plot = plot(get_tree(causal_forest, 1))
        cat(DiagrammeRsvg::export_svg(tree_plot), file='plot.svg')
    """
    if not installed "DiagrammeR" and quietly = True:
        EnvironmentError("Package \"DiagrammeR\" must be installed to plot trees.")

    dot_file = export_graphviz(x)
    DiagrammeR::grViz(dot_file)