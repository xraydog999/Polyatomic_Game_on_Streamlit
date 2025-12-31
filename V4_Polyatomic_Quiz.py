import streamlit as st
import random
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import datetime

# --- CONFIG & CONNECTION ---
st.set_page_config(page_title="Polyatomic Quiz", page_icon="🧪")

# Establish Google Sheets connection
# Note: This requires 'secrets' to be set up in the Streamlit Cloud dashboard
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

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

# --- SESSION STATE INITIALIZATION ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_index = 0
    st.session_state.ion_names = list(quiz_data.keys())
    random.shuffle(st.session_state.ion_names)
    st.session_state.quiz_over = False
    st.session_state.missed_ions = []
    st.session_state.submitted = False

if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# --- UI ---
st.title("🧪 Polyatomic Ion Challenge")

# Sidebar Stats
st.sidebar.metric("🏆 High Score", st.session_state.high_score)
st.sidebar.write("---")
st.sidebar.info("Type formulas with a space before the charge (e.g., XO4 3-)")

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
        user_input = st.text_input("Formula:").strip()
        submit = st.form_submit_button("Submit Answer")
        
        if submit:
            if user_input.replace(" ", "").lower() == correct_ans.replace(" ", "").lower():
                st.toast(f"Correct! {current_ion}", icon="✅")
                st.session_state.score += 1
            else:
                st.toast(f"Incorrect: {current_ion}", icon="❌")
                st.session_state.missed_ions.append(current_ion)
            
            if st.session_state.current_index < len(st.session_state.ion_names) - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.quiz_over = True
            st.rerun()

    if st.button("Need a Hint?"):
        st.info(f"💡 {hint_text}")

else:
    # Quiz Conclusion Logic
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
        st.balloons()

    st.header("🎉 Quiz Over!")
    st.write(f"## Final Score: {st.session_state.score} / {len(quiz_data)}")

    # 1. Review Missed Ions
    if st.session_state.missed_ions:
        with st.expander("📝 Review Missed Ions", expanded=True):
            for ion in st.session_state.missed_ions:
                formula = quiz_data[ion][0]
                st.write(f"• {format_latex(ion, formula)}")
    else:
        st.success("Perfect Score! You mastered them all!")

    st.divider()

    # 2. Submit Score to Teacher
    st.subheader("📤 Submit Results")
    if not st.session_state.submitted:
        student_name = st.text_input("Enter your name for the gradebook:")
        if st.button("Send Score to Teacher"):
            if student_name and conn:
                try:
                    # Create data for the new row
                    new_data = pd.DataFrame([{
                        "Name": student_name,
                        "Score": st.session_state.score,
                        "Total": len(quiz_data),
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    }])
                    
                    # Read existing data and append
                    existing_data = conn.read()
                    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                    
                    # Update the Google Sheet
                    conn.update(data=updated_data)
                    
                    st.session_state.submitted = True
                    st.success("Score recorded! Great job.")
                except Exception as e:
                    st.error("Submission failed. Ensure Sheet is connected.")
            elif not student_name:
                st.warning("Please enter your name first.")
            else:
                st.error("Database connection not found.")
    else:
        st.info("Your score has already been submitted.")

    # 3. Restart
    if st.button("Try Again"):
        st.session_state.score = 0
        st.session_state.current_index = 0
        st.session_state.missed_ions = []
        st.session_state.quiz_over = False
        st.session_state.submitted = False
        random.shuffle(st.session_state.ion_names)

        st.rerun()
