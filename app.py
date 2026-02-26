import streamlit as st
import pandas as pd
import json

# Set up the mobile-friendly page layout
st.set_page_config(page_title="Insurance Study App", layout="centered")

st.title("Insurance Study App 📚")

# Load your JSON data
try:
    with open('study_elements.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    st.success("Data loaded successfully!")
    
    # DIAGNOSTIC STEP: Print the exact column names
    st.subheader("Diagnostic Info:")
    st.write("Your exact column names are:")
    st.write(df.columns.tolist())
    
    # Display the raw table
    st.write("Raw Data Preview:")
    st.dataframe(df)
    
except Exception as e:
    st.error(f"Error: {e}")
