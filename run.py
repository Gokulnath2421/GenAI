import os
import streamlit as st
os.system('pip install google-generativeai')
import pandas as pd
import google.generativeai as genai

genai.configure(api_key='AIzaSyDw6WiX1_IYCWaVuM35ytN1wydi9j2SkDA')

def load_csv(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None

def analyze_feedback(feedback):
    try:
        response = genai.GenerativeModel('gemini-2.0-flash').generate_content(feedback)
        return response.text
    except Exception as e:
        st.error(f"Error analyzing feedback: {e}")
        return None


st.title("Customer Feedback Insight Generator")

uploaded_file = st.file_uploader("Upload Customer Feedback CSV", type=["csv"])

if uploaded_file:
    df = load_csv(uploaded_file)
    if df is not None:
        st.success("CSV loaded successfully!")
        st.dataframe(df)

        feedback_list = df['Feedback'].tolist()
        results = []

        for feedback in feedback_list:
            analysis = analyze_feedback(feedback)
            if analysis:
                results.append(analysis)

        st.subheader("Analysis Results")
        for i, feedback in enumerate(feedback_list):
            st.markdown(f"**Feedback:** {feedback}")
            st.markdown(f"**Analysis:** {results[i]}")
            st.markdown("---")
