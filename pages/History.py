import streamlit as st
import json, os
import pandas as pd
import plotly.express as px

# 🔐 Restrict access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.switch_page("app.py")

st.title("📜 Your History")
st.markdown("### ✨**Look back at your journey and celebrate your progress!**")

# 📂 Journal file
JOURNAL_FILE = "journal.json"
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w") as f:
        json.dump({}, f)

with open(JOURNAL_FILE, "r") as f:
    journal_data = json.load(f)

# 📂 Goals file
GOALS_FILE = "goals.json"
if not os.path.exists(GOALS_FILE):
    with open(GOALS_FILE, "w") as f:
        json.dump({}, f)

with open(GOALS_FILE, "r") as f:
    goals_data = json.load(f)

# ✅ Current user
user = st.session_state.get("username", "Guest")

# ✅ Show Journal History with Mood
st.subheader("📖 Your Journal Entries")
if user in journal_data and journal_data[user]:
    mood_records = []
    for entry_date in sorted(journal_data[user].keys(), reverse=True):
        entry = journal_data[user][entry_date]

        # ✅ Fix: Ensure entry is a dictionary before using .get()
        if not isinstance(entry, dict):
            entry = {}

        mood = entry.get("mood", "Not Analyzed")
        st.markdown(f"🗓️ **{entry_date}** | 😊 Mood: **{mood}**")
        st.write(f"💭 **Thoughts:** {entry.get('thoughts', '')}")
        st.write(f"❤️ **Feelings:** {entry.get('feelings', '')}")
        st.write(f"🌟 **Experiences:** {entry.get('experiences', '')}")
        st.markdown("---")

        mood_records.append({"Date": entry_date, "Mood": mood})

    # ✅ Mood Trend Graph
    df = pd.DataFrame(mood_records)
    if len(df) > 0:
        st.subheader("📈 Mood Trend Over Time")
        fig = px.line(df, x="Date", y="Mood", markers=True, title="Your Mood Journey")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("✍️ You haven't written anything in your journal yet.")

# ✅ Show Goals History
st.subheader("🎯 Your Goals")
if user in goals_data and goals_data[user]:
    for goal in goals_data[user]:
        status = "✅ Done" if goal.get("done", False) else "⏳ In Progress"
        st.markdown(f"🗓️ **{goal.get('deadline', '')}** - 🎯 *{goal.get('goal', '')}* - {status}")
else:
    st.info("🎯 You haven't set any goals yet.")
