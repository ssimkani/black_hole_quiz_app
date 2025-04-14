import streamlit as st
import json

# Load questions from JSON file
with open("questions/questions.json", "r") as f:
    questions = json.load(f)

with open("style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.q_idx = 0
    st.session_state.show_result = False

st.title("🕳️ Black Hole Quiz")

# Quiz Logic
if st.session_state.q_idx < len(questions):
    q = questions[st.session_state.q_idx]
    st.subheader(f"Question {st.session_state.q_idx + 1} of {len(questions)}")
    st.write(q["question"])

    answer = st.radio("Select an answer:", q["choices"])

    if st.button("Submit Answer"):
        if answer == q["answer"]:
            st.session_state.score += 1
            st.success("Correct!")
        else:
            st.error(f"Incorrect. Correct answer: {q['answer']}")

        st.info(f"Explanation: {q['explanation']}")
        st.session_state.q_idx += 1

        if st.session_state.q_idx == len(questions):
            if st.button("Finish Quiz"):
                st.session_state.show_result = True

        elif st.button("Next Question"):
            st.rerun()

else:
    st.session_state.show_result = True

# Results and restart
if st.session_state.show_result:
    st.markdown("## 🎉 Quiz Complete!")
    st.success(f"Your score: {st.session_state.score} / {len(questions)}")

    with st.expander("📚 Sources Used"):
        unique_sources = []
        for q in questions:
            src = q["source"]
            if src["url"] not in [s["url"] for s in unique_sources]:
                unique_sources.append(src)
        for src in unique_sources:
            st.markdown(f"- [{src['title']}]({src['url']})")

    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.q_idx = 0
        st.session_state.show_result = False
        st.rerun()
