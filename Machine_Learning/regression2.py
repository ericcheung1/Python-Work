import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt 

prostate = pd.read_csv('Prostate.csv', header=0)

Y = prostate[['lpsa']]
X1 = prostate[['lcavol']]
X2 = prostate[['pgg45']]

model_vol = linear_model.LinearRegression().fit(X1, Y)

fig1, ax1 = plt.subplots()
ax1.scatter(X1, Y)
ax1.plot(X1, model_vol.predict(X1), linewidth=3,color='orange')
ax1.set_xlabel('lcavol')
ax1.set_ylabel('lpsa')
ax1.set_title('model vol')
plt.show()

print('Intercept:', model_vol.intercept_)
print('Coeficient', model_vol.coef_)


