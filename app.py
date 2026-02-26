import streamlit as st
import pandas as pd
import json
import random

# Set up the mobile-friendly page layout
st.set_page_config(page_title="Insurance Study App", layout="centered")

st.title("Insurance Study App 📚")

# 1. Load the data
@st.cache_data
def load_data():
    with open('study_elements.json', 'r') as f:
        return pd.DataFrame(json.load(f))

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# 2. Initialize the "Memory" (Session State)
if 'card_index' not in st.session_state:
    st.session_state.card_index = 0
if 'score_correct' not in st.session_state:
    st.session_state.score_correct = 0
if 'score_incorrect' not in st.session_state:
    st.session_state.score_incorrect = 0
if 'answer_revealed' not in st.session_state:
    st.session_state.answer_revealed = False

# 3. Scoreboard UI
col1, col2 = st.columns(2)
col1.metric("✅ Correct", st.session_state.score_correct)
col2.metric("❌ Incorrect", st.session_state.score_incorrect)

st.write("---")

# 4. Mobile-friendly Topic Filter
with st.expander("👇 Tap Here to Change Topic", expanded=False):
    topic = st.radio("Available Topics:", df['main_topic'].unique())

filtered_df = df[df['main_topic'] == topic].reset_index(drop=True)

# 5. Draw Card Logic
if st.button("🎲 Draw New Random Card", use_container_width=True):
    st.session_state.card_index = random.randint(0, len(filtered_df) - 1)
    st.session_state.answer_revealed = False

# 6. Display the "Front" of the card
card = filtered_df.iloc[st.session_state.card_index]
st.info(f"**Concept / Sub-Topic:** \n### {card['sub_topic']}")

# 7. Display the "Back" of the card
with st.expander("👀 Reveal Answer / Details", expanded=st.session_state.answer_revealed):
    st.success(f"**Study Content:** {card.get('study_content', 'Content coming soon...')}")
    st.write(f"**MCL Codes:** {card['mcl_codes']}")
    st.write(f"**Exam Weight:** {card['percentage']}")
    st.write(f"**Number of Items:** {card['num_items']}")
    
    st.write("---")
    st.write("**Did you get it right?**")
    
    # Scoring Buttons
    c1, c2 = st.columns(2)
    if c1.button("✅ Yes", use_container_width=True):
        st.session_state.score_correct += 1
        st.session_state.card_index = random.randint(0, len(filtered_df) - 1)
        st.session_state.answer_revealed = False
        st.rerun() # The fix to instantly refresh the score and draw a new card
        
    if c2.button("❌ No", use_container_width=True):
        st.session_state.score_incorrect += 1
        st.session_state.card_index = random.randint(0, len(filtered_df) - 1)
        st.session_state.answer_revealed = False
        st.rerun() # The fix to instantly refresh the score and draw a new card
