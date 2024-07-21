import functools
from tslime.tslime import TSLimeExplainer
from tsutils.tsperturbers import BlockBootstrapPerturber
from tsutils.tsperturbers import MovingAveragePerturber
from buildModel import build_model_forecaster
import pandas as pd
import numpy as np
import random
import pickle
from sklearn.preprocessing import MinMaxScaler

differences = {}
best_explanation_collection = None
best_average_difference = float('inf')
best_seed = None

## list the random seeds
random_seeds = [42, 52, 62, 72, 82, 92]
block_lengths = [3, 4, 5]
block_swaps = [2, 3, 4]

def run_experiment(block_length, block_swap):
    total_difference_across_all_runs = 0
    total_difference_across_all_runs_MSE = 0
    total_difference_across_all_runs_MAPE = 0
    best_average_difference = float('inf')  # Initialize the variable


    for seed in random_seeds:
        np.random.seed(seed)
        random.seed(seed)
        f_model,train, model_stacked,df,scaler = build_model_forecaster(seed_value=seed)
        relevant_history = 12
        sequence_length = 12
        input_length = 12
        n_input = 12
        n_features = 1
        explanation_collection = []
        explainer = TSLimeExplainer(
                model=functools.partial(f_model.predict, verbose=0),
                input_length=sequence_length,
                relevant_history=relevant_history,
                perturbers=[
                    ####initial block-length==4
                    BlockBootstrapPerturber(window_length=min(10, sequence_length - 1), block_length=block_length, block_swap=block_swap),
                ],
                n_perturbations=1000,
                random_seed=22,
                use_weight=True,
            )

        pred_list_s = []
        batch = train[-n_input:].reshape((1, n_input, n_features))
        for j in range(n_input):
            pred_list_s.append(model_stacked.predict(batch)[0])
              # print('batch-before',batch)
            batch = np.append(batch[:,1:,:],[[pred_list_s[j]]],axis=1)
            print(batch)
            ###convert the format of batch
            batch_instance = batch.flatten()
            instance = pd.DataFrame(batch_instance, columns=['Sales'])
            instance.index.name = 'Index'

            explanation = explainer.explain_instance(instance)
            explanation_collection.append(explanation)
        print(explanation_collection)
        total_difference = 0
        total_difference_MSE = 0
        total_difference_MAPE = 0

        for i in explanation_collection:
             model_pred = i['model_prediction'][0]
             surrogate_pred = i['surrogate_prediction'][0][0]
             total_difference += abs(model_pred - surrogate_pred)
             total_difference_MSE += (model_pred - surrogate_pred) ** 2
             total_difference_MAPE += abs(model_pred - surrogate_pred) / model_pred

        average_difference = total_difference / len(explanation_collection)
        total_difference_across_all_runs += average_difference
        print(f"For seed {seed}, average difference is: {average_difference}")

        average_difference_MSE = total_difference_MSE /len(explanation_collection)
        total_difference_across_all_runs_MSE += average_difference_MSE

        average_difference_MAPE = total_difference_MAPE / len(explanation_collection)
        total_difference_across_all_runs_MAPE += average_difference_MAPE

        differences[seed] = average_difference
        if average_difference < best_average_difference:
            best_average_difference = average_difference
            best_explanation_collection = explanation_collection
            best_seed = seed

    final_avg_difference = total_difference_across_all_runs / len(random_seeds)
    final_avg_difference_MSE = total_difference_across_all_runs_MSE / len(random_seeds)
    final_avg_difference_MAPE = total_difference_across_all_runs_MAPE / len(random_seeds)
    return final_avg_difference, final_avg_difference_MSE, final_avg_difference_MAPE, block_length, block_swap



results = []
for block_length in block_lengths:
    for block_swap in block_swaps:
        avg_diff, avg_diff_MSE, avg_diff_MAPE, bl, bs = run_experiment(block_length, block_swap)
        results.append({
            'Block Length': bl,
            'Block Swap': bs,
            'Average Difference': avg_diff,
            'Average Difference MSE': avg_diff_MSE,
            'Average Difference MAPE': avg_diff_MAPE
        })

# Convert results to DataFrame and save as CSV
results_df = pd.DataFrame(results)
results_df.to_csv('experiment_results.csv', index=False)

print("Experiments completed and results saved in CSV.")


