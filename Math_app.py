import streamlit as st
import random

# --- 1. THE ADVANCED PROBLEM GENERATOR ---
def generate_math_problem(topic, level):
    themes = [
        {"item": "chanterelles 🍄", "action": "foraged"},
        {"item": "stickers ✨", "action": "bought in Nagoya"},
        {"item": "onigiri 🍙", "action": "made for a picnic"},
        {"item": "Yen coins 🪙", "action": "saved in a jar"},
        {"item": "apples 🍎", "action": "picked from the orchard"},
        {"item": "stamps 📮", "action": "collected from the post office"}
    ]
    theme = random.choice(themes)
    
    if topic == "Fractions (Word Problems)":
        # Level 1-3: Unit fractions (1/x)
        # Level 4-10: Non-unit fractions (2/3, 3/5, etc.)
        use_non_unit = level >= 4
        logic_type = random.choice(["remainder", "comparison", "reverse"])
        
        # Difficulty scales: Pool of denominators grows with level
        max_denom = min(5 + (level // 2), 12) 
        d1 = random.choice(range(2, max_denom + 1))
        
        # Pick a numerator: 1 for low levels, up to d1-1 for high levels
        n1 = random.randint(2, d1 - 1) if use_non_unit and d1 > 2 else 1
        
        if logic_type == "remainder":
            d2 = random.choice(range(2, 6))
            n2 = random.randint(2, d2 - 1) if use_non_unit and d2 > 2 else 1
            
            # Ensure total is divisible by both denominators
            total = d1 * d2 * random.randint(1, level + 1)
            
            # Step 1: First Fraction
            spent_first = (total // d1) * n1
            rem = total - spent_first
            
            # Step 2: Second Fraction of the REMAINING
            spent_second = (rem // d2) * n2
            ans = rem - spent_second
            
            story = (f"You {theme['action']} {total} {theme['item']}. You gave {n1}/{d1} to a friend. "
                     f"Then you gave {n2}/{d2} of the **remaining** items to your teacher. How many are left?")
            
            visual = f"Total Units: {d1}\nModel: " + "🟦" * n1 + "⬜" * (d1-n1) + f"\n(Each unit = {total//d1} items)"
            return story, ans, visual

        elif logic_type == "comparison":
            my_amt = d1 * random.randint(1, level + 1)
            friend_amt = (my_amt // d1) * n1
            
            story = (f"You {theme['action']} {my_amt} {theme['item']}. Your friend {theme['action']} "
                     f"{n1}/{d1} as many as you. How many do you have altogether?")
            
            ans = my_amt + friend_amt
            visual = f"You ({d1} units): {'🟦' * d1}\nFriend ({n1} units): {'🟩' * n1}\n(Each unit = {my_amt//d1})"
            return story, ans, visual

        else: # Reverse Logic
            parts_left = d1 - n1
            unit_val = random.randint(2, level + 3)
            current_left = unit_val * parts_left
            ans_start = unit_val * d1
            
            story = (f"After giving away {n1}/{d1} of your {theme['item']}, you have {current_left} left. "
                     f"How many did you start with?")
            
            visual = f"Left ({parts_left} units): {'⬜' * parts_left}\nMissing ({n1} units): {'❓' * n1}\n(Each unit = {unit_val})"
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
    st.session_state.problem_count = 0

# Sidebar Settings
st.sidebar.title("Settings ⚙️")
topic_choice = st.sidebar.selectbox("Choose Topic", ["Fractions (Word Problems)", "Addition", "Geometry"])
start_level = st.sidebar.slider("Starting Level", 1, 10, st.session_state.current_level)

if st.sidebar.button("Reset Game 🔄"):
    st.session_state.game_active = False
    st.session_state.current_level = 1
    st.session_state.streak = 0
    st.session_state.problem_count = 0
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

    

    # The input key changes every problem to keep the bar empty
    user_ans = st.number_input("Enter your answer:", step=1, value=None, key=f"math_input_{st.session_state.problem_count}")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Submit"):
            if user_ans == answer:
                st.balloons()
                st.success(f"Correct! Leveling up to {st.session_state.current_level + 1}! 🌟")
                
                # AUTO-LEVEL INCREASE
                st.session_state.current_level += 1
                st.session_state.streak += 1
                st.session_state.problem_count += 1
                
                # Generate new problem
                st.session_state.current_data = generate_math_problem(topic_choice, st.session_state.current_level)
                st.session_state.show_visual = False
                st.rerun()
            else:
                st.error("Not quite! Try using the 'Visual Model' below to see the units.")
                st.session_state.streak = 0

    with col2:
        if st.button("👁️ Show Visual Model"):
            st.session_state.show_visual = True

    if st.session_state.show_visual:
        st.markdown("#### Visual Hint (Bar Model):")
        st.code(visual_aid) 

    st.sidebar.write(f"**Current Streak:** {'🔥' * st.session_state.streak if st.session_state.streak > 0 else '0'}")
