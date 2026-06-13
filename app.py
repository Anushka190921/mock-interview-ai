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
    prompt = get_question_prompt(role, difficulty)
    response = call_llm(prompt)

    # Split response into individual questions
    questions = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(line)

    session["role"] = role
    session["difficulty"] = difficulty
    session["questions"] = questions

    return render_template("interview.html", role=role, difficulty=difficulty, questions=questions)


# ─── Route 3: Evaluate Answer ─────────────────────────────────────
@app.route("/feedback", methods=["POST"])
def feedback():
    role = session.get("role")
    difficulty = session.get("difficulty")
    question = request.form.get("question")
    answer = request.form.get("answer")

    prompt = get_evaluation_prompt(role, difficulty, question, answer)
    evaluation = call_llm(prompt)

    return render_template("feedback.html",
                           role=role,
                           difficulty=difficulty,
                           question=question,
                           answer=answer,
                           evaluation=evaluation)


# ─── Run App ──────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)