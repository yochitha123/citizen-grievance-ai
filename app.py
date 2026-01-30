import streamlit as st
import pandas as pd
from textblob import TextBlob

st.set_page_config(page_title="Citizen Grievance AI", layout="centered")
st.title("🧠 Citizen Grievance AI System")

uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ✅ COLUMN CLEANING (IMPORTANT FIX)
    df.columns = df.columns.str.strip().str.lower()

    st.write("Detected columns:", list(df.columns))

    if "grievance" not in df.columns or "location" not in df.columns:
        st.error("CSV must contain columns: grievance, location")
        st.stop()

    results = []

    for _, row in df.iterrows():
        text = row["grievance"]
        location = row["location"]

        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        if polarity < -0.2:
            sentiment = "Negative"
        elif polarity > 0.2:
            sentiment = "Positive"
        else:
            sentiment = "Neutral"

        text_lower = text.lower()
        if "water" in text_lower:
            category = "Water Issue"
        elif "garbage" in text_lower:
            category = "Garbage Issue"
        elif "pothole" in text_lower or "road" in text_lower:
            category = "Road Issue"
        elif "power" in text_lower:
            category = "Electricity Issue"
        elif "hospital" in text_lower:
            category = "Healthcare Issue"
        else:
            category = "General Complaint"

        results.append({
            "Grievance": text,
            "Location": location,
            "Category": category,
            "Sentiment": sentiment
        })

    result_df = pd.DataFrame(results)

    st.subheader("📊 Analyzed Grievances")
    st.dataframe(result_df)

    st.download_button(
        "⬇️ Download Result CSV",
        result_df.to_csv(index=False),
        "analysis_result.csv",
        "text/csv"
    )

else:
    st.info("Please upload a CSV file")
