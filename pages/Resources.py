import streamlit as st

# ✅ Restrict access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.switch_page("app.py")

# 🌸 Page Title
st.title("📚 Resources & Helplines")
st.markdown("### 💖 *EmpowerHer - Your Support & Growth Hub*")

# ✅ Collapsible Sections
with st.expander("🧠 Mental Health & Emotional Well-being", expanded=True):
    st.write("✅ **Mental Health Helpline India:** 9152987821")
    st.write("✅ **iCall (Free Counseling):** +91 9152987821 / [Website](https://icallhelpline.org/)")
    st.write("✅ **AASRA (Suicide Prevention):** +91-9820466726")
    st.write("✅ **Lifeline Foundation:** +91-9830010000")
    st.info("💖 Remember: It's okay to seek help. Your mental health matters!")

with st.expander("🚨 Women Safety & Emergency"):
    st.write("✅ **Women Helpline (India):** 181")
    st.write("✅ **Police Helpline:** 100")
    st.write("✅ **Domestic Violence Helpline:** 181 / 1091")
    st.write("✅ **National Commission for Women:** 011-26942369")
    st.warning("⚠️ In case of immediate danger, call **100** or your local police immediately.")

with st.expander("⚖️ Legal Support"):
    st.write("✅ **Free Legal Aid (India):** [NALSA Website](https://nalsa.gov.in/)")
    st.write("✅ **Know Your Rights:** [NCW](https://ncw.nic.in/)")
    st.success("📌 Knowledge of your rights is the first step towards empowerment!")

with st.expander("🎓 Free Education & Skill Building"):
    st.write("✅ **Khan Academy:** [Visit](https://www.khanacademy.org/)")
    st.write("✅ **Coursera Free Courses:** [Visit](https://www.coursera.org/)")
    st.write("✅ **Skill India Portal:** [Visit](https://skillindia.gov.in/)")
    st.write("✅ **Google Digital Skills:** [Visit](https://learndigital.withgoogle.com/digitalunlocked)")

with st.expander("💼 Career Growth & Opportunities"):
    st.write("✅ **LinkedIn Learning Free:** [Visit](https://www.linkedin.com/learning/)")
    st.write("✅ **Naukri Job Portal:** [Visit](https://www.naukri.com/)")
    st.write("✅ **Internshala Internships:** [Visit](https://internshala.com/)")
    st.success("🚀 Keep upgrading your skills, opportunities will follow!")

# ✅ Motivational Footer
st.markdown("---")
st.success("🌸 *You are strong, capable, and unstoppable. Believe in yourself!* 🌸")
