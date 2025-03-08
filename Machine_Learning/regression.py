from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns

diabetes = datasets.load_diabetes()

print(diabetes.DESCR)
print(diabetes.feature_names)

X = diabetes.data
Y = diabetes.target
X.shape
Y.shape

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2)
X_test.shape, Y_test.shape
X_train.shape, Y_train.shape

model = linear_model.LinearRegression()

model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)

print('Coefficients:', model.coef_)
print('Intercept:', model.intercept_)
print(f'Mean Squared Error: {mean_squared_error(Y_test, Y_pred):.2f}')
print(f'R^2: {r2_score(Y_test, Y_pred):.2f}')

sns.scatterplot(x=Y_test, y=Y_pred).set(title=
'Predicted vs Actual', ylabel='Predicted', xlabel='Actual')