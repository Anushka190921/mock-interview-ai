from flask import Flask, render_template, request, session
from utils.llm import call_llm
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
@app.route("/interview", methods=["POST"])
def interview():
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


# ─── Route 3: Evaluate Answer ─────────────────────────────────────
@app.route("/feedback", methods=["POST"])
def feedback():
    role = session.get("role")
    difficulty = session.get("difficulty")
    company = session.get("company")
    question = request.form.get("question")
    answer = request.form.get("answer")

    prompt = get_evaluation_prompt(role, difficulty, company, question, answer)
    evaluation = call_llm(prompt)

    return render_template("feedback.html",
                           role=role,
                           difficulty=difficulty,
                           company=company,
                           question=question,
                           answer=answer,
                           evaluation=evaluation)


# ─── Run App ──────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)