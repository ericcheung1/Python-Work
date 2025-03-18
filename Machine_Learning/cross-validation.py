from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, ShuffleSplit
from sklearn.metrics import mean_squared_error
from os import path
import pandas as pd
import numpy as np

dir = 'C:/Users/Eric/Documents/python/Python-Work/Machine_Learning'

prostate = pd.read_csv(path.join(dir, 'Prostate.csv'), header=0)
print(prostate.shape)
Y = prostate[['lpsa']]
X = prostate[['lcavol']]
print(X.shape, Y.shape)

kf = KFold(n_splits=5)
mse = []
for train, test in kf.split(X):
    x_train, x_test = X.iloc[train], X.iloc[test]
    y_train, y_test = Y.iloc[train], Y.iloc[test]

    mod_vol = LinearRegression().fit(x_train, y_train)
    y_pred = mod_vol.predict(x_test)
    
    mse.append(mean_squared_error(y_test, y_pred))
np.mean(mse)

ss = ShuffleSplit(n_splits=5, test_size=0.2)
mse_ss = []
for train1, test1 in ss.split(X):
    x_train1, x_test1 = X.iloc[train1], X.iloc[test1]
    y_train1, y_test1 = Y.iloc[train1], Y.iloc[test1]

    mod_vol1 = LinearRegression().fit(x_train1, y_train1)
    y_pred1 = mod_vol.predict(x_test1)

    mse_ss.append(mean_squared_error(y_test1, y_pred1))
np.mean(mse_ss)