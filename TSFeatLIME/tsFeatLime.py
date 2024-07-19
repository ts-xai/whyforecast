import functools
from tslime.tslime import TSLimeExplainer
from tsutils.tsperturbers import BlockBootstrapPerturber
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

####train model
f_model,train, model_stacked,df,scaler = build_model_forecaster()
pred_list_s = []
batch = train[-n_input:].reshape((1, n_input, n_features))
for j in range(n_input):
    pred_list_s.append(model_stacked.predict(batch)[0])
      # print('batch-before',batch)
    batch = np.append(batch[:,1:,:],[[pred_list_s[j]]],axis=1)
    print(batch)
      # print('batch-after',batch)

    ###df[-12:,] predict the test dataset.
df_predict_stacked = pd.DataFrame(scaler.inverse_transform(pred_list_s),
                                index=df[-n_input:].index, columns=['Prediction'])





###train explainer
explainer = TSLimeExplainer(
                            model= functools.partial(f_model.predict, verbose = 0),
                            input_length=sequence_length,
                            relevant_history=relevant_history,
                            perturbers=[
                                ###initial value:block length==2
                                BlockBootstrapPerturber(window_length=min(10, sequence_length-1), block_length=4, block_swap=2),
                            ],
                            n_perturbations=1000,
                            random_seed=22,
                        )


###convert the format
batch = batch.flatten()
df = pd.DataFrame(batch, columns=['Sales'])
df.index.name = 'Index'

#####explanation visulization
explanation = explainer.explain_instance(df)
###ba
print(explanation)

##train a model
##explain a batch
##


