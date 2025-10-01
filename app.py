import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="PhishShield Lite", layout="centered")

# Tiny seed data (for demo). Replace/add real emails later.
data = pd.DataFrame({
    "text": [
        "URGENT: Your account is locked. Click here to verify now.",
        "Final notice: update your payment details to avoid service interruption.",
        "You have won a $500 gift card! Provide bank info to claim.",
        "Team, attached are meeting notes and the sprint board link. Thanks.",
        "Professor, I’ve uploaded the assignment and included citations.",
        "Reminder: quarterly report draft is in the shared drive."
    ],
    "label": [1, 1, 1, 0, 0, 0]  # 1=phish, 0=legit
})

# Simple model pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1,2), min_df=1)),
    ("clf", LogisticRegression(max_iter=200))
])

model.fit(data["text"], data["label"])

st.title("PhishShield (Lite)")
st.caption("Paste an email and get a quick phishing probability. Demo model (tiny training set).")

email_text = st.text_area("Email content", height=200, placeholder="Paste email text here...")
if st.button("Analyze"):
    if not email_text.strip():
        st.warning("Please paste some email text.")
    else:
        proba = model.predict_proba([email_text])[0][1]
        pred = "PHISHING (Likely)" if proba >= 0.5 else "LEGIT (Likely)"
        st.subheader(f"Prediction: {pred}")
        st.write(f"**Phishing probability:** {proba:.2%}")
        with st.expander("Why this is a demo"):
            st.write(
                "This lightweight demo trains a tiny model at startup. "
                "For best results, expand the dataset and persist a trained model. "
                "Use this to showcase the concept quickly."
            )

st.markdown("---")
st.markdown(
    "Tips: Add more labeled examples in `data` above, commit to GitHub, and deploy via Streamlit Community Cloud."
)
