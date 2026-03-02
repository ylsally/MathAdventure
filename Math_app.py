import streamlit as st
import random
from fractions import Fraction

# --- CORE LOGIC: PROBLEM GENERATOR ---
def generate_math_problem(level):
    # 30% chance for a word problem if level > 2
    if level > 2 and random.random() < 0.3:
        themes = [
            {"item": "chanterelles", "action": "foraged in the woods", "unit": "mushrooms"},
            {"item": "Japanese stickers", "action": "bought in Nagoya", "unit": "stickers"},
            {"item": "onigiri", "action": "made for a picnic", "unit": "onigiri"}
        ]
        theme = random.choice(themes)
        
        # Ensure numbers are divisible for clean math
        total = random.choice([12, 24, 36, 48, 60])
        denom1 = random.choice([2, 3, 4])
        spent_first = total // denom1
        remaining = total - spent_first
        
        # Pick a denominator that fits the remainder
        possible_denoms = [d for d in [2, 3, 4, 5] if remaining % d == 0]
        denom2 = random.choice(possible_denoms) if possible_denoms else 2
        spent_second = remaining // denom2
        final_left = remaining - spent_second
        
        story = (f"You {theme['action']} {total} {theme['item']}. "
                 f"You gave 1/{denom1} to a friend. "
                 f"Then, you gave 1/{denom2} of the **remaining** {theme['item']} to a teacher. "
                 f"How many do you have left?")
        
        hint = (f"1. Find 1/{denom1} of {total} ({spent_first}). \n"
                f"2. Subtract that from {total} to find the remainder ({remaining}). \n"
                f"3. Now find 1/{denom2} of {remaining}!")
        
        return story, final_left, hint, "word"

    else:
        # Standard Calculation Problem
        n1 = random.randint(1, 10 + (level * 2))
        n2 = random.randint(1, 10 + (level * 2))
        return f"What is {n1} + {n2}?", n1 + n2, f"Try counting up from {n1}!", "calc"

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Math Adventure", page_icon="🔢")

if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.pending_hard_problem = None
    st.session_state.current_data = generate_math_problem(1)
    st.session_state.show_hint = False

st.title("Math Adventure! 🔢✨")
st.sidebar.write(f"### ⭐ Score: {st.session_state.score}")
st.sidebar.write(f"### 📈 Level: {st.session_state.level}")

# --- DISPLAY PROBLEM ---
question, answer, hint_text, p_type = st.session_state.current_data

if p_type == "word":
    st.info(f"**Word Problem:** {question}")
else:
    st.write(f"### {question}")

# --- USER INPUT ---
user_ans = st.number_input("Type your answer here:", step=1, value=None, key="user_input")

col1, col2 = st.columns([1, 4])
with col1:
    submit = st.button("Submit")
with col2:
    if st.button("Need a hint? 💡"):
        st.session_state.show_hint = True

if st.session_state.show_hint:
    st.warning(hint_text)
    

# --- ADAPTIVE LOGIC ---
if submit:
    if user_ans == answer:
        st.success("Correct! You're a genius! 🎉")
        st.session_state.score += 1
        st.session_state.show_hint = False
        
        if st.session_state.pending_hard_problem:
            st.session_state.current_data = st.session_state.pending_hard_problem
            st.session_state.pending_hard_problem = None
            st.info("Now, back to the one that was tricky! You got this.")
        else:
            st.session_state.level += 1
            st.session_state.current_data = generate_math_problem(st.session_state.level)
        st.rerun()
    else:
        st.error("Not quite! Let's try an easier one to warm up. 💪")
        st.session_state.pending_hard_problem = st.session_state.current_data
        st.session_state.level = max(1, st.session_state.level - 1)
        st.session_state.current_data = generate_math_problem(st.session_state.level)
        st.session_state.show_hint = False
        st.rerun()