import streamlit as st
import json, os

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
    for entry_date in sorted(journal_data[user].keys(), reverse=True):
        entry = journal_data[user][entry_date]

        # ✅ Ensure entry is a dictionary
        if not isinstance(entry, dict):
            entry = {}

        mood = entry.get("mood") or "Not Analyzed"
        thoughts = entry.get("thoughts", "")
        feelings = entry.get("feelings", "")
        experiences = entry.get("experiences", "")
        gratitude = entry.get("gratitude", "")
        lesson = entry.get("lesson", "")

        # 📅 Full Journal Entry Block
        st.markdown(f"🗓️ **{entry_date}** | 😊 Mood: **{mood}**")
        st.markdown(f"💭 **Thoughts:** {thoughts}")
        st.markdown(f"❤️ **Feelings:** {feelings}")
        st.markdown(f"🌟 **Experiences:** {experiences}")
        st.markdown(f"🙏 **Gratitude:** {gratitude}")
        st.markdown(f"📚 **Lesson Learned:** {lesson}")
        st.markdown("---")
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
