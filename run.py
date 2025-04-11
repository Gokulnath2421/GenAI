import os
import streamlit as st
import pandas as pd
import subprocess
import sys

# Function to install necessary packages
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install necessary packages if they aren't installed
required_packages = ["streamlit", "pandas", "google-generativeai"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        st.warning(f"{package} not found, installing now...")
        install_package(package)

import google.generativeai as genai

# Configure API key
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
