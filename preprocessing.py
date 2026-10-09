"""
Ledger — single-applicant preprocessing for live inference.
Mirrors the exact cleaning/encoding pipeline used in the training notebook,
so a live prediction request is transformed identically to the training data.
"""

import pandas as pd
import numpy as np

from config import BINARY_MAPS, MULTI_CAT_COLS


def clean_and_encode(df: pd.DataFrame) -> pd.DataFrame:
    """Applies the same binary mapping + one-hot encoding used in training."""
    df = df.copy()

    for col, mapping in BINARY_MAPS.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    existing_multi_cat = [c for c in MULTI_CAT_COLS if c in df.columns]
    df = pd.get_dummies(df, columns=existing_multi_cat, drop_first=True)

    bool_cols = df.select_dtypes(include="bool").columns
    df[bool_cols] = df[bool_cols].astype(int)

    return df


def preprocess_single_input(raw_dict: dict, scaler, feature_columns: list) -> np.ndarray:
    """
    Takes one applicant's raw field values (matching the original column
    names/casing used in the form), applies the same cleaning/encoding as
    training, aligns columns to the exact training order, and scales.

    Returns a (1, n_features) numpy array ready for model inference.
    """
    df_single = pd.DataFrame([raw_dict])
    df_single.columns = (
        df_single.columns.str.strip().str.lower().str.replace(" ", "_")
    )

    df_encoded = clean_and_encode(df_single)

    # Any one-hot category not present in this single row (because it wasn't
    # the dropped baseline AND wasn't selected) needs to exist as a 0 column.
    for col in feature_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    # Enforce exact training column order; drop anything unexpected.
    df_encoded = df_encoded[feature_columns]

    scaled = scaler.transform(df_encoded)
    return scaled
