import streamlit as st
import random

# --- 1. THE VISUAL PROBLEM GENERATOR ---
def generate_math_problem(topic, level):
    themes = [
        {"item": "chanterelles 🍄", "action": "foraged"},
        {"item": "stickers ✨", "action": "bought in Nagoya"},
        {"item": "onigiri 🍙", "action": "made for a picnic"},
        {"item": "coins 🪙", "action": "saved in a jar"}
    ]
    theme = random.choice(themes)
    
    if topic == "Fractions (Word Problems)":
        logic_type = random.choice(["remainder", "comparison", "reverse"])
        
        if logic_type == "remainder":
            d1, d2 = random.randint(2, 4), random.randint(2, 4)
            total = d1 * d2 * random.randint(1, level + 1)
            rem = total - (total // d1)
            ans = rem - (rem // d2)
            
            story = (f"You {theme['action']} {total} {theme['item']}. You gave 1/{d1} to a friend. "
                     f"Then you gave 1/{d2} of the **remaining** to your teacher. How many are left?")
            
            # Create a simple emoji bar model for 1/d1
            bar = "🟦" * (total // d1) + "⬜" * rem
            visual = f"Step 1 (The Total): {bar} \n(🟦 = given to friend, ⬜ = what's left)"
            return story, ans, visual

        elif logic_type == "comparison":
            d1 = random.choice([2, 3, 4, 5])
            my_amt = d1 * random.randint(1, level + 2)
            friend_amt = (my_amt // d1) * (d1 - 1)
            
            story = (f"You {theme['action']} {my_amt} {theme['item']}. Your friend {theme['action']} "
                     f"{(d1-1)}/{d1} as many as you. How many do you have altogether?")
            
            visual = f"You: {'🟦' * my_amt}\nFriend: {'🟩' * friend_amt}"
            return story, my_amt + friend_amt, visual

        else: # Reverse
            d1 = random.randint(3, 5)
            ans_start = d1 * random.randint(1, level + 2)
            left = (ans_start // d1) * (d1 - 1)
            
            story = (f"After giving away 1/{d1} of your {theme['item']}, you have {left} left. "
                     f"How many did you start with?")
            
            visual = f"Current ({(d1-1)}/{d1}): {'⬜' * left}\nMissing (1/{d1}): {'❓' * (ans_start // d1)}"
            return story, ans_start, visual

    # (Add your Geometry and Addition logic back here)
    return "Sample Question", 0, "No visual yet"

# --- 2. THE UI ---
st.set_page_config(page_title="Math Adventure", page_icon="🎒")

if 'game_active' not in st.session_state:
    st.session_state.game_active = False

# Sidebar settings
st.sidebar.title("Settings ⚙️")
topic_choice = st.sidebar.selectbox("Choose Topic", ["Fractions (Word Problems)", "Addition", "Geometry"])
level_choice = st.sidebar.slider("Level", 1, 10, 1)

if not st.session_state.game_active:
    st.title("Welcome to Math Adventure! 🗺️")
    if st.button("🚀 Start My Adventure"):
        st.session_state.current_data = generate_math_problem(topic_choice, level_choice)
        st.session_state.game_active = True
        st.session_state.show_visual = False
        st.rerun()
else:
    question, answer, visual_aid = st.session_state.current_data
    st.title("Challenge Time! ⚔️")
    st.write(f"### {question}")

    

    user_ans = st.number_input("Answer:", step=1, value=None, key="math_input")
    
    if st.button("Submit"):
        if user_ans == answer:
            st.success("Great job! 🎉")
            st.session_state.current_data = generate_math_problem(topic_choice, level_choice)
            st.session_state.show_visual = False
            st.rerun()
        else:
            st.error("Try again! Use the 'Visual Mode' if you're stuck.")

    if st.button("👁️ Show Visual Model"):
        st.session_state.show_visual = True

    if st.session_state.show_visual:
        st.code(visual_aid) # st.code keeps the emojis lined up perfectly
