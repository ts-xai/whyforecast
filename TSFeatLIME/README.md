# TSFeatELIME

TSFeatLIME integrates an auxiliary feature into the surrogate model and considers the pairwise Euclidean distances between the queried time series and the generated samples to improve the fidelity of the surrogate models.

## Folder Structure

This project includes the following directories:

`/dataset`: Stores raw data and preprocessing scripts or utilities. This directory is essential for data handling before it is fed into the models.

`/modelselection`: Used to evaluate and compare different black-box models to determine which model performs best for the specific requirements of the project.

`/tslime`: Contains the baseline implementation of the TSLIME algorithm.

`/tsfeatlime`: Hosts our custom algorithm, TSFEATLIME, which builds upon or modifies the baseline TSLIME to enhance its performance or suitability.

`/tsutils`: Includes various tools and utilities that support operations within both the TSLIME and TSFEATLIME directories.

`/results`: Stores outcomes from running TSLIME and TSFEATLIME algorithms. This folder is also used for selecting the best performing model for interface design based on the results.

`/plot_result`: Provides visualization of results. This directory contains scripts and output files for generating graphical representations that help in analyzing the performance and efficacy of the algorithms.



