from flask import Flask, render_template, request, session
from utils.llm import call_llm, get_db_connection
from utils.prompts import get_question_prompt, get_evaluation_prompt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ─── Route 1: Home Page ───────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ─── Route 2: Generate Questions ─────────────────────────────────
@app.route("/interview", methods=["GET", "POST"])
def interview():
    if request.method == "GET":
        # Re-use previous session data
        role = session.get("role")
        difficulty = session.get("difficulty")
        company = session.get("company")
        questions = session.get("questions")
        return render_template("interview.html", role=role, difficulty=difficulty, company=company, questions=questions)

    role = request.form.get("role")
    difficulty = request.form.get("difficulty")
    company = request.form.get("company")
    prompt = get_question_prompt(role, difficulty, company)
    response = call_llm(prompt)

    questions = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(line)

    session["role"] = role
    session["difficulty"] = difficulty
    session["company"] = company
    session["questions"] = questions

    return render_template("interview.html", role=role, difficulty=difficulty, company=company, questions=questions)


# ─── Route 3: Generate Follow-up Question ─────────────────────────
@app.route("/followup", methods=["POST"])
def followup():
    role = session.get("role")
    difficulty = session.get("difficulty")
    company = session.get("company")
    question = request.form.get("question")
    answer = request.form.get("answer")

    # Store original question and answer in session
    session["original_question"] = question
    session["original_answer"] = answer

    # Generate follow-up question
    from utils.prompts import get_followup_prompt
    prompt = get_followup_prompt(role, difficulty, company, question, answer)
    followup_question = call_llm(prompt)

    return render_template("followup.html",
                           role=role,
                           difficulty=difficulty,
                           company=company,
                           original_question=question,
                           original_answer=answer,
                           followup_question=followup_question)




# ─── Route 4: Evaluate Answer ─────────────────────────────────────
@app.route("/feedback", methods=["POST"])
def feedback():
    role = session.get("role")
    difficulty = session.get("difficulty")
    company = session.get("company")
    question = request.form.get("question")
    answer = request.form.get("answer")
    followup_question = request.form.get("followup_question", "")
    followup_answer = request.form.get("followup_answer", "")

    combined_answer = answer
    if followup_answer:
        combined_answer = f"""
Main Answer: {answer}

Follow-up Question: {followup_question}
Follow-up Answer: {followup_answer}
"""

    prompt = get_evaluation_prompt(role, difficulty, company, question, combined_answer)
    evaluation = call_llm(prompt)

    # Extract score from evaluation
    score = "N/A"
    for line in evaluation.split("\n"):
        if line.strip().startswith("SCORE:"):
            score = line.strip().replace("SCORE:", "").strip()
            break

    # Save to database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO interview_history
            (role, difficulty, company, question, answer, followup_question, followup_answer, score, evaluation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (role, difficulty, company, question, answer, followup_question, followup_answer, score, evaluation))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database error:", e)

    return render_template("feedback.html",
                           role=role,
                           difficulty=difficulty,
                           company=company,
                           question=question,
                           answer=answer,
                           followup_question=followup_question,
                           followup_answer=followup_answer,
                           evaluation=evaluation)



# ─── Route 5: View Interview History ──────────────────────────────
@app.route("/history")
def history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM interview_history ORDER BY created_at DESC")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database error:", e)
        records = []

    return render_template("history.html", records=records)


# ─── Run App ──────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)