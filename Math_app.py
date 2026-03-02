import streamlit as st
import random

# --- 1. THE ADVANCED PROBLEM GENERATOR ---
def generate_math_problem(topic, level):
    themes = [
        {"item": "chanterelles 🍄", "action": "foraged"},
        {"item": "stickers ✨", "action": "bought in Nagoya"},
        {"item": "onigiri 🍙", "action": "made for a picnic"},
        {"item": "Yen coins 🪙", "action": "saved in a jar"}
    ]
    theme = random.choice(themes)
    
    if topic == "Fractions (Word Problems)":
        # Randomly choose between 3 logic types
        logic_type = random.choice(["remainder", "comparison", "reverse"])
        
        # Difficulty scales: Pool of denominators grows with level
        max_denom = min(5 + (level // 2), 12) 
        denom_pool = list(range(2, max_denom + 1))
        
        if logic_type == "remainder":
            d1, d2 = random.choice(denom_pool), random.choice(denom_pool)
            total = d1 * d2 * random.randint(1, level + 1)
            rem = total - (total // d1)
            ans = rem - (rem // d2)
            story = (f"You {theme['action']} {total} {theme['item']}. You gave 1/{d1} to a friend. "
                     f"Then you gave 1/{d2} of the **remaining** to your teacher. How many are left?")
            visual = f"Step 1: 🟦" * (total // d1) + "⬜" * rem + f"\n(Blue = Friend's, White = Remainder)"
            return story, ans, visual

        elif logic_type == "comparison":
            d1 = random.choice(denom_pool)
            my_amt = d1 * random.randint(1, level + 1)
            friend_amt = (my_amt // d1) * (d1 - 1)
            story = (f"You {theme['action']} {my_amt} {theme['item']}. Your friend {theme['action']} "
                     f"{(d1-1)}/{d1} as many as you. How many do you have altogether?")
            visual = f"You: {'🟦' * my_amt}\nFriend: {'🟩' * friend_amt}"
            return story, my_amt + friend_amt, visual

        else: # Reverse Logic
            d1 = random.choice(denom_pool)
            ans_start = d1 * random.randint(1, level + 1)
            left = (ans_start // d1) * (d1 - 1)
            story = (f"After giving away 1/{d1} of your {theme['item']}, you have {left} left. "
                     f"How many did you start with?")
            visual = f"What you have ({(d1-1)}/{d1}): {'⬜' * left}\nWhat's missing (1/{d1}): {'❓' * (ans_start // d1)}"
            return story, ans_start, visual

    elif topic == "Geometry":
        l, w = random.randint(2, 5 + level), random.randint(2, 4 + level)
        return f"What is the AREA of a {l}x{w} rectangle?", l * w, f"Formula: {l} units × {w} units"
    
    else: # Addition
        n1, n2 = random.randint(1, 10 * level), random.randint(1, 10 * level)
        return f"What is {n1} + {n2}?", n1 + n2, "Try adding the tens first, then the ones!"

# --- 2. THE UI & AUTO-LEVELING STATE ---
st.set_page_config(page_title="Math Adventure", page_icon="🎒")

if 'game_active' not in st.session_state:
    st.session_state.game_active = False
    st.session_state.current_level = 1
    st.session_state.streak = 0

# Sidebar Settings
st.sidebar.title("Settings ⚙️")
topic_choice = st.sidebar.selectbox("Choose Topic", ["Fractions (Word Problems)", "Addition", "Geometry"])
start_level = st.sidebar.slider("Starting Level", 1, 10, st.session_state.current_level)

if st.sidebar.button("Reset Game 🔄"):
    st.session_state.game_active = False
    st.session_state.current_level = 1
    st.session_state.streak = 0
    st.rerun()

# --- 3. THE GAME FLOW ---
if not st.session_state.game_active:
    st.title("Welcome to Math Adventure! 🗺️")
    st.write("Ready to level up your math skills?")
    if st.button("🚀 Start My Adventure"):
        st.session_state.current_level = start_level
        st.session_state.current_data = generate_math_problem(topic_choice, st.session_state.current_level)
        st.session_state.game_active = True
        st.session_state.show_visual = False
        st.rerun()
else:
    question, answer, visual_aid = st.session_state.current_data
    
    st.title(f"Level {st.session_state.current_level} Challenge ⚔️")
    st.write(f"### {question}")

    

    user_ans = st.number_input("Enter your answer:", step=1, value=None, key="math_input")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Submit"):
            if user_ans == answer:
                st.balloons()
                st.success(f"Correct! Leveling up to {st.session_state.current_level + 1}! 🌟")
                
                # AUTO-LEVEL INCREASE
                st.session_state.current_level += 1
                st.session_state.streak += 1
                
                # Generate new problem with NEW level
                st.session_state.current_data = generate_math_problem(topic_choice, st.session_state.current_level)
                st.session_state.show_visual = False
                st.rerun()
            else:
                st.error("Not quite! Try using the 'Visual Model' below to see the parts.")
                st.session_state.streak = 0

    with col2:
        if st.button("👁️ Show Visual Model"):
            st.session_state.show_visual = True

    if st.session_state.show_visual:
        st.markdown("#### Visual Hint:")
        st.code(visual_aid) # Keeps emojis aligned in a neat box

    st.sidebar.write(f"**Current Streak:** {'🔥' * st.session_state.streak if st.session_state.streak > 0 else '0'}")
