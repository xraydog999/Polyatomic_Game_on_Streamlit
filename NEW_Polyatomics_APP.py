import streamlit as st
import random

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Polyatomic Quiz")

def format_latex(ion_name, formula_raw):
    """Converts 'SO4 2-' to LaTeX for Streamlit."""
    parts = formula_raw.split()
    base = parts[0]
    # Wrap numbers in subscripts
    formatted_base = "".join([f"_{char}" if char.isdigit() else char for char in base])
    
    if len(parts) > 1:
        charge = parts[1]
        return f"{ion_name}: ${formatted_base}^{{{charge}}}$"
    return f"{ion_name}: ${formatted_base}$"

# --- QUIZ DATA ---
quiz_data = {
    "Sulfate": ["SO4 2-", "It contains 1 Sulfur, 4 Oxygens, and has a -2 charge."],
    "Ammonium": ["NH4 1+", "It's the only common positive polyatomic ion you'll study."],
    "Nitrate": ["NO3 1-", "Nitrogen and 3 Oxygens. Charge is -1."],
    "Hydroxide": ["OH 1-", "Just Oxygen and Hydrogen with a -1 charge."],
    "Carbonate": ["CO3 2-", "1 Carbon, 3 Oxygens. Charge is -2."],
    "Phosphate": ["PO4 3-", "1 Phosphorus, 4 Oxygens. Charge is -3."],
    "Hydronium": ["H3O 1+", "3 Hydrogens, 1 Oxygen. Charge is +1."],
    "Nitrite": ["NO2 1-", "Nitrogen and 2 Oxygens. Charge is -1."]
}

# --- SESSION STATE INITIALIZATION ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_index = 0
    st.session_state.ion_names = list(quiz_data.keys())
    random.shuffle(st.session_state.ion_names)
    st.session_state.quiz_over = False

# --- UI ---
st.title("🧪 Polyatomic Ion Challenge")

if not st.session_state.quiz_over:
    current_ion = st.session_state.ion_names[st.session_state.current_index]
    correct_ans = quiz_data[current_ion][0]
    hint_text = quiz_data[current_ion][1]

    st.subheader(f"Question {st.session_state.current_index + 1} of {len(quiz_data)}")
    st.write(f"What is the formula for **{current_ion}**?")
    
    with st.form(key='quiz_form', clear_on_submit=True):
        user_input = st.text_input("Type answer (e.g., XO2 4-):").strip()
        submit = st.form_submit_button("Submit")
        
        if submit:
            if user_input.replace(" ", "").lower() == correct_ans.replace(" ", "").lower():
                st.success(f"Correct! {format_latex(current_ion, correct_ans)}")
                st.session_state.score += 1
            else:
                st.error(f"Incorrect. The answer was {correct_ans}")
            
            if st.session_state.current_index < len(st.session_state.ion_names) - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.quiz_over = True
            
            # Using st.rerun() to refresh the page for the next question/result
            st.rerun()

    if st.button("Need a Hint?"):
        st.info(f"💡 {hint_text}")

else:
    st.balloons()
    st.header("Quiz Over!")
    st.write(f"## Final Score: {st.session_state.score}/{len(quiz_data)}")
    if st.button("Restart Quiz"):
        # Reset all session states
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
