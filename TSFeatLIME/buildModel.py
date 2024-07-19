
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from tsutils.model_wrappers import Tensor_Based_Forecaster
import warnings
import random


warnings.filterwarnings("ignore")

#####measure of prediction accuracy
def performance(y_true, y_pred):
    mse = ((y_pred - y_true) ** 2).mean()
    mape= np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    performance_data= {'MSE':round(mse, 2),
                      'RMSE':round(np.sqrt(mse), 2),
                       'MAPE':round(mape, 2)
                      }
    return performance_data

def performance2(y_true, y_pred):
    #y_true, y_pred = np.array(y_true), np.array(y_pred)
    mse = ((y_pred - y_true) ** 2).mean()
    mape= np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return( print(' The MSE of forecasts is {}'.format(round(mse, 2))+
                  '\n The RMSE of forecasts is {}'.format(round(np.sqrt(mse), 2))+
                  '\n The MAPE of forecasts is {}'.format(round(mape, 2))))



def build_model_forecaster(seed_value=42):
    np.random.seed(seed_value)
    random.seed(seed_value)


    ####initial values
    df = pd.read_csv("./dataset/furnitureSales.csv")
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Set 'order_date' as the index
    df.set_index('order_date', inplace=True)

    # Convert the 'sales' column to a Series with desired attributes
    df = df['sales'].asfreq('MS')
    df.name = 'sales'
    df = df.astype('float64')
    print(df)

    train, test = np.array(df[:-12]), np.array(df[-12:])
    train= train.reshape(-1,1)
    test= test.reshape(-1,1)

    scaler = MinMaxScaler()
    scaler.fit(train)
    train = scaler.transform(train)
    test = scaler.transform(test)
    n_input = 12
    # univariate
    n_features = 1
    #TimeseriesGenerator automatically transform a univariate time series dataset into a supervised learning problem.
    generator = TimeseriesGenerator(train, train, length=n_input, batch_size=10)


    ####stacked LSTM
    # n=3
    # store2= np.zeros((12,n))
    # for i in range(n):
    model_stacked = Sequential()
        #In stacked LSTM, we should output a sequence rather than a single value for each input -> return_sequences=True
    model_stacked.add(LSTM(50, activation='relu', return_sequences = True, input_shape=(12, 1)))
    model_stacked.add(LSTM(50, activation='relu'))
    model_stacked.add(Dense(100, activation='relu'))
    model_stacked.add(Dense(50, activation='relu'))
    model_stacked.add(Dense(1))
    model_stacked.compile(optimizer='adam', loss='mse')
    model_stacked.fit_generator(generator,epochs=200)

    f_model = Tensor_Based_Forecaster(model=model_stacked, forecast_function="predict", input_length=12, n_features = 1)

###the reason annotation is: write it in another class
    # pred_list_s = []
    # batch = train[-n_input:].reshape((1, n_input, n_features))
    # for j in range(n_input):
    #   pred_list_s.append(model_stacked.predict(batch)[0])
    #   # print('batch-before',batch)
    #   batch = np.append(batch[:,1:,:],[[pred_list_s[j]]],axis=1)
    #   # print('batch-after',batch)
    #
    # ###df[-12:,] predict the test dataset.
    # df_predict_stacked = pd.DataFrame(scaler.inverse_transform(pred_list_s),
    #                               index=df[-n_input:].index, columns=['Prediction'])
    return f_model, train, model_stacked,df,scaler











