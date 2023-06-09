import joblib
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from scipy.integrate import quad

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
    def __init__(self, x_range, model_path, slot_size=0):
        # Load the model
        self.model = joblib.load(model_path)
        self.x_range = x_range

        self.slot_size = slot_size
        if(slot_size == 0):
            self.x_values = np.linspace(x_range[0], x_range[1], 100)
        else:
            self.x_values = np.arange(x_range[0], x_range[1], slot_size)

        self.y_predictions = self.model.predict(self.x_values)
        self.y_range = (0, max(self.y_predictions))
        self.y_values = np.linspace(self.y_range[0], self.y_range[1], 100)
        self.area = self._get_area()
    
    def _get_area(self):
        polinomio = self.model.predict
        area, error = quad(polinomio, self.x_range[0], self.x_range[1])
        return area



#patio1a = Polynomial((0, 250),'../data_analysis/math_models/Pulmon1A.joblib')

    



    

