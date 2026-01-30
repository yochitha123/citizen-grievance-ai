import streamlit as st
import pandas as pd

from backend.classifier import classify_issue
from backend.sentiment import get_sentiment
from backend.priority import get_urgency, priority_score

st.set_page_config(page_title="Citizen Grievance AI", layout="wide")

st.title("🧠 Citizen Grievance & Welfare Intelligence System")

uploaded_file = st.file_uploader("📂 Upload Grievance CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Validation
    if "grievance" not in df.columns or "location" not in df.columns:
        st.error("CSV must contain 'grievance' and 'location' columns")
    else:
        results = []

        for _, row in df.iterrows():
            text = row["grievance"]
            location = row["location"]

            category = classify_issue(text)
            sentiment = get_sentiment(text)
            urgency = get_urgency(text)
            priority = priority_score(sentiment, urgency)

            results.append([
                text,
                location,
                category,
                sentiment,
                urgency,
                priority
            ])

        result_df = pd.DataFrame(results, columns=[
            "Grievance",
            "Location",
            "Category",
            "Sentiment",
            "Urgency",
            "Priority"
        ])

        st.subheader("📋 Processed Grievances with Location")
        st.dataframe(result_df)

        st.subheader("📊 Issue Distribution")
        st.bar_chart(result_df["Category"].value_counts())

        st.subheader("📍 Location-wise High Priority Issues")
        high_priority = result_df[result_df["Priority"] >= 6]
        st.dataframe(high_priority)

else:
    st.info("Please upload a CSV file with 'grievance' and 'location' columns")
