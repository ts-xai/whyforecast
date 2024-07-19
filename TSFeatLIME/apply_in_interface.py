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
random_seeds = 42

f_model,train, model_stacked,df,scaler = build_model_forecaster(seed_value=42)
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
            BlockBootstrapPerturber(window_length=min(10, sequence_length - 1), block_length=5, block_swap=2),
        ],
        n_perturbations=1000,
        random_seed=22,
        use_weight=True,
)

pred_list_s = []
batch = train[-n_input:].reshape((1, n_input, n_features))
for j in range(n_input):
    batch_instance = batch.flatten()
    instance = pd.DataFrame(batch_instance, columns=['Sales'])
    instance.index.name = 'Index'
    print('instance', instance)
    explanation = explainer.explain_instance(instance)
    explanation_collection.append(explanation)
    pred_list_s.append(model_stacked.predict(batch)[0])
    print('pred_list_s',pred_list_s)
    batch = np.append(batch[:,1:,:],[[pred_list_s[j]]],axis=1)
    print('=====')
    print('batch-after')
    print(batch)
    print('======')
        ###convert the format of batch

# print(explanation_collection)
    #list the finial result of the testing dataset.
print('pred_list_s',pred_list_s)
df_predict_stacked = pd.DataFrame(scaler.inverse_transform(pred_list_s),
                    index=df[-n_input:].index, columns=['Prediction'])

print('================')
print(df_predict_stacked)
print('================')



# save the final result
with open('explanation_to_interface.pkl', 'wb') as f:
    pickle.dump(explanation_collection, f)
# get the plot.


