import streamlit as st
import json, os
from datetime import date

# ✅ Restrict access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.switch_page("app.py")

# 📂 File to store goals
GOALS_FILE = "goals.json"

# ✅ Safe JSON Load
def load_goals():
    if not os.path.exists(GOALS_FILE) or os.path.getsize(GOALS_FILE) == 0:
        with open(GOALS_FILE, "w") as f:
            json.dump({}, f)
    with open(GOALS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

# ✅ Save Goals
def save_goals(data):
    with open(GOALS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ✅ Load existing goals
goals = load_goals()
username = st.session_state.get("username", "guest")
if username not in goals:
    goals[username] = []

# 🎯 Title
st.title("🎯 My Goals & Habits")

# 📌 Add New Goal
with st.form("add_goal"):
    goal_text = st.text_input("Enter your goal or habit:")
    deadline = st.date_input("Deadline", date.today())
    submitted = st.form_submit_button("➕ Add Goal")

    if submitted and goal_text.strip() != "":
        goals[username].append({"goal": goal_text, "deadline": str(deadline), "done": False})
        save_goals(goals)
        st.success("✅ Goal added successfully!")

# 📋 Display Existing Goals
st.subheader("📌 Your Goals")

if len(goals[username]) == 0:
    st.info("You have no goals yet. Start by adding one above!")
else:
    for idx, g in enumerate(goals[username]):
        col1, col2, col3 = st.columns([5, 2, 2])
        with col1:
            st.write(f"🔹 **{g['goal']}** (Deadline: {g['deadline']})")
        with col2:
            if not g["done"]:
                if st.button("✅ Mark Done", key=f"done_{idx}"):
                    goals[username][idx]["done"] = True
                    save_goals(goals)
                    st.rerun()
            else:
                st.success("✔️ Completed")
        with col3:
            if st.button("🗑️ Delete", key=f"del_{idx}"):
                goals[username].pop(idx)
                save_goals(goals)
                st.rerun()
