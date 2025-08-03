import streamlit as st
import json, os
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# 🔐 Restrict access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.switch_page("app.py")

st.title("🌈 Mood Analyzer")
st.markdown("### 🧠 Analyze your mood based on your journal entries!")

# 📂 Journal file
JOURNAL_FILE = "journal.json"

# ✅ Load journal data
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w") as f:
        json.dump({}, f)

with open(JOURNAL_FILE, "r") as f:
    journal = json.load(f)

username = st.session_state.get("username", "guest")

# ✅ Small training dataset for moods
training_data = [
    # Happy
    ("I am so happy and excited today!", "Happy"),
    ("I had a great time with my friends!", "Happy"),
    ("Everything is going perfectly, I feel amazing!", "Happy"),
    ("Today is full of joy and laughter!", "Happy"),
    ("I am smiling so much, my heart feels light!", "Happy"),
    ("This is the best day of my life!", "Happy"),
    ("I feel grateful for everything I have!", "Happy"),
    ("I achieved something big today, I’m so proud!", "Happy"),
    ("Life feels beautiful and full of colors!", "Happy"),
    ("I am surrounded by positivity and love!", "Happy"),

    # Sad
    ("Feeling really sad and down.", "Sad"),
    ("Crying and feeling lonely.", "Sad"),
    ("My heart feels heavy, I want to be alone.", "Sad"),
    ("I miss the old happy days.", "Sad"),
    ("Nothing feels right, everything is dull.", "Sad"),
    ("I feel like I am losing myself.", "Sad"),
    ("It's a gloomy day and my mood matches it.", "Sad"),
    ("I can’t stop thinking about what I lost.", "Sad"),
    ("Tears keep rolling down, I feel empty.", "Sad"),
    ("I just want someone to hug me and say it's okay.", "Sad"),

    # Stressed
    ("I am stressed about my exams.", "Stressed"),
    ("Too much pressure and anxiety.", "Stressed"),
    ("I have so many deadlines, my head is spinning.", "Stressed"),
    ("I feel like I can’t handle this workload.", "Stressed"),
    ("Everything is overwhelming, I need a break.", "Stressed"),
    ("My chest feels tight with all this stress.", "Stressed"),
    ("I am overthinking every little thing.", "Stressed"),
    ("I am scared I will fail and disappoint everyone.", "Stressed"),
    ("I can't sleep properly because of all these worries.", "Stressed"),
    ("I just need some peace, this is too much.", "Stressed"),

    # Motivated
    ("I feel motivated to work harder!", "Motivated"),
    ("I can achieve anything!", "Motivated"),
    ("Nothing can stop me from reaching my goals!", "Motivated"),
    ("I am ready to conquer the world!", "Motivated"),
    ("Success is just one step away, I can feel it!", "Motivated"),
    ("Every challenge is a new opportunity to grow!", "Motivated"),
    ("I am unstoppable and full of energy!", "Motivated"),
    ("I will prove to myself how strong I am!", "Motivated"),
    ("I believe in my dreams and I will achieve them!", "Motivated"),
    ("Hard work always pays off and I’m ready to work!", "Motivated"),

    # Neutral
    ("It's just a normal day, nothing special.", "Neutral"),
    ("Calm and peaceful day.", "Neutral"),
    ("Nothing much happened today, it was okay.", "Neutral"),
    ("I feel neither good nor bad, just neutral.", "Neutral"),
    ("It was a regular day without any surprises.", "Neutral"),
    ("I am just going with the flow today.", "Neutral"),
    ("Nothing exciting, nothing sad, just a day.", "Neutral"),
    ("I feel balanced and calm.", "Neutral"),
    ("There’s nothing unusual about today.", "Neutral"),
    ("Life feels steady and quiet right now.", "Neutral"),

    # Angry
    ("I am so frustrated right now!", "Angry"),
    ("Everything is making me lose my temper.", "Angry"),
    ("I can’t stand this situation anymore.", "Angry"),
    ("Why does this always happen to me?!", "Angry"),   
    ("I feel like screaming out loud.", "Angry"),
    ("My patience is running out.", "Angry"),
    ("I hate being treated this way!", "Angry"),
    ("I am furious at what they did.", "Angry"),
    ("This makes my blood boil!", "Angry"), 
    ("I need to calm down before I explode.", "Angry"),

    # Anxious
    ("I feel nervous about what will happen next.", "Anxious"),
    ("My heart is racing for no reason.", "Anxious"),
    ("I can’t stop worrying about the future.", "Anxious"),
    ("What if everything goes wrong?", "Anxious"),
    ("I feel uneasy and restless.", "Anxious"),  
    ("I keep imagining the worst-case scenario.", "Anxious"),
    ("My mind just won’t stop overthinking.", "Anxious"),
    ("I have a constant pit in my stomach.", "Anxious"),
    ("Every little thing is making me nervous.", "Anxious"), 
    ("I can't relax, something feels off.", "Anxious"),

    # Excited
    ("I can’t wait for tomorrow, I’m so thrilled!", "Excited"),
    ("Something amazing is going to happen soon!", "Excited"),
    ("I feel like jumping with joy!", "Excited"),
    ("This is the best surprise ever!", "Excited"),
    ("My heart is pounding with excitement!", "Excited"),
    ("I can’t sit still, I’m so pumped!", "Excited"),
    ("This opportunity makes me so thrilled!", "Excited"),
    ("I feel electrified with anticipation!", "Excited"),
    ("I am counting down the seconds for this moment!", "Excited"),
    ("This is going to be unforgettable!", "Excited"),

    # Relaxed
    ("I feel so calm and at ease.", "Relaxed"),
    ("Everything feels peaceful right now.", "Relaxed"),
    ("I’m just enjoying the present moment.", "Relaxed"),
    ("This quiet moment is exactly what I needed.", "Relaxed"),
    ("I feel light and stress-free.", "Relaxed"),
    ("My mind is clear and calm.", "Relaxed"),
    ("Everything feels slow and soothing.", "Relaxed"),
    ("I am content and breathing deeply.", "Relaxed"),
    ("This calm energy feels healing.", "Relaxed"),
    ("I am fully present and at peace.", "Relaxed"),

    # Tired
    ("I just want to lie down and rest.", "Tired"),
    ("I feel completely drained of energy.", "Tired"),
    ("My body feels heavy and exhausted.", "Tired"),
    ("I can’t keep my eyes open anymore.", "Tired"),
    ("I’ve been working all day and I’m worn out.", "Tired"),
    ("I feel mentally and physically tired.", "Tired"),
    ("All I want is a good night’s sleep.", "Tired"),
    ("I need a break, I can’t go on like this.", "Tired"),
    ("I am too exhausted to even think.", "Tired"),
    ("My body is screaming for rest.", "Tired"),

    # Fearful
    ("I feel scared of what might happen.", "Fearful"),
    ("My heart is pounding with fear.", "Fearful"),
    ("I can’t shake this feeling of dread.", "Fearful"),
    ("I’m too afraid to take the next step.", "Fearful"),
    ("This situation makes me want to run away.", "Fearful"),
    ("I feel chills down my spine.", "Fearful"),
    ("I am terrified of failing.", "Fearful"),
    ("I feel paralyzed by fear.", "Fearful"),
    ("Every little noise is making me jump.", "Fearful"),
    ("I wish I could hide and feel safe.", "Fearful"),

    # Disgusted
    ("That was absolutely disgusting!", "Disgusted"),
    ("I can’t even look at it, it’s gross.", "Disgusted"),
    ("This situation makes me sick.", "Disgusted"),
    ("I feel repulsed by what I saw.", "Disgusted"),
    ("That left a bad taste in my mouth.", "Disgusted"),
    ("I can’t stand being near this.", "Disgusted"),
    ("I feel a wave of nausea just thinking about it.", "Disgusted"),
    ("This is so unpleasant and disturbing.", "Disgusted"),
    ("Everything about this makes me cringe.", "Disgusted"),
    ("I just want to get away from this.", "Disgusted"),

    # In Love
    ("My heart skips a beat when I think of them.", "In Love"),
    ("I can’t stop smiling when they text me.", "In Love"),
    ("Every little thing reminds me of them.", "In Love"),
    ("I feel butterflies in my stomach.", "In Love"),
    ("I’m falling deeper for them every day.", "In Love"),
    ("Just hearing their voice makes me happy.", "In Love"),
    ("I feel safe and cherished with them.", "In Love"),
    ("My world feels brighter when they’re around.", "In Love"),
    ("I love how they make me feel special.", "In Love"),
    ("They are always on my mind.", "In Love"),

    # Confident
    ("I know I can achieve anything I set my mind to.", "Confident"),
    ("I feel proud of my abilities.", "Confident"),
    ("I trust myself to make the right decision.", "Confident"),
    ("I am fearless and ready to take on challenges.", "Confident"),
    ("I know my worth and value.", "Confident"),
    ("I walk with self-assurance and grace.", "Confident"),
    ("I am prepared for any situation.", "Confident"),
    ("I radiate positive and strong energy.", "Confident"),
    ("I feel unstoppable today.", "Confident"),
    ("I believe in myself completely.", "Confident"),

    # Confused
    ("I have no idea what to do next.", "Confused"),
    ("Everything feels unclear right now.", "Confused"),
    ("I feel lost and unsure.", "Confused"),
    ("I can’t make sense of this situation.", "Confused"),
    ("My mind is all over the place.", "Confused"),
    ("I feel stuck between choices.", "Confused"),
    ("Nothing is making sense right now.", "Confused"),
    ("I wish I had some clarity.", "Confused"),
    ("I don’t know which way to go.", "Confused"),
    ("Everything feels like a blur.", "Confused")
]

texts, labels = zip(*training_data)

# ✅ Vectorizer + Naive Bayes Model
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X_train, labels)

# ✅ Input for mood analysis
user_text = st.text_area("✍️ Enter a sentence or your journal text:")

if st.button("🔍 Analyze Mood"):
    if user_text.strip():
        X_test = vectorizer.transform([user_text])
        prediction = model.predict(X_test)[0]

        st.success(f"🎯 **Predicted Mood:** {prediction}")

        # ✅ Save mood with journal if user exists
        if username not in journal:
            journal[username] = {}

        from datetime import date
        today = str(date.today())
        if today not in journal[username]:
            journal[username][today] = {"thoughts": "", "feelings": "", "experiences": "", "mood": prediction}
        else:
            journal[username]["mood"] = prediction

        with open(JOURNAL_FILE, "w") as f:
            json.dump(journal, f, indent=4)

        st.info("✅ Mood saved with today's journal entry!")
    else:
        st.error("⚠️ Please enter some text to analyze.")
