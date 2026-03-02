import streamlit as st
import random

# --- 1. THE PROBLEM GENERATOR (Your rigorous scaling logic) ---
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
        denom_pool = list(range(2, 2 + level * 3))  
        d1, d2 = random.choice(denom_pool), random.choice(denom_pool)
        factor = random.randint(1, level * 5)
        total = d1 * d2 * factor

        gave_away_first = total // d1
        remainder = total - gave_away_first
        gave_away_second = remainder // d2
        final_left = remainder - gave_away_second

        story = (f"You {theme['action']} {total} {theme['item']}. "
                 f"You gave 1/{d1} to a friend. "
                 f"Then you gave 1/{d2} of the **remaining** items to your teacher. "
                 f"How many do you have left?")
        hint = (f"Step 1: 1/{d1} of {total} = {gave_away_first}. "
                f"Step 2: Remainder is {remainder}. "
                f"Step 3: 1/{d2} of {remainder} = {gave_away_second}.")
        return story, final_left, hint

    elif topic == "Geometry":
        l, w = random.randint(2, 5 + level), random.randint(2, 4 + level)
        return f"What is the AREA of a {l}x{w} rectangle?", l * w, "Area = L × W"
    else:
        n1, n2 = random.randint(1, 10 * level), random.randint(1, 10 * level)
        return f"What is {n1} + {n2}?", n1 + n2, "Break it into tens and ones!"

# --- 2. THE UI & STATE ---
st.set_page_config(page_title="Math Adventure", page_icon="🎒")

# Initialize game state
if 'game_active' not in st.session_state:
    st.session_state.game_active = False

# Sidebar
st.sidebar.title("Configuration ⚙️")
topic_choice = st.sidebar.selectbox("Choose Topic", ["Fractions (Word Problems)", "Addition", "Geometry"])
level_choice = st.sidebar.slider("Difficulty Level", 1, 10, 1)

if st.sidebar.button("Reset App 🔄"):
    st.session_state.game_active = False
    st.session_state.clear()
    st.rerun()

# --- 3. THE "LOBBY" VS. THE "GAME" ---
if not st.session_state.game_active:
    st.title("Welcome to Math Adventure! 🗺️")
    st.write("Pick your topic and level in the sidebar, then press the button below to start.")
    
    if st.button("🚀 Start My Adventure"):
        st.session_state.current_data = generate_math_problem(topic_choice, level_choice)
        st.session_state.game_active = True
        st.session_state.show_hint = False
        st.rerun()
else:
    # Game is active - Display the problem
    question, answer, hint_text = st.session_state.current_data
    
    st.title("Current Challenge ⚔️")
    st.info(f"Topic: {topic_choice} | Level: {level_choice}")
    st.write(f"### {question}")
    
    
    
    user_ans = st.number_input("Enter your answer:", step=1, value=None, key="math_input")
    
    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("Submit"):
            if user_ans == answer:
                st.success("Correct! 🌟")
                st.session_state.current_data = generate_math_problem(topic_choice, level_choice)
                st.session_state.show_hint = False
                st.rerun()
            else:
                st.error("Try again! You can use a hint if you're stuck.")
    with c2:
        if st.button("Hint 💡"):
            st.session_state.show_hint = True
            
    if st.session_state.show_hint:
        st.warning(hint_text)
