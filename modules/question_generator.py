def generate_questions(role, difficulty, resume_text):

    questions = []

    # AI Engineer Questions
    if role == "AI Engineer":

        if difficulty == "Easy":
            questions = [
                "What is Machine Learning?",
                "Difference between AI and ML?",
                "What is supervised learning?",
                "Explain NumPy and Pandas.",
                "Tell me about one AI project from your resume."
            ]

        elif difficulty == "Medium":
            questions = [
                "Explain overfitting and underfitting.",
                "What is feature engineering?",
                "Difference between classification and regression?",
                "Explain gradient descent.",
                "Describe your machine learning project workflow."
            ]

        else:
            questions = [
                "Explain bias-variance tradeoff.",
                "How does backpropagation work?",
                "Explain CNN and RNN.",
                "How would you deploy an ML model?",
                "Explain hyperparameter tuning."
            ]

    # Data Analyst Questions
    elif role == "Data Analyst":

        questions = [
            "Explain data cleaning.",
            "What is data visualization?",
            "Difference between Excel and SQL?",
            "Explain Pandas.",
            "Tell me about your analytics experience."
        ]

    # Default
    else:
        questions = [
            "Tell me about yourself.",
            "Explain one project from your resume.",
            "Why should we hire you?"
        ]

    return questions