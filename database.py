import sqlite3


def create_table():

    conn = sqlite3.connect("interview_data.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_results (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
                   
        interview_id TEXT,

        role TEXT,
        difficulty TEXT,
        question TEXT,
        answer TEXT,
        feedback TEXT,
                   
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()



def save_result(interview_id, role, difficulty, question, answer, feedback):
    conn = sqlite3.connect("interview_data.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO interview_results
    (interview_id, role, difficulty, question, answer, feedback)

    VALUES (?, ?, ?, ?, ?, ?)
    """, (
    interview_id,
    role,
    difficulty,
    question,
    answer,
    feedback
))

    conn.commit()

    conn.close()


def get_all_results():

    conn = sqlite3.connect("interview_data.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT  interview_id, 
            role, 
            difficulty, 
            MIN(created_at) as created_at
    FROM interview_results
    GROUP BY interview_id
    ORDER BY created_at DESC
    """,
    )

    results = cursor.fetchall()

    conn.close()

    return results

def get_interview_questions(interview_id):

    conn = sqlite3.connect("interview_data.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT question, answer, feedback
    FROM interview_results
    WHERE interview_id = ?
    """, (interview_id,))

    results = cursor.fetchall()

    conn.close()

    return results