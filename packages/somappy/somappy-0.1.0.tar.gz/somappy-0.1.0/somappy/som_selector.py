import os
import sys
import logging

import pandas

from . import somutils

LOGGER = logging.getLogger(__name__)

""" Som Pre Processer Model """
def execute(args):
    """Run a SOM configuration.

    Args:
        args['_output_dir_path_'] (string): path to a directory to save SOM 
            model outputs.
        args['_data_input_path_'] (string): path to a CSV file with the data
            to use in the SOM. Each row is a sample and each column is a 
            feature.
        args['_data_columns_excluded_'] (string): comma separated list of 
            columns from ``_data_input_path`` that should not be used as
            features in the SOM.
        args['_columns_'] (int): number of columns for the SOM model grid.
        args['_rows_'] (int): number of rows for the SOM model grid.
        args['_iterations_'] (int): number of iterations to run the SOM.
        args['_grid_type_'] (string): either 'hex' or 'square' for how the 
            SOM grid is interpeted and how distances are calculated.
        args['_number_clusters_'] (int): the number of clusters to sort the 
            output SOM weights into.

    Returns:
        Dictionary:
            'model_weights_path': path to a saved .txt with SOM weights
            'som_figure': pyplot figure of trained SOM
    """
    workspace_dir = args['_output_dir_path_']
    if not os.path.isdir(workspace_dir):
        os.makedirs(workspace_dir)

    data_path = args['_data_input_path_']

    data_dataframe = pandas.read_csv(data_path)
    data_dataframe.columns = data_dataframe.columns.str.lower()
    data_columns = data_dataframe.columns.values

    LOGGER.info(f"Input data columns lowercase: {data_columns}")
    excluded_columns = []
    if len(args['_data_columns_excluded_']) > 0:
        excluded_columns = [col.lower().strip() for col in args['_data_columns_excluded_'].split(',')]
    LOGGER.info(f"Data columns to exclude: {excluded_columns}")

    # Remove excluded columns from operable features.
    selected_features = list(set(data_columns) ^ set(excluded_columns))
    LOGGER.info(f"SOM data column features: {selected_features}")

    ## NOT IMPLEMENTED ##
    # Should be an input text box in GUI that takes a string for col name
    #validation_class_feat = ["class"]

    # The number of features for the SOM
    num_feats = len(selected_features)

    # Get only the data from the features of interest
    selected_data_feats_df = data_dataframe.loc[:, selected_features]
    LOGGER.debug(selected_data_feats_df.head(n=5))

    # Check to make sure feature columns are numeric
    non_numeric_cols_df = selected_data_feats_df.select_dtypes(exclude=['number'])
    if not non_numeric_cols_df.empty:
        raise ValueError(
            "SOM features must be numeric. The following feature columns were"
            f" not: {non_numeric_cols_df.columns.values}. Please add these"
            " to the excluded list.")

    LOGGER.info(f"Number of samples: {selected_data_feats_df.shape[0]}")
    # Handle NODATA / Missing data by removing (for now)
    selected_data_feats_df.dropna(how='any', inplace=True)
    LOGGER.info(
        "Number of samples after removing missing values:"
        f" {selected_data_feats_df.shape[0]}")

    # NORMALIZE DATA by min, max normalization approach
    selected_feats_df_norm = somutils.normalize(selected_data_feats_df)

    # Display statistics on our normalized data
    LOGGER.info("Normalized data stats:")
    LOGGER.info(selected_feats_df_norm.describe())

    # Initial learning rate for SOM. Will decay to 0.01 linearly
    init_learning_rate = 0.05

    # The number of rows for the grid and number of columns. This dictates
    # how many nodes the SOM will consist of. Currently not calculated
    # using PCA or other analyses methods.
    nrows = int(args['_rows_'])
    ncols = int(args['_columns_'])
    grid_type = args['_grid_type_']

    # Create the SOM grid (which initializes the SOM network)
    som_grid = somutils.create_grid(nrows, ncols, grid_type=grid_type)

    # Initial neighbourhood radius is defaulted to 2/3 of the longest distance
    # Should be set up similar to R package Kohonen
    # https://cran.r-project.org/web/packages/kohonen/kohonen.pdf
    # Radius will decay to 0.0 linearly
    init_radius = somutils.default_radius(som_grid)

    # Get the data as a matrix dropping the dataframe wrapper
    data = selected_feats_df_norm.values

    # Number of iterations to run SOM
    niter = int(args['_iterations_'])
    # Number of clusters to cluster SOM
    nclusters = int(args['_number_clusters_'])

    # Run SOM
    som_weights, object_distances = somutils.run_som(
        data, som_grid, grid_type, niter, init_radius, init_learning_rate)
    # Save SOM model. This is done by saving the weights (numpy ndarray)
    som_model_weights_path = os.path.join(
        workspace_dir, 'som_model_weights.txt')
    somutils.save_som_model(
        som_weights, som_model_weights_path, grid_type, cluster=nclusters)

    # It's possible that some data samples were not selected for training,
    # and do not have a latest BMU (best matching unit)
    object_distances = somutils.fill_bmu_distances(
        data, som_weights, object_distances)

    # Cluster SOM nodes
    clustering = somutils.cluster_som(som_weights, nclusters)

    # Let's save the clusters corresponding to the samples now
    results_path = os.path.join(workspace_dir, 'cluster_results.csv')
    somutils.save_cluster_results(
        selected_data_feats_df, results_path, clustering.labels_,
        (nrows, ncols), object_distances)
    # Display the SOM, coloring the nodes into different clusters from
    # 'clustering' above
    ## NOT IMLEMENTED keep ``class_name=None``##
    ## Optional: pass in original dataframe to plot the IDs onto their 
    ## respective nodes
    som_figure_path = os.path.join(workspace_dir, 'som_figure.jpg')
    plt = somutils.basic_som_figure(
        data, som_weights, som_grid, clustering.labels_, grid_type,
        som_figure_path, dframe=data_dataframe, class_name=None)

    return {
        'model_weights_path':som_model_weights_path, 'som_figure':plt.gcf()}
