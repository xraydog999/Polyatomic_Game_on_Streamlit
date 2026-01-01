import streamlit as st
import random

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Grp 1A & 2A Element Names Quiz")



# --- QUIZ DATA ---
# -----------------------------
quiz_data = {
    "nitrate": "NO3 1-",
    "phosphate": "PO4 3-",
    "carbonate": "CO3 2-",
    "nitrite": "NO2 1-",
    "hydroxide": "OH 1-",
    "hydronium": "H3O 1+",
    "sulfate": "SO4 2-",
    "ammonium": "NH4 1+",
    "Acetate": "CH3COO 1-"
}

import streamlit as st
import random

# --- SESSION STATE INITIALIZATION ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_index = 0
    st.session_state.Element_symbols = list(quiz_data.keys())
    random.shuffle(st.session_state.Element_symbols)
    st.session_state.quiz_over = False
    st.session_state.results = [] # Initialize a list to store results

import streamlit as st

st.title("Polyatomics Challenge")
st.header("Enter answers in two parts, formula, space, charge")
st.subheader("Example: for nitrite, enter NO2 1-")
st.subheader("                                  ")
st.write(f"Score: {st.session_state.score}/{len(quiz_data)}")

if st.session_state.quiz_over:
    st.success("Quiz Over!")
    st.write(f"Final Score: {st.session_state.score}/{len(quiz_data)}")
    
    st.subheader("Quiz Summary:")
    for result in st.session_state.results:
        symbol = result['symbol']
        correct = result['correct_answer']
        user_ans = result['user_answer']
        is_correct = result['is_correct']

        if is_correct:
            st.write(f"✅ **{symbol}**: You answered '{user_ans}' (Correct: '{correct}')")
        else:
            st.write(f"❌ **{symbol}**: You answered '{user_ans}' (Correct: '{correct}')")

else:
    current_symbol_index = st.session_state.current_index
    element_symbols = st.session_state.Element_symbols

    if current_symbol_index < len(element_symbols):
        current_symbol = element_symbols[current_symbol_index]
        correct_answer = quiz_data[current_symbol]

#       st.write(f"Type the formula, a space and charge for '{current_symbol}'?")
# new
        st.markdown(f"### Type the formula, a space, then charge for '{current_symbol}'")

        user_answer = st.text_input("Your answer (lowercase):", key=f"question_{current_symbol_index}")

        if user_answer:
            is_correct = (user_answer.lower() == correct_answer.lower())
            st.session_state.results.append({
                'symbol': current_symbol,
                'correct_answer': correct_answer,
                'user_answer': user_answer,
                'is_correct': is_correct
            })

            if is_correct:
                st.success("Correct!")
                st.session_state.score += 1
                st.session_state.current_index += 1
                if st.session_state.current_index >= len(element_symbols):
                    st.session_state.quiz_over = True
                st.rerun()
            else:
                st.error("Incorrect. Try again.")
    else:
        st.session_state.quiz_over = True
        st.rerun()

if st.session_state.quiz_over == True:
     st.balloons() # This triggers a beautiful, built-in balloon animation
     st.success("Congratulations! You finished the quiz.")