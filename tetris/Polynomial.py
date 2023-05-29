import joblib
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin

# Define a custom estimator class that wraps numpy.poly1d
class PolyRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, degree=1):
        self.degree = degree

    def fit(self, X, y=None):
        self.coeffs = np.polyfit(X.squeeze(), y, self.degree)
        return self

    def predict(self, X):
        X = np.asarray(X)
        return np.polyval(self.coeffs, X.squeeze())


class Polynomial:
    def __init__(self, x_range, model_path):
        # Load the model
        self.model = joblib.load(model_path)
        self.x_range = x_range

        self.x_values = np.linspace(x_range[0], x_range[1], 100)
        self.y_predictions = self.model.predict(self.x_values)
        self.y_range = (0, max(self.y_predictions))
        self.y_values = np.linspace(self.y_range[0], self.y_range[1], 100)



#patio1a = Polynomial((0, 250),'../data_analysis/math_models/Pulmon1A.joblib')

    



    

