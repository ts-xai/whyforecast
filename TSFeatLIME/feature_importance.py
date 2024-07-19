
from buildModel import build_model_forecaster
import pandas as pd
import numpy as np
import eli5

###initial dataset
relevant_history = 12
sequence_length = 12
input_length = 12
n_input = 12
n_features = 1
batch_collection = []
y_collection = []

class CallableModelWrapper:
    def __init__(self, model):
        self.model = model

    def __call__(self, inputs):
        return self.model.predict(inputs)


####train model
f_model,train, model_stacked,df,scaler = build_model_forecaster()
pred_list_s = []
batch = train[-n_input:].reshape((1, n_input, n_features))
print('batch',batch)

for j in range(n_input):
    pred_list_s.append(model_stacked.predict(batch)[0])
      # print('batch-before',batch)
    batch = np.append(batch[:,1:,:],[[pred_list_s[j]]],axis=1)
    print(batch)
    batch_collection.append(batch)
    y_values = [group[0][0] for group in batch]
    y_collection.append(y_values)
      # print('batch-after',batch)

    ###df[-12:,] predict the test dataset.
df_predict_stacked = pd.DataFrame(scaler.inverse_transform(pred_list_s),
                                index=df[-n_input:].index, columns=['Prediction'])


print(y_collection)
print('batch_collection',batch_collection)
###comparea feature important between surrogate model and black box model
background = np.concatenate(batch_collection)

# Reshape the array to 2 dimensions
background = background.reshape(-1, 12)

import shap
def model_wrapper(x):
    # This function takes a numpy array as input and returns a numpy array as output
    return model_stacked.predict(x.reshape(-1, 12, 1)).flatten()

explainer = shap.Explainer(model_wrapper, background)

# Calculate SHAP values for the entire test dataset
shap_values = explainer.shap_values(background)

# Create a summary plot
shap.summary_plot(shap_values, background)
#
# shap_values = explainer(background)
# print(shap_values)
feature_importances = np.mean(np.abs(shap_values), axis=0)

# Sort feature importances in descending order
sorted_indices = np.argsort(-feature_importances)

# Display sorted feature importances
print("Feature importances:")
for i in sorted_indices:
    print(f"Feature {i + 1}: {feature_importances[i]}")