from modules.resume_parser import extract_resume_text
from modules.question_generator import generate_questions
from modules.feedback_engine import generate_feedback
from database import create_table, save_result, get_all_results, get_interview_questions
import time
import uuid

import numpy as np
import pandas as pd

import streamlit as st


# Page Config
st.set_page_config(
    
    
    page_title="AI Interview Assistant",
    page_icon="🎤",
    layout="wide"
)
create_table()

# Sidebar
st.sidebar.title("🎯 Navigation")
st.sidebar.info(
    """
    AI Interview Assistant

    Built using:
    - Python
    - Streamlit
    - HuggingFace API
    - SQLite
    - PDF Processing
    """
)

# Main Title
st.title("🎤 AI Interview Assistant")

st.markdown(
    "### Practice interviews with AI and improve your confidence"
)

st.divider()

# Resume Upload Section
st.subheader("📄 Upload Your Resume")
resume_text = ""

uploaded_file = st.file_uploader(
    
    "Upload Resume (PDF Only)",
    type=["pdf"]
)

if uploaded_file:
    st.success("Resume uploaded successfully!")

    resume_text = extract_resume_text(uploaded_file)

    st.subheader("📑 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=300
    )

st.divider()

# Interview Settings
st.subheader("⚙️ Interview Settings")

col1, col2 = st.columns(2)

with col1:
    role = st.selectbox(
        "Select Role",
        [
            "AI Engineer",
            "Data Analyst",
            "Python Developer",
            "Machine Learning Engineer",
            "Frontend Developer"
        ]
    )

with col2:
    difficulty = st.selectbox(
        "Difficulty Level",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

st.divider()

# Start Interview Button
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if st.button("🚀 Start Interview"):
    st.session_state.interview_started = True
    st.session_state.interview_id = str(uuid.uuid4())
    
if st.session_state.interview_started:

    st.success(f"Starting {difficulty} level interview for {role}")

    questions = generate_questions(
        role,
        difficulty,
        resume_text
    )

    st.subheader("🎯 Interview Questions")

    for i, question in enumerate(questions, start=1):

        st.write(f"### {i}. {question}")

        answer = st.text_area(
            f"Your Answer for Question {i}",
            key=f"answer_{i}"
        )


        if f"last_click_{i}" not in st.session_state:
            st.session_state[f"last_click_{i}"] = 0

        submit = st.button(f"Generate Feedback {i}", key=f"btn_{i}")

        if submit:

            current_time = time.time()
            if current_time - st.session_state[f"last_click_{i}"] < 30:
                
                remaining = int(30 - (current_time - st.session_state[f"last_click_{i}"]))

                st.warning(f"Please wait {remaining} seconds before generating feedback again.")


            elif answer.strip() == "":
                st.warning("Please provide an answer before generating feedback.")

            else:
               
               st.session_state[f"last_click_{i}"] = current_time

               with st.spinner("Generating feedback..."):

                   feedback = generate_feedback(question, answer)

                   save_result(
                          st.session_state.interview_id,
                          role,
                          difficulty,
                          question,
                          answer,
                          feedback
                     )

                   st.markdown(feedback)

                   st.success("Interview results saved successfully!")

        st.divider()

        # Interview History Section

st.subheader("📚 Interview History")

history = get_all_results()

if history:

    for item in history:
        
        
        interview_id = item[0]
        role_data = item[1]
        difficulty_data = item[2]
        created_at = item[3]
        



        with st.expander(f"🕒 {created_at} | {role_data} | {difficulty_data}"):

            st.write(f"Interview Session ID: {interview_id}")

            questions_answers = get_interview_questions(interview_id)

            for q in questions_answers:

                question_data = q[0]
                answer_data = q[1]
                feedback_data = q[2]
                

                st.markdown("### ❓ Question")
                st.write(question_data)
                
                st.markdown("### ✍️ Your Answer")
                st.write(answer_data)

                st.markdown("### 🤖 AI Feedback")
                st.markdown(feedback_data)
                
                st.divider()
            

else:

    st.info("No interview history found.")

st.divider()


# Analytics Dashboard

st.subheader("📊 Interview Analytics")

history = get_all_results()

if history:

    total_interviews = len(history)

    scores = []

    for item in history:

        interview_id = item[0]

        questions_answers = get_interview_questions(interview_id)

        for q in questions_answers: 

            feedback_data = q[2]

            try:

                if "Score:" in feedback_data:

                    score_text = feedback_data.split("Score:")[1].split("out")[0].strip()

                    score = int(score_text)

                    scores.append(score)

            except:
                pass

    



        try:

            if "Score:" in feedback:

                score_text = feedback.split("Score:")[1].split("out")[0].strip()

                score = int(score_text)

                scores.append(score)

        except:
            pass

    average_score = round(sum(scores) / len(scores), 1) if scores else 0

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Interviews", total_interviews)

    with col2:
        st.metric("Average Score", average_score)

else:

    st.info("No analytics available yet.")

st.divider()