# model_creation.py
from src.local import ARTIFACTS_PATH, DATA_PATH
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_and_preprocess_data(file_path, features, target):
    # Load the dataset
    data = pd.read_csv(file_path, low_memory=False)

    # Handling missing values
    imputer = SimpleImputer(strategy='most_frequent')
    data[features] = imputer.fit_transform(data[features])

    # Ensure the target column has no missing values
    data[target] = data[target].fillna(data[target].mode()[0])

    # Encode categorical features
    label_encoders = {}
    for col in features:
        if data[col].dtype == 'object':
            label_encoders[col] = LabelEncoder()
            data[col] = label_encoders[col].fit_transform(data[col])

    # Save the label encoders for later use
    for col, le in label_encoders.items():
        joblib.dump(le, os.path.join(ARTIFACTS_PATH,
                    f'{col}_label_encoder.joblib'))

    # Create a status mapping dynamically to include all unique statuses
    unique_statuses = data[target].unique()
    status_mapping = {label: idx for idx, label in enumerate(unique_statuses)}

    # Map the target column using the dynamic status mapping
    data[target] = data[target].map(status_mapping)

    # Check for any NaN values in the mapped target column
    if data[target].isnull().sum() > 0:
        raise ValueError(
            "The 'status' column contains NaN values after mapping.")

    # Save the status mapping for later use
    joblib.dump(status_mapping, os.path.join(
        ARTIFACTS_PATH, 'status_mapping.joblib'))

    X = data[features]
    y = data[target]

    return X, y, label_encoders


def train_and_evaluate_model(X, y, param_grid):
    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Standardizing numerical features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Save the scaler for later use
    joblib.dump(scaler, os.path.join(ARTIFACTS_PATH, 'scaler.joblib'))

    # Initialize the Random Forest classifier
    rf = RandomForestClassifier(random_state=42)

    # Perform GridSearchCV for hyperparameter tuning
    grid_search = GridSearchCV(
        estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2, scoring='f1_macro')
    grid_search.fit(X_train, y_train)

    # Best parameters from the grid search
    best_params = grid_search.best_params_

    # Train the Random Forest classifier with the best parameters
    best_rf = RandomForestClassifier(**best_params, random_state=42)
    best_rf.fit(X_train, y_train)

    # Predict on the test set
    y_pred = best_rf.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)

    return best_rf, scaler, best_params, accuracy, conf_matrix, class_report


def main():
    file_path = os.path.join(DATA_PATH, 'combined_df.csv')
    features = ['total_mass', 'span', 'period_mins', 'perigee_km', 'apogee_km',
                'inclination', 'object_type']
    target = 'status'

    X, y, label_encoders = load_and_preprocess_data(
        file_path, features, target)

    # Define the reduced parameter grid for hyperparameter tuning
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'class_weight': [None, 'balanced']
    }

    best_rf, scaler, best_params, accuracy, conf_matrix, class_report = train_and_evaluate_model(
        X, y, param_grid)

    # Save the trained model to a file using joblib
    model_path = os.path.join(ARTIFACTS_PATH, 'ran_for_model.joblib')
    joblib.dump(best_rf, model_path)
    print(f"Model saved to {model_path}")
    print(f"Best Parameters: {best_params}")
    print(f"Accuracy: {accuracy}")
    print(f"Confusion Matrix:\n{conf_matrix}")
    print(f"Classification Report:\n{class_report}")


if __name__ == '__main__':
    main()
