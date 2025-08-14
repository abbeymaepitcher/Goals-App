import streamlit as st                       # Imports the Streamlit library that powers the app UI.
from datetime import date                    # Imports 'date' to show the current month/year in the header.

st.set_page_config(                          # Sets basic page settings (appears once, at the top of the script).
    page_title="Monthly Goals",              #   The browser tab title.
    page_icon="✅",                           #   The little emoji/icon in the tab.
    layout="centered",                       #   Centers the content for a clean look.
)

# -----------------------------
# Helper function(s)
# -----------------------------

def set_done(index: int, value: bool):       # Defines a function to update one goal's "done" status.
    """Update the 'done' flag for the goal at position 'index'."""
    st.session_state.goals[index]["done"] = value  # Flips the boolean flag for that goal.

# -----------------------------
# Session state (keeps data while you interact)
# -----------------------------

if "goals" not in st.session_state:          # If this is the first run, there's no 'goals' list yet...
    st.session_state.goals = []              # ...so create it: a list of dicts like {"text": str, "done": bool}.

if "month" not in st.session_state:          # Stores a friendly month label (e.g., "August 2025").
    st.session_state.month = date.today().strftime("%B %Y")

# -----------------------------
# Page header
# -----------------------------

st.title("Monthly Goals")                    # Big page title at the top.
st.caption("Write a goal, add it, and check it off when you're done.")  # A short, helpful subtitle.
st.subheader(st.session_state.month)         # Shows the current month and year.

# -----------------------------
# Input form (type a goal and add it)
# -----------------------------

with st.form("add_goal", clear_on_submit=True):     # A small form that groups the text box + button.
    new_goal = st.text_input("✍️ Write a goal for this month")  # Where you type the new goal.
    add_clicked = st.form_submit_button("Add goal")             # The button that submits the form.
    if add_clicked:                                    # Runs only when you click the button.
        text = new_goal.strip()                        # Remove extra spaces from the start/end.
        if text:                                       # Only add if the box wasn't empty.
            st.session_state.goals.append(             # Add one goal to the list in memory:
                {"text": text, "done": False}          #   the text you typed, and done=False (not finished yet).
            )
            st.success("Goal added ✅")                # A friendly confirmation message.
        else:
            st.warning("Type a goal before clicking *Add goal*.")  # Warn if the box was empty.

st.divider()                                           # A visual line to separate sections.

# -----------------------------
# To-do section (goals not done yet)
# -----------------------------

st.subheader("To do")                                  # Heading for the "not done" list.
has_todo = False                                       # Tracks whether we printed at least one pending goal.

for i, g in enumerate(st.session_state.goals):         # Go through every saved goal (with its index i).
    if not g["done"]:                                  # Only show goals that are NOT completed.
        has_todo = True                                # We found at least one pending goal.
        left, right = st.columns([0.1, 0.9])           # Two columns: checkbox (left) and text (right).
        left.checkbox(                                 # The checkbox the user can tick to complete it.
            " ",                                       # Empty label (we'll show the text in the right column).
            value=False,                               # Starts unchecked because it's not done yet.
            key=f"todo_{i}",                           # Unique key so Streamlit remembers this widget.
            on_change=set_done,                        # When the box changes, call our helper function...
            args=(i, True),                            # ...and tell it: mark this goal index as done=True.
            help="Check to mark as completed",         # Little tooltip shown on hover.
        )
        right.write(g["text"])                         # Shows the goal text next to the checkbox.

if not has_todo:                                       # If we didn't show any pending goals...
    st.info("No pending goals. Add one above!")        # ...inform the user gently.

st.divider()                                           # Another visual separator.

# -----------------------------
# Completed section (goals you finished)
# -----------------------------

st.subheader("Completed")                              # Heading for the completed list.
has_done = False                                       # Tracks whether we printed at least one completed goal.

for i, g in enumerate(st.session_state.goals):         # Go through every goal again...
    if g["done"]:                                      # ...but this time only the completed ones.
        has_done = True                                # We found at least one completed goal.
        left, right = st.columns([0.1, 0.9])           # Two columns again.
        left.checkbox(                                 # Checkbox is checked for a completed goal.
            " ",                                       # Empty label; we display text separately.
            value=True,                                # Starts checked because it's done.
            key=f"done_{i}",                           # Different key from the "To do" checkbox.
            on_change=set_done,                        # If you uncheck it...
            args=(i, False),                           # ...mark this goal as done=False (move it back to To do).
            help="Uncheck to move back to To do",      # Tooltip.
        )
        right.markdown(f"~~{g['text']}~~")             # The goal text, crossed out with Markdown.

if not has_done:                                       # If no goals are done yet...
    st.caption("Completed goals will appear here.")    # ...show a gentle hint.
