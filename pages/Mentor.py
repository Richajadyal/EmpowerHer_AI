import streamlit as st
import google.generativeai as genai
import datetime

# ✅ Restrict access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.switch_page("app.py")

# ✅ Configure Gemini API
genai.configure(api_key="Add your API")

# 🎨 Dark Theme CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        font-family: 'Arial', sans-serif;
        color: white;
    }
    .chat-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .user {
        background-color: #2b2b2b;
        border-left: 5px solid #ff6b6b;
        color: #f1f1f1;
    }
    .bot {
        background-color: #232931;
        border-left: 5px solid #4da8da;
        color: #e8e8e8;
    }
    h1, label {
        color: #4da8da !important;
    }
    h3, label {
        color: #4da8da !important;
    }
    h2, label {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Your AI Mentor")
st.markdown("### 🌌Guidance, motivation & career advice at your fingertips!")

# ✅ Initialize chat history
if "mentor_history" not in st.session_state:
    st.session_state.mentor_history = []

# ✅ User Input
user_input = st.text_area("💬 Ask your mentor:", key="mentor_input")

if st.button("✨ Get Advice"):
    if user_input.strip():
        with st.spinner("Mentor is thinking..."):
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            response = model.generate_content(user_input)
            answer = response.text

            # ✅ Save chat
            st.session_state.mentor_history.append({
                "time": str(datetime.datetime.now().strftime("%H:%M")),
                "user": user_input,
                "bot": answer
            })

            st.success("✅ Mentor replied!")
    else:
        st.warning("⚠️ Please enter a question.")

# ✅ Display Chat History
st.markdown("---")
st.subheader("📜 Conversation History")

if len(st.session_state.mentor_history) == 0:
    st.info("No conversations yet. Ask your first question!")
else:
    for chat in reversed(st.session_state.mentor_history):
        st.markdown(f"<div class='chat-box user'><b>👩 You ({chat['time']}):</b><br>{chat['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-box bot'><b>🤖 Mentor:</b><br>{chat['bot']}</div>", unsafe_allow_html=True)

