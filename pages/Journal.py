import streamlit as st
import json, os
from datetime import date

# ✅ Restrict access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.switch_page("app.py")

# 📂 File to store journal entries
JOURNAL_FILE = "journal.json"

# ✅ Safe JSON load
def load_journal():
    if not os.path.exists(JOURNAL_FILE) or os.path.getsize(JOURNAL_FILE) == 0:
        with open(JOURNAL_FILE, "w") as f:
            json.dump({}, f)
    with open(JOURNAL_FILE, "r") as f:
        return json.load(f)

# ✅ Save journal
def save_journal(data):
    with open(JOURNAL_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ✅ Load existing entries
journal = load_journal()

st.title("📔 My Personal Journal")

username = st.session_state.get("username", "guest")
if username not in journal:
    journal[username] = {}

# 📅 Today's Journal
today = str(date.today())
st.subheader(f"📅 Journal for {today}")

# ✅ Default structure if no entry exists for today
if today not in journal[username]:
    journal[username][today] = {
        "thoughts": "", "feelings": "", "experiences": "",
        "gratitude": "", "lesson": "", "mood": ""
    }

# ✅ Real Journal Sections
st.markdown("### 💭 Thoughts")
thoughts = st.text_area("Write your thoughts here:", value=journal[username][today]["thoughts"], height=100)

st.markdown("### ❤️ Feelings")
feelings = st.text_area("How are you feeling today?", value=journal[username][today]["feelings"], height=100)

st.markdown("### 🌟 Experiences")
experiences = st.text_area("Describe today's experiences:", value=journal[username][today]["experiences"], height=150)

st.markdown("### 🙏 Gratitude")
gratitude = st.text_area("What are you grateful for today?", value=journal[username][today]["gratitude"], height=80)

st.markdown("### 📚 Lesson Learned")
lesson = st.text_area("What lesson did you learn today?", value=journal[username][today]["lesson"], height=80)

# ✅ Mood Selector with full list
st.markdown("### 🙂 Mood of the Day")
mood_options = [
    "Happy", "Sad", "Angry", "Excited", "Stressed", "Confused", "Motivated",
    "Neutral", "Anxious", "Relaxed", "Tired", "Fearful", "Disgusted", "In Love", "Confident"
]
mood = st.selectbox("How are you feeling overall today?", mood_options, index=7)  # Default to "Neutral"

# ✅ Save Button
if st.button("💾 Save Today's Journal"):
    journal[username][today] = {
        "thoughts": thoughts,
        "feelings": feelings,
        "experiences": experiences,
        "gratitude": gratitude,
        "lesson": lesson,
        "mood": mood
    }
    save_journal(journal)
    st.success("✅ Journal entry saved successfully!")

# 📜 Past Entries
st.subheader("📖 Past Entries")
if len(journal[username]) == 0:
    st.info("No journal entries yet. Start writing today!")
else:
    for entry_date in sorted(journal[username].keys(), reverse=True):
        with st.expander(f"📅 {entry_date}"):
            entry = journal[username][entry_date]
            st.markdown(f"**💭 Thoughts:** {entry.get('thoughts', '')}")
            st.markdown(f"**❤️ Feelings:** {entry.get('feelings', '')}")
            st.markdown(f"**🌟 Experiences:** {entry.get('experiences', '')}")
            st.markdown(f"**🙏 Gratitude:** {entry.get('gratitude', '')}")
            st.markdown(f"**📚 Lesson Learned:** {entry.get('lesson', '')}")
            st.markdown(f"**🙂 Mood:** {entry.get('mood', 'Not Recorded')}")

            if st.button(f"🗑️ Delete {entry_date}", key=f"del_{entry_date}"):
                del journal[username][entry_date]
                save_journal(journal)
                st.rerun()
