# Imports
import pandas as pd
import sklearn

makeDados = sklearn.datasets.make_classification(n_samples=200, n_features=8, weights=[0.995, 0.005], n_classes=2, random_state=45)

print(makeDados)