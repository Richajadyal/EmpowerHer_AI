import streamlit as st
import json
import os
import random

# 🎨 Custom CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput input {
        background-color: #2c2c2c;
        color: white;
        border-radius: 8px;
        border: 1px solid #555;
    }
    .stButton>button {
        background-color: #ff4b5c;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #ff6b81;
        color: white;
    }
    h1, h3 {
        color: #ffde59;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Title
st.markdown("<h1>🌸 EmpowerHer AI 🌸</h1>", unsafe_allow_html=True)

# ✅ Motivational Quotes
quotes = [
    "🌟 Believe in yourself and you will be unstoppable!",
    "💖 Your voice matters. Your dreams matter.",
    "🔥 Empowered women empower the world!",
    "🌈 Every day is a new chance to shine.",
    "🌻 You are stronger than you think."
]
st.markdown(f"<h3>{random.choice(quotes)}</h3>", unsafe_allow_html=True)

# ✅ File for storing users
USER_FILE = "users.json"
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ✅ Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ✅ Login / Signup Page
if not st.session_state.logged_in:
    st.subheader("🔐 Login / Signup to Get Started")

    username = st.text_input("👩 Username")
    password = st.text_input("🔑 Password", type="password")
    option = st.radio("Choose Option:", ["Login", "Signup"])

    if st.button("🚀 Submit"):
        users = load_users()

        if option == "Signup":
            if username in users:
                st.error("⚠️ Username already exists!")
            else:
                users[username] = password
                save_users(users)
                st.success("✅ Signup successful! Please login now.")
        else:  # Login
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.switch_page("pages/Dashboard.py")  # ✅ FIXED PATH
            else:
                st.error("❌ Invalid username or password!")

# ✅ If already logged in, redirect to Dashboard
else:
    st.switch_page("pages/Dashboard.py")  # ✅ FIXED PATH
