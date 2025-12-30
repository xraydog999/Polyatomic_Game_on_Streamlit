# Polyatomic Quiz
# !pip install chemformula
from IPython.display import display, Markdown
import random # Import the random module

def format_latex(ion_name, formula_raw):
    """Converts simple text like 'SO4 2-' to beautiful LaTeX."""
    # Split the base from the charge
    parts = formula_raw.split()
    base = parts[0]
    # Wrap numbers in subscripts for LaTeX
    formatted_base = "".join([f"_{char}" if char.isdigit() else char for char in base])

    if len(parts) > 1:
        charge = parts[1]
        return f"$\text{{{ion_name}}}: {formatted_base}^{{{charge}}}$"
    return f"$\text{{{ion_name}}}: {formatted_base}$"

# --- QUIZ DATA ---
# Format: "Ion Name": ["Correct Code", "Hint Text"]
quiz_data = {
    "Sulfate": ["SO4 2-", "It contains 1 Sulfur, 4 Oxygens, and has a -2 charge."],
    "Ammonium": ["NH4 1+", "It's the only common positive polyatomic ion you'll study."],
    "Nitrate": ["NO3 1-", "Nitrogen and 3 Oxygens. Charge is -1."],
    "Hydroxide": ["OH 1-", "Just Oxygen and Hydrogen with a -1 charge."],
    "Carbonate": ["CO3 2-", "Just Oxygen and Hydrogen with a -1 charge."],
    "Phosphate": ["PO4 3-", "Just Oxygen and Hydrogen with a -1 charge."],
    "Hydronium": ["H3O 1+", "Just Oxygen and Hydrogen with a -1 charge."],
    "Nitrite": ["NO2 1-", "Just Oxygen and Hydrogen with a -1 charge."]
}

score = 0

display(Markdown("<h1>🧪 Polyatomic Ion Challenge</h1>"))
display(Markdown("<h3>Type your answer like this: <b>SO4 2-</b> (Base + Space + Charge). Type <b>'hint'</b> if you need help!</h3>"))

# Get the keys and shuffle them
ion_names = list(quiz_data.keys())
random.shuffle(ion_names)

for ion in ion_names: # Iterate through the shuffled ion names
    info = quiz_data[ion] # Get the info for the current ion
    correct_ans = info[0]
    hint_text = info[1]

    while True:
        user_input = input(f"\nWhat is the formula for {ion}? ").strip()

        if user_input.lower() == "hint":
            display(Markdown(f"<span style='font-size: x-large;'>💡 HINT: {hint_text}</span>"))
            continue

        # Check answer (ignoring case and extra spaces)
        if user_input.replace(" ", "").lower() == correct_ans.replace(" ", "").lower():
            display(Markdown(f"<span style='font-size: x-large; color: green;'>✅ **Correct!**</span> <span style='font-size: x-large;'>{format_latex(ion, correct_ans)}</span>"))
            score += 1
            break
        else:
            display(Markdown("<span style='font-size: x-large; color: red;'>❌ Not quite. Try again or type 'hint'.</span>"))
            break

display(Markdown(f"--- \n## Quiz Over! Final Score: {score}/{len(quiz_data)}"))


