import streamlit as st
import pandas as pd

from backend.classifier import classify_issue
from backend.sentiment import get_sentiment
from backend.priority import get_urgency, priority_score

st.set_page_config(page_title="Citizen Grievance AI", layout="wide")

st.title("🧠 Citizen Grievance & Welfare Intelligence System")

uploaded_file = st.file_uploader("Upload Grievance CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    results = []
    for text in df["grievance"]:
        category = classify_issue(text)
        sentiment = get_sentiment(text)
        urgency = get_urgency(text)
        priority = priority_score(sentiment, urgency)

        results.append([text, category, sentiment, urgency, priority])

    result_df = pd.DataFrame(results, columns=[
        "Grievance", "Category", "Sentiment", "Urgency", "Priority"
    ])

    st.subheader("📋 Processed Grievances")
    st.dataframe(result_df)

    st.subheader("📊 Issue Distribution")
    st.bar_chart(result_df["Category"].value_counts())

    st.subheader("🚨 High Priority Issues")
    st.dataframe(result_df[result_df["Priority"] >= 6])
else:
    st.info("Please upload a CSV file with a column named 'grievance'")
