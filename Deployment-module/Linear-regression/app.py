from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("linear_regression_model.joblib")


@app.get(path="/predict/{TV_value}")
def predict(TV_value):
    value = np.array(TV_value).reshape(-1, 1)
    pred = model.predict(value)

    return {"Sales-value": pred[0]}
