from fpdf import FPDF


def generate_pdf(interview_id, role, difficulty, questions_answers):

    pdf = FPDF()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 20)

    pdf.cell(200, 10, "AI Interview Report", ln=True, align="C")

    pdf.ln(10)

    # Interview Info
    pdf.set_font("Arial", "B", 12)

    pdf.cell(200, 10, f"Interview ID: {interview_id}", ln=True)

    pdf.cell(200, 10, f"Role: {role}", ln=True)

    pdf.cell(200, 10, f"Difficulty: {difficulty}", ln=True)

    pdf.ln(10)

    total_score = 0

    score_count = 0

    # Questions + Answers + Feedback
    for idx, q in enumerate(questions_answers, start=1):

        question = q[0]

        answer = q[1]

        feedback = q[2]

        pdf.set_font("Arial", "B", 13)

        pdf.multi_cell(0, 10, f"Question {idx}: {question}")

        pdf.set_font("Arial", "", 12)

        pdf.multi_cell(0, 10, f"Answer:\n{answer}")

        pdf.multi_cell(0, 10, f"Feedback:\n{feedback}")

        # Extract Score
        try:

            import re

            match = re.search(r"Score:\s*(\d+)", feedback)

            if match:

                score = int(match.group(1))

                total_score += score

                score_count += 1

                pdf.set_font("Arial", "B", 12)

                pdf.cell(200, 10, f"Score: {score}/10", ln=True)

        except:

            pass

        pdf.ln(8)

    # Average Score
    average_score = round(total_score / score_count, 1) if score_count else 0

    pdf.set_font("Arial", "B", 15)

    pdf.cell(200, 10, f"Final Average Score: {average_score}/10", ln=True)

    # Save PDF
    file_name = f"Interview_Report_{interview_id}.pdf"

    pdf.output(file_name)

    return file_name