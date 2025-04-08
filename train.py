# save_model.py
import pickle
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.linear_model import LinearRegression

iris = load_iris()
X, y = iris.data, iris.target

model = RandomForestClassifier()
model.fit(X, y)

with open("app/model.pkl", "wb") as f:
    pickle.dump(model, f)

# Exercise 5

housing = pd.read_csv("Housing.csv")

feature = housing[['area', 'bedrooms', 'bathrooms']]
target = housing['price']

linear = LinearRegression()
linear.fit(feature, target)

with open('app/linear_model.pkl', 'wb') as f:
    pickle.dump(linear, f)