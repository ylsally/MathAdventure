import streamlit as st
import random
from fractions import Fraction

# --- CORE LOGIC: UPDATED PROBLEM GENERATOR ---
def generate_math_problem(topic, level):
    if topic == "Fractions (Word Problems)":
        themes = [
            {"item": "chanterelles", "action": "foraged in the woods"},
            {"item": "Japanese stickers", "action": "bought in Nagoya"},
            {"item": "onigiri", "action": "made for a picnic"}
        ]
        theme = random.choice(themes)
        
        # Difficulty scales with level
        total = random.choice([12, 24, 36, 48, 60]) if level < 5 else random.choice([72, 84, 96, 120])
        denom1 = random.choice([2, 3, 4])
        spent_first = total // denom1
        remaining = total - spent_first
        
        possible_denoms = [d for d in [2, 3, 4, 5] if remaining % d == 0]
        denom2 = random.choice(possible_denoms) if possible_denoms else 2
        spent_second = remaining // denom2
        final_left = remaining - spent_second
        
        story = (f"You {theme['action']} {total} {theme['item']}. "
                 f"You gave 1/{denom1} to a friend. "
                 f"Then, you gave 1/{denom2} of the **remaining** {theme['item']} to a teacher. "
                 f"How many do you have left?")
        
        hint = f"Step 1: Find 1/{denom1} of {total}. Step 2: Subtract it. Step 3: Find 1/{denom2} of that remainder!"
        return story, final_left, hint

    elif topic == "Geometry":
        length = random.randint(2, 5 + level)
        width = random.randint(2, 4 + level)
        return f"What is the AREA of a rectangle with length {length} and width {width}?", length * width, f"Area = Length × Width"

    else: # Basic Arithmetic
        n1 = random.randint(1, 10 + (level * 5))
        n2 = random.randint(1, 10 + (level * 5))
        return f"What is {n1} + {n2}?", n1 + n2, "Try breaking the numbers into tens and ones!"

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Math Adventure", page_icon="🔢")

# --- SIDEBAR FOR TOPIC & LEVEL ---
st.sidebar.title("Adventure Settings 🛠️")
chosen_topic = st.sidebar.selectbox("Choose a Topic:", ["Addition", "Geometry", "Fractions (Word Problems)"])
chosen_level = st.sidebar.slider("Choose Difficulty Level:", 1, 10, 1)

if 'current_data' not in st.session_state or st.sidebar.button("Generate New Problem"):
    st.session_state.current_data = generate_math_problem(chosen_topic, chosen_level)
    st.session_state.show_hint = False

st.title("Math Adventure! 🔢✨")

# --- DISPLAY PROBLEM ---
question, answer, hint_text = st.session_state.current_data
st.info(f"**Target:** {chosen_topic} (Level {chosen_level})")
st.write(f"### {question}")

# --- USER INPUT ---
user_ans = st.number_input("Type your answer:", step=1, value=None, key="math_input")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Submit"):
        if user_ans == answer:
            st.success("Correct! 🎉")
            # Automatically generates a new one on rerun
            st.session_state.current_data = generate_math_problem(chosen_topic, chosen_level)
            st.session_state.show_hint = False
            st.rerun()
        else:
            st.error("Not quite! Try again or use a hint. 💪")

with col2:
    if st.button("Need a hint? 💡"):
        st.session_state.show_hint = True

if st.session_state.show_hint:
    st.warning(hint_text)
