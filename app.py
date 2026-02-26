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
    
    # Display a simple dropdown to test interactivity
    topic = st.selectbox("Choose a topic to preview:", df['Main Topic'].unique())
    st.write(df[df['Main Topic'] == topic])
    
except Exception as e:
    st.error(f"Couldn't load the data. Error: {e}")
