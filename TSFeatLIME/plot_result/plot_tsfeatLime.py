import pickle
import numpy as np
import pandas as pd

with open('../explanation_to_interface.pkl', 'rb') as f:
    explanations = pickle.load(f)


n=2 ###number of testing dataset
relevant_history = 12
explanation = explanations[n]
print(explanation)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

instance_prediction = explanation['model_prediction']
normalized_weights = (explanation['history_weights'] / np.mean(np.abs(explanation['history_weights'])))

fig, ax = plt.subplots(figsize=(15, 10))

feature_values = explanation['input_data'].iloc[-relevant_history:]
scores=normalized_weights.flatten()

print('feature_values',feature_values)
print(type(feature_values))
print('scores',scores)


###seperate score for lag/rolling window and extending window.
lags = ['lag(12,11,10)', 'lag(11,10,9)', 'lag(10,9,8)', 'lag(9,8,7)', 'lag(8,7,6)', 'lag(7,6,5)',
        'lag(6,5,4)', 'lag(5,4,3)', 'lag(4,3,2)', 'lag(3,2,1)']
lags_extend_window = ['lag(1...12)','lag(1...11)', 'lag(1...10)', 'lag(1...9)', 'lag(1...8)', 'lag(1...7)', 'lag(1...6)',
        'lag(1...5)', 'lag(1...4)']
lag_scores = scores[:12]
print('lag',lag_scores)
rolling_window_scores = scores[12:22]
print('rolling',rolling_window_scores)
extending_window_scores = scores[22:]
extending_window_scores = extending_window_scores[::-1]
print('extend',extending_window_scores)


print('extending_window_scores',extending_window_scores)
# Insert the first value of lag_scores at the start of extending_window_scores
# extending_window_scores = np.insert(extending_window_scores, 10, lag_scores[11])
# extending_window_scores = np.insert(extending_window_scores, 9, rolling_window_scores[9])
print('after extending_window_scores',extending_window_scores)

fig, ax = plt.subplots(3, 1, figsize=(10, 18))  # 3 rows, 1 column

# Plot for Lag features


# Plot for ax[0] (Lags)
ax[0].plot(feature_values.index, feature_values['Sales'], label='Input Time Series', marker='o', markerfacecolor='blue', markeredgecolor='blue', linestyle='--')
colors = ['blue' if value >= 0 else 'red' for value in lag_scores]
# ax[0].bar(feature_values.index, lag_scores, 0.4, color=colors)
ax[0].axhline(y=0, color='r', linestyle='-', alpha=0.4)
ax[0].set_title('Previous month weight (Lags)')
lag_labels = ['lag' + str(i) for i in range(12, 0, -1)]
ax[0].set_xticks(feature_values.index)
ax[0].set_xticklabels(lag_labels)

edgecolors = ['black' if i == 0 else 'none' for i in range(len(lag_scores))]
linewidths = [2 if i == 0 else 0 for i in range(len(lag_scores))]
ax[0].bar(feature_values.index, lag_scores, 0.4, color=colors, edgecolor=edgecolors, linewidth=linewidths)
y_pos = lag_scores[0] + 0.002 * max(lag_scores)
ax[0].text(feature_values.index[0], y_pos, 'seasonal lag', horizontalalignment='center', fontsize=10, color='black')
ax[0].legend(loc='upper right')

# Plot for Rolling Window features
ax[1].plot(lags, rolling_window_scores, marker='o', color='b', linestyle='-')
ax[1].set_title('Weight of Rolling Window Mean Values')
ax[1].set_xlabel('Lags')
ax[1].set_ylabel('Weight Value')
ax[1].grid(True, which='both', linestyle='--', linewidth=0.5)
ax[1].tick_params(axis='x', rotation=45)
ax[1].axhline(y=0, color='red', linestyle='--')
#
# # Plot for Extending Window features
ax[2].plot(lags_extend_window, extending_window_scores, marker='o', color='skyblue', linestyle='-')
ax[2].set_title('Weight of Extending Window Mean Values')
ax[2].set_xlabel('Lags (extending windows)')
ax[2].set_ylabel('Weight values')
ax[2].grid(axis='y', linestyle='--', linewidth=0.5)
ax[2].tick_params(axis='x', rotation=45)
ax[2].axhline(y=0, color='red', linestyle='--')
#
# Add title
instance_prediction = explanation['model_prediction']
fig.suptitle("Time Series Lime Explanation Plot for test point i={} with forecast={}".format(str(n), str(instance_prediction)), fontsize="x-large")


plt.tight_layout()  # Adjusts subplot parameters for better layout
plt.show()

differences = []

# Iterate over each explanation in the explanations list
for explanation in explanations:
    # Extract surrogate_prediction and model_prediction
    surrogate_prediction = explanation['surrogate_prediction']
    model_prediction = explanation['model_prediction']

    # Compute the difference and add it to the list
    difference = abs(surrogate_prediction - model_prediction)
    differences.append(difference)

# Calculate the mean of the differences
mean_difference = np.mean(differences)

print("Mean difference between surrogate_prediction and model_prediction:", mean_difference)