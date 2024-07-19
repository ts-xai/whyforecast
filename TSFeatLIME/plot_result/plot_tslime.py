import pickle
import numpy as np
import pandas as pd

with open('../best_explanation_collection.pkl', 'rb') as f:
    explanations = pickle.load(f)
print('explanation_tslime',explanations)

n=0 ###number of testing dataset
relevant_history = 12
explanation = explanations[n]
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

# ax.plot(feature_values.index, feature_values, label='Input Time Series', marker='o', markerfacecolor='blue', markeredgecolor='blue')
# ax.set_title('Previous month weight')
# colors = ['blue' if value >= 0 else 'red' for value in scores]
# ax.bar(feature_values.index, scores, 0.4, label='TSLime Weights (Normalized)', color=colors)
# ax.axhline(y=0, color='r', linestyle='-', alpha=0.4)


ax.plot(feature_values.index, feature_values['Sales'], label='Input Time Series', marker='o', markerfacecolor='blue', markeredgecolor='blue', linestyle='--')
colors = ['blue' if value >= 0 else 'red' for value in scores]
ax.bar(feature_values.index, scores, 0.4, color=colors)
ax.axhline(y=0, color='r', linestyle='-', alpha=0.4)
ax.set_title('Previous month weight (Lags)')
lag_labels = ['lag' + str(i) for i in range(12, 0, -1)]
ax.set_xticks(feature_values.index)
ax.set_xticklabels(lag_labels)

ax.legend(loc='upper right')

# Add title
instance_prediction = explanation['model_prediction']
fig.suptitle("Time Series Lime Explanation Plot for test point i={} with forecast={}".format(str(n), str(instance_prediction)), fontsize="x-large")

# Show the plot
plt.show()


# def generate_summary(feature_values: pd.DataFrame, scores: list) -> str:
#     # Ensure both inputs are properly aligned in size
#     if len(feature_values) != len(scores):
#         return "The length of feature values and scores do not match."
#
#     # Map index to its "lag" meaning
#     index_to_lag = {i: "lag" + str(12 - i) for i in range(12)}
#
#     # Sort the scores and get their indices
#     sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
#
#     # Get the top 3 positive weights and their indices
#     top3_positive_indices = sorted_indices[:3]
#     top3_positive_scores = [scores[i] for i in top3_positive_indices]
#     top3_positive_values = [feature_values.iloc[i]['Sales'] for i in top3_positive_indices]
#
#     # Get the top 3 negative weights and their indices
#     top3_negative_indices = sorted_indices[-3:]
#     top3_negative_scores = [scores[i] for i in top3_negative_indices]
#     top3_negative_values = [feature_values.iloc[i]['Sales'] for i in top3_negative_indices]
#
#     # Generate the summary
#     summary = "In predicting the sales, the three most influential factors that positively impacted the prediction were:\n"
#     for i in range(3):
#         summary += f"{i+1}. Sales from {index_to_lag[top3_positive_indices[i]]} ({top3_positive_values[i]:.2f}) with a weight of approximately {top3_positive_scores[i]:.2f}.\n"
#
#     summary += "\nOn the other hand, the factors that negatively impacted the prediction the most were:\n"
#     for i in range(3):
#         summary += f"{i+1}. Sales from {index_to_lag[top3_negative_indices[i]]} ({top3_negative_values[i]:.2f}) with a weight of approximately {top3_negative_scores[i]:.2f}.\n"
#
#     summary += "\nThis means that sales from longer ago have more positive influence on the current prediction, while more recent sales tend to decrease the prediction."
#
#     return summary
#
# print(generate_summary(feature_values, scores))
