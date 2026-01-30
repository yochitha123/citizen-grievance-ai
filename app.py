import streamlit as st
import pandas as pd
from textblob import TextBlob

st.set_page_config(page_title="Citizen Grievance AI", layout="centered")

st.title("🧠 Citizen Grievance AI System")
st.write("Upload grievance data (CSV) to analyze complaints")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Show columns for debugging clarity
        st.write("📌 Detected columns:", list(df.columns))

        # Mandatory columns check
        if "grievance" not in df.columns or "location" not in df.columns:
            st.error("❌ CSV must contain columns named: grievance, location")
        else:
            st.success("✅ CSV loaded successfully")

            results = []

            for text, location in zip(df["grievance"], df["location"]):
                analysis = TextBlob(text)
                polarity = analysis.sentiment.polarity

                if polarity < -0.2:
                    sentiment = "Negative"
                elif polarity > 0.2:
                    sentiment = "Positive"
                else:
                    sentiment = "Neutral"

                # Simple category detection
                text_lower = text.lower()
                if "water" in text_lower:
                    category = "Water Issue"
                elif "garbage" in text_lower:
                    category = "Garbage Issue"
                elif "road" in text_lower or "pothole" in text_lower:
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

            # Download result
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Analysis Result",
                data=csv,
                file_name="grievance_analysis.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

else:
    st.info("ℹ️ Please upload a CSV file to continue")

