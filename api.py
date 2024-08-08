# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI()

# Define the path to the artifacts and model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_PATH = os.path.join(BASE_DIR, 'artifacts')
MODEL_PATH = os.path.join(ARTIFACTS_PATH, 'ran_for_model.joblib')
SCALER_PATH = os.path.join(ARTIFACTS_PATH, 'scaler.joblib')
STATUS_MAPPING_PATH = os.path.join(ARTIFACTS_PATH, 'status_mapping.joblib')

# Load the model and preprocessing objects
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
status_mapping = joblib.load(STATUS_MAPPING_PATH)
status_mapping_inv = {v: k for k, v in status_mapping.items()}

# Load label encoders
label_encoders = {
    'object_type': joblib.load(os.path.join(ARTIFACTS_PATH, 'object_type_label_encoder.joblib'))
}


class PredictionRequest(BaseModel):
    """Model to define the request body for prediction"""
    total_mass: float
    span: float
    period_mins: float
    perigee_km: float
    apogee_km: float
    inclination: float
    object_type: str


def encode_features(data, label_encoders):
    """
    Encode categorical features using label encoders.

    Args:
        data (pd.DataFrame): DataFrame containing the input features.
        label_encoders (dict): Dictionary of label encoders for categorical features.

    Returns:
        pd.DataFrame: DataFrame with encoded categorical features.
    """
    for col, le in label_encoders.items():
        if data[col].values[0] not in le.classes_:
            # Handle unseen labels by adding them to the encoder
            le.classes_ = np.append(le.classes_, data[col].values[0])
        data[col] = le.transform(data[col])
    return data


@app.post("/predict")
def predict(data: PredictionRequest):
    """
    Predict the status of a satellite based on input features.

    Args:
        data (PredictionRequest): Input data for prediction.

    Returns:
        dict: Dictionary containing the predicted status.
    """
    try:
        # Convert request data to DataFrame
        input_data = pd.DataFrame([data.dict()])

        # Encode categorical features
        input_data = encode_features(input_data, label_encoders)

        # Scale the features
        input_data_scaled = scaler.transform(input_data)

        # Predict using the loaded model
        prediction = model.predict(input_data_scaled)
        prediction_label = status_mapping_inv[prediction[0]]

        return {"prediction": prediction_label}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
