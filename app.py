"""
Ledger — Loan Approval Prediction
A calibrated, monotonicity-constrained ensemble for loan approval decisions.
"""

import streamlit as st
import pandas as pd

import theme
from preprocessing import preprocess_single_input
from ensemble import load_all_models, load_results_summary, ensemble_predict, predict_one
from config import (
    EDUCATION_OPTIONS, HOME_OWNERSHIP_OPTIONS, LOAN_INTENT_OPTIONS,
    GENDER_OPTIONS, YES_NO_OPTIONS, MODEL_DISPLAY_NAMES, DEFAULT_THRESHOLD,
)

st.set_page_config(
    page_title="Ledger — Loan Approval Prediction",
    page_icon="📘",
    layout="centered",
)

theme.inject_css(st)


@st.cache_resource
def get_models():
    return load_all_models()


models, scaler, feature_columns = get_models()
results_summary = load_results_summary()

# ---------------------------------------------------------------
# Header
# ---------------------------------------------------------------
st.title("Ledger")
st.markdown(
    '<p class="ledger-caption">A calibrated ensemble for loan approval prediction — '
    "four models, one decision, every weight accounted for.</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Sidebar — model + threshold controls
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown("### Settings")
    model_choice_label = st.selectbox(
        "Model",
        ["Ensemble (all 4)"] + list(MODEL_DISPLAY_NAMES.values()),
    )
    threshold = st.slider("Decision threshold", 0.0, 1.0, DEFAULT_THRESHOLD, 0.01)

    st.markdown(theme.rule_html(), unsafe_allow_html=True)
    st.markdown(
        '<p class="ledger-caption">Ledger averages probability estimates from four '
        "independently trained models — Logistic Regression, Decision Tree, "
        "Random Forest, and a monotonicity-constrained neural network — "
        "calibrated so no single model dominates by confidence alone.</p>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------
# Applicant information form
# ---------------------------------------------------------------
st.markdown("### Applicant Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 18, 100, 30)
    gender = st.selectbox("Gender", GENDER_OPTIONS)
    education = st.selectbox("Education", EDUCATION_OPTIONS)
    person_income = st.number_input("Annual income", 0, 1_000_000, 50_000, step=1000)
    employee_experience = st.number_input("Years of experience", 0, 50, 3)
    home_ownership = st.selectbox("Home ownership", HOME_OWNERSHIP_OPTIONS)
    loan_amount = st.number_input("Loan amount", 0, 500_000, 10_000, step=500)

with col2:
    loan_intent = st.selectbox("Loan intent", LOAN_INTENT_OPTIONS)
    loan_interest_rate = st.number_input("Loan interest rate (%)", 0.0, 40.0, 12.0, step=0.1)
    loan_percentage = round(loan_amount / person_income, 2) if person_income > 0 else 0.0
    st.markdown(
         f'<p class="ledger-caption">Loan as % of income: {loan_percentage:.0%} (calculated)</p>',
         unsafe_allow_html=True,
    )
    credit_history = st.number_input("Credit history (years)", 0, 30, 5)
    credit_score = st.number_input("Credit score", 300, 850, 650)
    previous_loan = st.selectbox("Previous loan on record", YES_NO_OPTIONS)

st.markdown(theme.rule_html(), unsafe_allow_html=True)

predict_clicked = st.button("Evaluate Application", type="primary")

# ---------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------
if predict_clicked:
    raw_input = {
        "age": age,
        "gender": gender,
        "education": education,
        "person_income": person_income,
        "employee_experience": employee_experience,
        "home_ownership": home_ownership,
        "loan_amount": loan_amount,
        "loan_intent": loan_intent,
        "loan_interest_rate": loan_interest_rate,
        "loan_percentage": loan_percentage,
        "credit_history": credit_history,
        "credit_score": credit_score,
        "previous_loan": previous_loan,
    }

    X_scaled = preprocess_single_input(raw_input, scaler, feature_columns)

    model_key_lookup = {v: k for k, v in MODEL_DISPLAY_NAMES.items()}
    is_ensemble = model_choice_label == "Ensemble (all 4)"

    if is_ensemble:
        per_model_probs, ensemble_prob, _ = ensemble_predict(models, X_scaled, threshold)
        final_prob = float(ensemble_prob[0])
    else:
        final_prob = float(predict_one(models, model_key_lookup[model_choice_label], X_scaled)[0])

    is_approved = final_prob >= threshold
    decision_text = "Approved" if is_approved else "Rejected"

    st.markdown("### Result")
    st.markdown(theme.result_animation_html(is_approved), unsafe_allow_html=True)
    st.markdown(
        theme.result_panel_html(
            label=f"{model_choice_label} — Decision",
            value_text=f"{decision_text}  ·  {final_prob:.1%} approval probability",
            is_approved=is_approved,
        ),
        unsafe_allow_html=True,
    )

    def play_sound(url: str):
        st.markdown(
            f"""
                <audio autoplay hidden>
                   <source src="{url}" type="audio/mp3">
                </audio>
            """,
            unsafe_allow_html=True
         )

    if is_approved:
        st.balloons()
        play_sound("https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3")  # Success chime
    else:
        st.snow()
        play_sound("https://assets.mixkit.co/active_storage/sfx/2670/2670-preview.mp3")  # Whistle/Wind sound effect

    if is_ensemble:
        st.markdown("### Per-Model Breakdown")
        breakdown_df = pd.DataFrame({
            "Model": list(MODEL_DISPLAY_NAMES.values()) + ["Ensemble (average)"],
            "Approval probability": [
                f"{per_model_probs['logistic_regression'][0]:.1%}",
                f"{per_model_probs['decision_tree'][0]:.1%}",
                f"{per_model_probs['random_forest'][0]:.1%}",
                f"{per_model_probs['mlp'][0]:.1%}",
                f"{ensemble_prob[0]:.1%}",
            ],
        })
        st.table(breakdown_df.set_index("Model"))
        st.markdown(
            '<p class="ledger-caption">Probabilities are averaged with equal weight across '
            "all four models. The neural network's output is temperature-scaled so its "
            "confidence is calibrated before averaging.</p>",
            unsafe_allow_html=True,
        )
# ---------------------------------------------------------------
# Model performance (expander, not front-and-center)
# ---------------------------------------------------------------
if results_summary is not None:
    with st.expander("Model performance on held-out test data"):
        display_df = results_summary.copy()
        display_df.columns = [c.capitalize() for c in display_df.columns]
        for col in ["Accuracy", "Precision", "Recall", "F1", "Auc"]:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda v: f"{v:.1%}")
        st.table(display_df.set_index("Name"))
        st.markdown(
            '<p class="ledger-caption">Metrics computed on a held-out test set not '
            "used during training. The ensemble is evaluated using the same equal-weight "
            "averaging used for live predictions above.</p>",
            unsafe_allow_html=True,
        )
