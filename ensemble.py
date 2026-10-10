"""
Ledger — model loading and soft-voting ensemble logic.
"""

import torch
import numpy as np
import joblib
import pandas as pd

from models import MonotonicMLP
from config import (
    SCALER_PATH, FEATURE_COLUMNS_PATH, MONOTONIC_MASK_PATH,
    LOGISTIC_REGRESSION_PATH, DECISION_TREE_PATH, RANDOM_FOREST_PATH, MLP_PATH,
    RESULTS_SUMMARY_PATH, DEFAULT_THRESHOLD,
)


def load_all_models():
    """Loads every trained model plus the shared scaler and feature column order."""
    log_reg = joblib.load(LOGISTIC_REGRESSION_PATH)
    dtree = joblib.load(DECISION_TREE_PATH)
    rf = joblib.load(RANDOM_FOREST_PATH)

    feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
    mask = joblib.load(MONOTONIC_MASK_PATH)

    mlp = MonotonicMLP(in_features=len(feature_columns), monotonic_mask=mask)
    mlp.load_state_dict(torch.load(MLP_PATH, map_location="cpu"))
    mlp.eval()

    scaler = joblib.load(SCALER_PATH)

    models = {
        "logistic_regression": log_reg,
        "decision_tree": dtree,
        "random_forest": rf,
        "mlp": mlp,
    }
    return models, scaler, feature_columns


def load_results_summary():
    """Loads the saved evaluation metrics table from the training notebook, if present."""
    try:
        return pd.read_csv(RESULTS_SUMMARY_PATH)
    except FileNotFoundError:
        return None

def predict_one(models: dict, key: str, X_scaled: np.ndarray) -> np.ndarray:
    """Probability of Approved from a single model only."""
    if key == "mlp":
        X_t = torch.tensor(X_scaled, dtype=torch.float32)
        with torch.no_grad():
            return models["mlp"].predict_proba(X_t, apply_temperature=True).numpy()
    return models[key].predict_proba(X_scaled)[:, 1]

def predict_all(models: dict, X_scaled: np.ndarray) -> dict:
    """Returns each model's probability of class 1 (Approved) for the input batch."""
    probs = {}
    probs["logistic_regression"] = models["logistic_regression"].predict_proba(X_scaled)[:, 1]
    probs["decision_tree"] = models["decision_tree"].predict_proba(X_scaled)[:, 1]
    probs["random_forest"] = models["random_forest"].predict_proba(X_scaled)[:, 1]

    X_t = torch.tensor(X_scaled, dtype=torch.float32)
    with torch.no_grad():
        mlp_probs = models["mlp"].predict_proba(X_t, apply_temperature=True).numpy()
    probs["mlp"] = mlp_probs

    return probs


def ensemble_predict(models: dict, X_scaled: np.ndarray, threshold: float = DEFAULT_THRESHOLD):
    """
    Equal-weight soft voting across all 4 models — deliberately not weighted
    by accuracy/AUC, since the MLP's probabilities are calibrated via
    temperature scaling specifically so an equal-weight average is fair.

    Returns (per_model_probs: dict, ensemble_prob: np.ndarray, decision: np.ndarray)
    """
    probs = predict_all(models, X_scaled)
    stacked = np.stack(list(probs.values()), axis=0)
    ensemble_prob = stacked.mean(axis=0)
    decision = (ensemble_prob >= threshold).astype(int)

    return probs, ensemble_prob, decision
