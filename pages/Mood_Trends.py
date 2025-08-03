import streamlit as st
import json, os
import matplotlib.pyplot as plt

# ✅ Restrict access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.switch_page("app.py")

st.title("📈 Mood Trends")
st.markdown("### 🔍 Track how your mood changes over time!")

# 📂 Journal file
JOURNAL_FILE = "journal.json"

# ✅ Load journal data
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w") as f:
        json.dump({}, f)

with open(JOURNAL_FILE, "r") as f:
    journal = json.load(f)

username = st.session_state.get("username", "guest")

# ✅ Check if user has any journal data
if username not in journal or len(journal[username]) == 0:
    st.info("📌 No mood data available yet. Start writing in your journal!")
else:
    dates = []
    moods = []

    for entry_date, entry in journal[username].items():
        # ✅ Prevent error if entry is a string instead of dict
        if isinstance(entry, dict):
            mood = entry.get("mood", "Not Recorded")
        else:
            mood = "Not Recorded"

        dates.append(entry_date)
        moods.append(mood)

    # ✅ Sort by date for proper timeline
    combined = sorted(zip(dates, moods))
    dates, moods = zip(*combined)

    # ✅ Plot the trend
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, moods, marker="o", color="#4a90e2")
    ax.set_xlabel("Date")
    ax.set_ylabel("Mood")
    ax.set_title("Your Mood Over Time")
    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig)

    # ✅ Show data as list too
    st.markdown("### 📜 Mood History")
    for d, m in zip(dates, moods):
        st.write(f"🗓️ **{d}** → 😀 {m}")
