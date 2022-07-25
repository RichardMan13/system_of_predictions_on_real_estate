# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

from importlib.resources import path
import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import mlflow
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    path_file = (
        "data/ativa_data.csv"
    )
    try:
        data = pd.read_csv(path_file)
    except Exception as e:
        logger.exception(
            "Error: %s", e
        )
    
    # dealing with empty values
    mask1 = data.private_area != 0
    data = data[mask1]

    # drop columns
    data = data.drop(columns=[
        'total_area',
        'id',
        'type',
        'neighborhood'
    ])

    #deleting points
    data = data.drop(data[data.index == 1061].index)
    data = data.drop(data[data.index == 780].index)

    #rescale
    data['private_area'] = np.log(data['private_area'])
    data['price'] = np.log(data['price'])

    #get dummies
    data = pd.get_dummies(data)

    # Split the data into training and test sets.
    X = data.drop(columns=['price'])
    y = data['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=.30, random_state=40)


    with mlflow.start_run():

        lr = make_pipeline(StandardScaler(with_mean=False), LinearRegression())
        lr.fit(X_train, y_train)

        predicted_qualities = lr.predict(X_test)

        (rmse, mae, r2) = eval_metrics(y_test, predicted_qualities)

        print("LinearRegression model")
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(
            sk_model=lr,
            artifact_path="sklearn-model"
        )