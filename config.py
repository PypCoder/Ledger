"""
Ledger — central configuration.
All paths, feature lists, and constants live here so nothing is duplicated
across preprocessing, ensemble, and app modules.
"""

import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models_saved")

SCALER_PATH = os.path.join(MODELS_DIR, "scaler.joblib")
FEATURE_COLUMNS_PATH = os.path.join(MODELS_DIR, "feature_columns.joblib")
MONOTONIC_MASK_PATH = os.path.join(MODELS_DIR, "monotonic_mask.joblib")
RESULTS_SUMMARY_PATH = os.path.join(MODELS_DIR, "results_summary.csv")

LOGISTIC_REGRESSION_PATH = os.path.join(MODELS_DIR, "logistic_regression.joblib")
DECISION_TREE_PATH = os.path.join(MODELS_DIR, "decision_tree.joblib")
RANDOM_FOREST_PATH = os.path.join(MODELS_DIR, "random_forest.joblib")
MLP_PATH = os.path.join(MODELS_DIR, "mlp.pt")

# --- Target / columns ---
TARGET_COL = "loan_status"

BINARY_MAPS = {
    "gender": {"female": 0, "male": 1},
    "previous_loan": {"No": 0, "Yes": 1},
}

MULTI_CAT_COLS = ["education", "home_ownership", "loan_intent"]

MONOTONIC_FEATURES = ["person_income", "credit_score"]

# --- Dropdown choices (must match training data categories exactly) ---
EDUCATION_OPTIONS = ["High School", "Associate", "Bachelor", "Master", "Doctorate"]
HOME_OWNERSHIP_OPTIONS = ["RENT", "OWN", "MORTGAGE", "OTHER"]
LOAN_INTENT_OPTIONS = ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"]
GENDER_OPTIONS = ["female", "male"]
YES_NO_OPTIONS = ["No", "Yes"]

# --- Model display names ---
MODEL_DISPLAY_NAMES = {
    "logistic_regression": "Logistic Regression",
    "decision_tree": "Decision Tree",
    "random_forest": "Random Forest",
    "mlp": "Neural Network (MLP)",
}

DEFAULT_THRESHOLD = 0.5
