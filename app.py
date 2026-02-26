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
    # !!! UPDATED: Load from qa_study_elements.json for enriched content !!!
    with open('qa_study_elements.json', 'r') as f:
        return pd.DataFrame(json.load(f))

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Initialize session state for score and feedback tracking
if 'card_index' not in st.session_state:
    st.session_state.card_index = 0
if 'total_correct' not in st.session_state:
    st.session_state.total_correct = 0
if 'total_incorrect' not in st.session_state:
    st.session_state.total_incorrect = 0
if 'answer_revealed' not in st.session_state:
    st.session_state.answer_revealed = False
if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = False

# 2. Build the UI
st.write("### 🧠 Flashcard Mode")

# Let the user filter by the main topic using a mobile-friendly touch menu
with st.expander("👇 Tap Here to Change Topic", expanded=False):
    # Ensure the topic selection is tied to a unique key if multiple radio buttons are on the page
    selected_topic = st.radio("Available Topics:", df['main_topic'].unique(), key='topic_selector')

# Filter the data based on the selection
filtered_df = df[df['main_topic'] == selected_topic].reset_index(drop=True)

# Handle the "Draw Random Card" button
if st.button("🎲 Draw Random Card", use_container_width=True):
    if not filtered_df.empty:
        st.session_state.card_index = random.randint(0, len(filtered_df) - 1)
        st.session_state.answer_revealed = False  # Reset for new card
        st.session_state.feedback_given = False   # Reset for new card
        st.experimental_rerun() # Force a rerun to reset expander and buttons
    else:
        st.warning("No study elements available for the selected topic.")

# Display the current card
if not filtered_df.empty and 0 <= st.session_state.card_index < len(filtered_df):
    card = filtered_df.iloc[st.session_state.card_index]

    st.write("---") # Visual separator
    # !!! UPDATED: Display question on the front of the card !!!
    st.markdown(f"### Question:\n{card['question']}")

    # Display the "Back" of the card (Hidden until clicked)
    # Use a unique key for the expander to prevent state issues across cards
    expander_key = f"expander_{st.session_state.card_index}_{st.session_state.answer_revealed}"
    with st.expander("👀 Reveal Answer / Details", expanded=st.session_state.answer_revealed, key=expander_key):
        st.session_state.answer_revealed = True # Mark as revealed when expander is open

        # !!! UPDATED: Display correct answer and explanation !!!
        st.success(f"**Correct Answer:** {card.get('correct_answer', 'N/A')}")
        st.write(f"**Explanation:** {card.get('explanation', 'No explanation provided.')}")

        if card.get('mcl_codes'):
            st.write(f"**MCL Codes:** {card['mcl_codes']}")
        st.write(f"**Exam Weight:** {card['percentage']} ({card['num_items']} items)")

    # !!! NEW FEATURE: Interactive 'Correct' and 'Incorrect' buttons !!!
    if st.session_state.answer_revealed and not st.session_state.feedback_given:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Correct", type="primary", use_container_width=True):
                st.session_state.total_correct += 1
                st.session_state.feedback_given = True
                st.success("That's right! Keep up the good work!", icon="✅")
                st.experimental_rerun() # Force rerun to show updated score and disable buttons
        with col2:
            if st.button("❌ Incorrect", type="secondary", use_container_width=True):
                st.session_state.total_incorrect += 1
                st.session_state.feedback_given = True
                st.error("Let's review this one. Don't worry, you'll get it next time!", icon="❌")
                st.experimental_rerun() # Force rerun to show updated score and disable buttons
    elif st.session_state.feedback_given:
        st.info("Feedback recorded. Draw a new card to continue.")

    st.write("---")
    st.markdown(f"**Session Score:** ✅ Correct: {st.session_state.total_correct} | ❌ Incorrect: {st.session_state.total_incorrect}")
else:
    st.info("Select a topic and draw a random card to start studying!")
