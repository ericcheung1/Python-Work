import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd

prostate = pd.read_csv('Prostate.csv', header=0)

Y = prostate[['lpsa']]
X1 = prostate[['lcavol']]
X2 = prostate[['pgg45']]

model = sm.OLS(Y, X1)
results = model.fit()
print(results.summary())

model2 = smf.ols(formula='lpsa ~ lcavol', data=prostate)
results2 = model2.fit()
print(results2.summary())

model3 = smf.ols(formula='lpsa ~ pgg45', data=prostate)
results3 = model3.fit()
print(results3.summary())

model4 = smf.ols(formula='lpsa ~ lcavol + pgg45', data=prostate)
results4 = model4.fit()
print(results4.summary())
