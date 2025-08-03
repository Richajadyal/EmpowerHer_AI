import streamlit as st
import random

# ✅ Restrict access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.switch_page("app.py")

# 🎨 Page Title
st.markdown("<h1 style='text-align:center; color:#ffde59;'>🌸Welcome to EmpowerHer AI🌸</h1>", unsafe_allow_html=True)
st.markdown("### 💪Your daily dose of motivation!")

# ✅ 100+ Empowering Quotes
quotes = [
    "🌟 Believe in yourself and all that you are.",
    "💖 You are stronger than you think.",
    "🌸 Every day is a new beginning.",
    "🔥 Turn your wounds into wisdom.",
    "🌞 Rise above the storm and you will find the sunshine.",
    "🌻 Bloom where you are planted.",
    "✨ Don’t wait for opportunity. Create it.",
    "🌺 Self-love is the greatest revolution.",
    "💃 A woman with a voice is by definition a strong woman.",
    "🏔️ Difficult roads often lead to beautiful destinations.",
    "🦋 Just when the caterpillar thought the world was over, it became a butterfly.",
    "💫 Your potential is endless.",
    "🌹 Empowered women empower the world.",
    "🔥 She remembered who she was and the game changed.",
    "💎 You are your best investment.",
    "🌻 Courage is grace under pressure.",
    "🎯 Focus on progress, not perfection.",
    "💜 Self-love is not selfish; it’s necessary.",
    "🌈 When it rains, look for rainbows.",
    "🦋 Transformation begins with self-acceptance.",
    "🌞 Let your light shine bright.",
    "💪 Strong women don’t have attitudes; they have standards.",
    "🔥 She believed she could, so she did.",
    "🌺 Grow through what you go through.",
    "🌻 Your story is your strength.",
    "💃 Dance with your fears until they become your strengths.",
    "🌼 Peace begins with self-love.",
    "🌟 Fall seven times, stand up eight.",
    "🌹 Your worth is not defined by others.",
    "💎 Be fearless in the pursuit of what sets your soul on fire.",
    "🌻 Dream big, work hard, stay humble.",
    "🌸 Celebrate every tiny victory.",
    "🔥 Turn pain into power.",
    "🌞 Be a voice, not an echo.",
    "🌺 You deserve the love you keep trying to give others.",
    "💪 Strength grows in the moments you think you can’t go on.",
    "🌻 A little progress each day adds up to big results.",
    "🔥 Your comeback is always stronger than your setback.",
    "🌼 You are enough just as you are.",
    "🦋 Evolve into the best version of yourself.",
    "🌺 EmpowerHer is your safe space to grow and shine."
]

# ✅ Display random quote
quote = random.choice(quotes)
st.markdown(f"""
<div style='background-color:#2c2c2c; padding:20px; border-radius:10px; color:white; font-size:18px; text-align:center;'>
    {quote}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 🎨 Attractive Page Navigation Cards
st.subheader("🚀 Explore EmpowerHer Features")

col1, col2 = st.columns(2)

with col1:
    if st.button("📔 My Journal", use_container_width=True):
        st.switch_page("pages/Journal.py")
    if st.button("🎯 My Goals & Habits", use_container_width=True):
        st.switch_page("pages/Goals.py")
    if st.button("📚 Resources & Helplines", use_container_width=True):
        st.switch_page("pages/Resources.py")

with col2:
    if st.button("📜 My History", use_container_width=True):
        st.switch_page("pages/History.py")
    if st.button("🤝 Find a Mentor", use_container_width=True):
        st.switch_page("pages/Mentor.py")
    if st.button("🤝 Analyze your Mood", use_container_width=True):
        st.switch_page("pages/Mood_Analyzer.py")

# ✅ Centered button for new page
st.markdown("<br>", unsafe_allow_html=True)  # spacing

center_col = st.columns([1, 2, 1])  # create 3 columns to center the middle one
with center_col[1]:
    if st.button("📊 View Mood Trends", use_container_width=True):
        st.switch_page("pages/Mood_Trends.py")

st.markdown("---")
st.success("🌷Click on any feature to start your journey of empowerment!🌷")
