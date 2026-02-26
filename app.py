import streamlit as st
import pandas as pd
import json
import random

# Set up the mobile-friendly page layout
st.set_page_config(page_title="Insurance Study App", layout="centered")

st.title("Ashley's Insurance Study App 📚")

# 1. Load the data (and cache it so it's fast)
@st.cache_data
def load_data():
    with open('study_elements.json', 'r') as f:
        return pd.DataFrame(json.load(f))

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# 2. Build the UI
st.write("### 🧠 Flashcard Mode")

# Let the user filter by the main topic using a mobile-friendly touch menu
with st.expander("👇 Tap Here to Change Topic", expanded=False):
    topic = st.radio("Available Topics:", df['main_topic'].unique())

# Filter the data based on the selection
filtered_df = df[df['main_topic'] == topic].reset_index(drop=True)

# 3. Handle the "Memory" for the random card
if 'card_index' not in st.session_state:
    st.session_state.card_index = 0

if st.button("🎲 Draw Random Card"):
    # Pick a random number between 0 and the end of the filtered list
    st.session_state.card_index = random.randint(0, len(filtered_df) - 1)

# 4. Display the "Front" of the card
card = filtered_df.iloc[st.session_state.card_index]

st.info(f"**Concept / Sub-Topic:** \n### {card['sub_topic']}")

# 5. Display the "Back" of the card (Hidden until clicked)
with st.expander("👀 Reveal Answer / Details"):
    st.success(f"**Study Content:** {card.get('study_content', 'Content coming soon...')}")
    st.write(f"**MCL Codes:** {card['mcl_codes']}")
    st.write(f"**Exam Weight:** {card['percentage']}")
    st.write(f"**Number of Items:** {card['num_items']}")
