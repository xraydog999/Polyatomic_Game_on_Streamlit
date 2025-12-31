import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="Polyatomic Quiz", page_icon="🧪")

def format_latex(ion_name, formula_raw):
    """Converts 'SO4 2-' to LaTeX for Streamlit."""
    parts = formula_raw.split()
    base = parts[0]
    formatted_base = "".join([f"_{char}" if char.isdigit() else char for char in base])
    if len(parts) > 1:
        charge = parts[1]
        return f"{ion_name}: ${formatted_base}^{{{charge}}}$"
    return f"{ion_name}: ${formatted_base}$"

# --- QUIZ DATA ---
quiz_data = {
    "Sulfate": ["SO4 2-", "1 Sulfur, 4 Oxygens, -2 charge."],
    "Ammonium": ["NH4 1+", "Positive ion! 1 Nitrogen, 4 Hydrogens."],
    "Nitrate": ["NO3 1-", "Nitrogen and 3 Oxygens, -1 charge."],
    "Hydroxide": ["OH 1-", "Oxygen and Hydrogen, -1 charge."],
    "Carbonate": ["CO3 2-", "1 Carbon, 3 Oxygens, -2 charge."],
    "Phosphate": ["PO4 3-", "1 Phosphorus, 4 Oxygens, -3 charge."],
    "Hydronium": ["H3O 1+", "3 Hydrogens, 1 Oxygen, +1 charge."],
    "Nitrite": ["NO2 1-", "Nitrogen and 2 Oxygens, -1 charge."]
}

# --- SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_index = 0
    st.session_state.ion_names = list(quiz_data.keys())
    random.shuffle(st.session_state.ion_names)
    st.session_state.quiz_over = False
    st.session_state.missed_ions = [] # Track wrong answers
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# --- UI ---
st.title("🧪 Polyatomic Ion Challenge")

# Sidebar for stats
st.sidebar.metric("🏆 High Score", st.session_state.high_score)
st.sidebar.write("---")
st.sidebar.write("Goal: Master the formulas!")

if not st.session_state.quiz_over:
    # Progress Bar
    progress = st.session_state.current_index / len(quiz_data)
    st.progress(progress)
    
    current_ion = st.session_state.ion_names[st.session_state.current_index]
    correct_ans = quiz_data[current_ion][0]
    hint_text = quiz_data[current_ion][1]

    st.subheader(f"Question {st.session_state.current_index + 1} of {len(quiz_data)}")
    st.write(f"What is the formula for **{current_ion}**?")
    
    with st.form(key='quiz_form', clear_on_submit=True):
        user_input = st.text_input("Type answer (e.g., SO4 2-):").strip()
        submit = st.form_submit_button("Submit")
        
        if submit:
            # Check answer
            if user_input.replace(" ", "").lower() == correct_ans.replace(" ", "").lower():
                st.toast(f"Correct! {current_ion}", icon="✅")
                st.session_state.score += 1
            else:
                st.toast(f"Wrong: {current_ion}", icon="❌")
                # Add to missed list
                st.session_state.missed_ions.append(current_ion)
            
            # Move forward
            if st.session_state.current_index < len(st.session_state.ion_names) - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.quiz_over = True
            st.rerun()

    if st.button("Need a Hint?"):
        st.info(f"💡 {hint_text}")

else:
    # Handle High Score and Celebration
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
        st.balloons()

    st.header("Quiz Over!")
    st.write(f"## Final Score: {st.session_state.score}/{len(quiz_data)}")

    # --- REVIEW SECTION ---
    if st.session_state.missed_ions:
        st.subheader("📝 Review Your Missed Ions")
        st.write("Take a moment to study the ones you missed:")
        for ion in st.session_state.missed_ions:
            formula = quiz_data[ion][0]
            st.write(f"- {format_latex(ion, formula)}")
    else:
        st.success("Perfect Score! You're a chemistry pro! ⚗️")

    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.current_index = 0
        st.session_state.missed_ions = []
        random.shuffle(st.session_state.ion_names)
        st.session_state.quiz_over = False
        st.rerun()