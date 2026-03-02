import streamlit as st
import random

# --- 1. THE UPDATED PROBLEM GENERATOR ---
def generate_math_problem(topic, level):
    if topic == "Fractions (Word Problems)":
        themes = [
            {"item": "chanterelles", "action": "foraged in the woods"},
            {"item": "Japanese stickers", "action": "bought in Nagoya"},
            {"item": "onigiri", "action": "made for a picnic"},
            {"item": "books", "action": "collected from the library"},
            {"item": "coins", "action": "found in a jar"},
            {"item": "apples", "action": "picked from the orchard"},
        ]
        theme = random.choice(themes)

        # Expanded denominator pool — grows with level
        denom_pool = list(range(2, 2 + level * 3))  
        d1 = random.choice(denom_pool)
        d2 = random.choice(denom_pool)

        # Factor scales more aggressively with level
        factor = random.randint(1, level * 5)
        total = d1 * d2 * factor

        gave_away_first = total // d1
        remainder = total - gave_away_first
        gave_away_second = remainder // d2
        final_left = remainder - gave_away_second

        story = (
            f"You {theme['action']} {total} {theme['item']}. "
            f"You gave 1/{d1} to a friend. "
            f"Then you gave 1/{d2} of the **remaining** items to your teacher. "
            f"How many do you have left?"
        )

        hint = (
            f"Step 1: 1/{d1} of {total} = {gave_away_first}. "
            f"Step 2: {total} - {gave_away_first} = {remainder}. "
            f"Step 3: 1/{d2} of {remainder} = {gave_away_second}. "
            f"Step 4: {remainder} - {gave_away_second} = {final_left}."
        )

        return story, final_left, hint

    elif topic == "Geometry":
        l, w = random.randint(2, 5 + level), random.randint(2, 4 + level)
        return f"What is the AREA of a {l}x{w} rectangle?", l * w, "Area = Length x Width"

    else: # Addition
        n1, n2 = random.randint(1, 10 * level), random.randint(1, 10 * level)
        return f"What is {n1} + {n2}?", n1 + n2, "Try breaking the numbers into tens and ones!"

# --- 2. THE UI & SESSION STATE ---
st.set_page_config(page_title="Math Adventure", page_icon="🔢")

# Emergency Reset Button
if st.sidebar.button("Reset / Clear Errors 🔄"):
    st.session_state.clear()
    st.rerun()

st.sidebar.title("Settings ⚙️")
topic_choice = st.sidebar.selectbox("Choose Topic", ["Fractions (Word Problems)", "Addition", "Geometry"])
level_choice = st.sidebar.slider("Difficulty Level", 1, 10, 1)

# Check if we need to generate a new problem due to a settings change
if 'current_data' not in st.session_state:
    st.session_state.current_data = generate_math_problem(topic_choice, level_choice)
    st.session_state.show_hint = False

# --- 3. THE DISPLAY ---
question, answer, hint_text = st.session_state.current_data

st.title("Math Adventure! 🔢✨")
st.write(f"### {question}")



# User Input
user_ans = st.number_input("Enter your answer:", step=1, value=None, key="user_input")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Submit"):
        if user_ans == answer:
            st.success("Correct! Well done! 🌟")
            st.session_state.current_data = generate_math_problem(topic_choice, level_choice)
            st.session_state.show_hint = False
            st.rerun()
        else:
            st.error("Not quite. Want to try again or see a hint?")

with col2:
    if st.button("Hint 💡"):
        st.session_state.show_hint = True

if st.session_state.show_hint:
    st.info(hint_text)

# Manual refresh for a new problem
if st.sidebar.button("New Problem 🆕"):
    st.session_state.current_data = generate_math_problem(topic_choice, level_choice)
    st.session_state.show_hint = False
    st.rerun()
