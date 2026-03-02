import streamlit as st
import random

# --- 1. THE PROBLEM GENERATOR (Returns exactly 3 items) ---
def generate_math_problem(topic, level):
    if topic == "Fractions (Word Problems)":
        # Logic for "Remainder" problems
        total = random.choice([12, 24, 36, 48, 60])
        denom1 = random.choice([2, 3, 4])
        rem = total - (total // denom1)
        
        possible_denoms = [d for d in [2, 3, 4, 5] if rem % d == 0]
        denom2 = random.choice(possible_denoms) if possible_denoms else 2
        ans = rem - (rem // denom2)
        
        story = f"You have {total} items. You give 1/{denom1} away. Then you give 1/{denom2} of the REMAINING away. How many are left?"
        hint = f"First subtract 1/{denom1} of {total}, then find 1/{denom2} of what's left!"
        return story, ans, hint

    elif topic == "Geometry":
        l, w = random.randint(2, 5+level), random.randint(2, 4+level)
        return f"Area of a {l}x{w} rectangle?", l*w, "Area = Length x Width"

    else: # Addition
        n1, n2 = random.randint(1, 10*level), random.randint(1, 10*level)
        return f"What is {n1} + {n2}?", n1+n2, "Try breaking it into parts!"

# --- 2. THE UI & SESSION STATE ---
st.set_page_config(page_title="Math Adventure")

# Reset Button (Emergency Fix for Errors)
if st.sidebar.button("Reset / Clear Errors 🔄"):
    st.session_state.clear()
    st.rerun()

st.sidebar.title("Settings ⚙️")
topic = st.sidebar.selectbox("Topic", ["Addition", "Geometry", "Fractions (Word Problems)"])
level = st.sidebar.slider("Level", 1, 10, 1)

# Initialize if empty
if 'current_data' not in st.session_state:
    st.session_state.current_data = generate_math_problem(topic, level)
    st.session_state.show_hint = False

# --- 3. THE DISPLAY (Line 59 area) ---
# This line now matches the 3 items returned above!
question, answer, hint_text = st.session_state.current_data

st.title("Math Adventure! 🔢")
st.write(f"### {question}")

user_ans = st.number_input("Answer:", step=1, value=None)

if st.button("Submit"):
    if user_ans == answer:
        st.success("Correct! 🎉")
        st.session_state.current_data = generate_math_problem(topic, level)
        st.session_state.show_hint = False
        st.rerun()
    else:
        st.error("Try again! 💪")

if st.button("Hint 💡"):
    st.session_state.show_hint = True

if st.session_state.show_hint:
    st.info(hint_text)
