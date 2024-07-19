# whyforecast
This project contains..

## Dataset Overview

We validate the proposed algorithm and its corresponding explanations using two univariate time series forecasting datasets. These datasets pertain to electricity consumption and retail store sales, respectively.

### Superstore Sales Dataset
- **Source:** Community.tableau.com (2017)
- **Period:** 2014 to 2017
- **Data Points:** Nearly 10,000
- **Features:** 21 distinct features across three primary sales categories: furniture, technology goods, and office supplies.
- **Focus Area:** Furniture sales due to their pronounced seasonal fluctuations.
  
### Spanish Electricity Market Dataset
- **Source:** [Kaggle - Spanish Electricity Market](https://www.kaggle.com/datasets/manualrg/spanish-electricity-market-demand-gen-price)
- **Period:** 2014 to 2018
- **Resampling:** Data resampled on a monthly frequency using average daily consumption values.
- **Focus Area:** Forecasting electricity demand.

### Data Partitioning

For time series data, using a simple random split into training and testing sets is untenable as it doesn't respect the temporal order and can lead to data leakage. Instead, the data must be split temporally to preserve its chronological integrity.

### Partitioning Details

| Dataset         | Training Period         | Testing Period        |
|-----------------|-------------------------|-----------------------|
| Sales           | 2014.01.01 - 2016.12.01 | 2017.01.01 - 2017.12.01|
| Consumption     | 2014.01.01 - 2017.12.01 | 2018.01.01 - 2018.12.01|

## Univariate time series forecasting results

| Dataset      | Time Series Model  | RMSE       | MAPE     |
|--------------|--------------------|------------|----------|
| **Sales**    |                    |            |          |
|              | SARIMA             | 205.68     | 28.89%   |
|              | TES                | 204.83     | 27.81%   |
|              | Prophet            | 167.29     | 22.62%   |
|              | Vanilla LSTM       | 146.45     | 19.01%   |
|              | Stacked LSTM       | 145.07     | 18.47%   |
|              | Bidirectional LSTM | 203.50     | 21.04%   |
|              | CNN                | 202.47     | 20.67%   |
| **Electricity** |                 |            |          |
|              | SARIMA             | 12334.76   | 7.95%    |
|              | TES                | 11065.90   | 7.40%    |
|              | Prophet            | 10785.78   | 6.74%    |
|              | Vanilla LSTM       | 9885.90    | 5.85%    |
|              | Stacked LSTM       | 10454.84   | 6.24%    |
|              | Bidirectional LSTM | 12575.76   | 7.66%    |
|              | CNN                | 12048.25   | 7.41%    |


## Prolifc study interface

Treatment group: https://whyforecast1.bristol-xai.uk/consent?prolific_id=[Prolific_ID]
Control group: https://whyforecast.bristol-xai.uk/consent?prolific_id=[Prolific_ID]
