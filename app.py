from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils.llm import call_llm, get_db_connection, generate_pdf_report
from flask import send_file
import io
from utils.prompts import get_question_prompt, get_evaluation_prompt
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from utils.models import (
    get_user_by_id, get_user_by_username, create_user,
    get_user_by_email, set_reset_token, get_user_by_reset_token, update_password
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message
import secrets
from datetime import datetime, timedelta
import re
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ─── Flask-Mail Setup ───────────────────────────────────────────────
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")
mail = Mail(app)

# ─── Flask-Login Setup ─────────────────────────────────────────────
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ─── Rate Limiting Setup ───────────────────────────────────────────
# Logged-in users are limited per account (so one account can't be
# hammered from many IPs); anonymous requests fall back to per-IP.
def rate_limit_key():
    if current_user.is_authenticated:
        return f"user:{current_user.id}"
    return get_remote_address()


limiter = Limiter(
    app=app,
    key_func=rate_limit_key,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Look up the user from MySQL by id (used by Flask-Login on every request)
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# ─── Route 1: Home Page ───────────────────────────────────────────
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("interview"))
    return render_template("index.html")



# ─── Health Check (keeps Aiven DB + Render awake) ──────────────────
@app.route("/healthz")
def healthz():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return "OK", 200
    except Exception as e:
        print("Health check DB error:", e)
        return "DB unreachable", 500


# ─── Route: Register ──────────────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per hour")
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not username or not email or not password:
        flash("All fields are required.", "error")
        return render_template("register.html")

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return render_template("register.html")

    if len(password) < 6:
        flash("Password must be at least 6 characters.", "error")
        return render_template("register.html")

    if get_user_by_username(username):
        flash("That username is already taken.", "error")
        return render_template("register.html")

    try:
        create_user(username, email, password)
    except Exception as e:
        print("Registration error:", e)
        flash("Something went wrong. That email may already be registered.", "error")
        return render_template("register.html")

    flash("Account created! You can now log in.", "success")
    return redirect(url_for("index"))


# ─── Route: Login ──────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    remember = bool(request.form.get("remember"))

    user = get_user_by_username(username)

    if user is None or not user.check_password(password):
        flash("Invalid username or password.", "error")
        return render_template("login.html")

    login_user(user, remember=remember)
    flash(f"Welcome back, {user.username}!", "success")
    return redirect(url_for("index"))


# ─── Route: Logout ─────────────────────────────────────────────────
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("login"))


# ─── Route: Forgot Password ────────────────────────────────────────
@app.route("/forgot-password", methods=["GET", "POST"])
@limiter.limit("5 per hour")
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")

    email = request.form.get("email", "").strip()
    user = get_user_by_email(email)

    # Always show the same message whether or not the email exists,
    # so this route can't be used to check which emails are registered.
    if user:
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(hours=1)
        set_reset_token(user.id, token, expiry)

        reset_link = url_for("reset_password", token=token, _external=True)
        try:
            msg = Message(
                subject="Reset your AI Mock Interview password",
                recipients=[user.email],
                body=(
                    f"Hi {user.username},\n\n"
                    f"We received a request to reset your password.\n"
                    f"Click the link below to set a new one (valid for 1 hour):\n\n"
                    f"{reset_link}\n\n"
                    f"If you didn't request this, you can safely ignore this email."
                )
            )
            mail.send(msg)
        except Exception as e:
            print("Email sending error:", e)

    flash("If that email is registered, a reset link has been sent.", "success")
    return redirect(url_for("login"))


# ─── Route: Reset Password ──────────────────────────────────────────
@app.route("/reset-password/<token>", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def reset_password(token):
    user = get_user_by_reset_token(token)

    if not user:
        flash("That reset link is invalid or has expired.", "error")
        return redirect(url_for("forgot_password"))

    if request.method == "GET":
        return render_template("reset_password.html", token=token)

    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return render_template("reset_password.html", token=token)

    if len(password) < 6:
        flash("Password must be at least 6 characters.", "error")
        return render_template("reset_password.html", token=token)

    update_password(user.id, password)
    flash("Your password has been reset. You can now log in.", "success")
    return redirect(url_for("login"))


# ─── Route 2: Generate Questions ─────────────────────────────────
@app.route("/interview", methods=["GET", "POST"])
@login_required
@limiter.limit("15 per hour", methods=["POST"])
def interview():
    if request.method == "GET":
        # Re-use previous session data
        role = session.get("role")
        difficulty = session.get("difficulty")
        company = session.get("company")
        questions = session.get("questions")
        if questions:
            return render_template("interview.html", role=role, difficulty=difficulty, company=company, questions=questions)
        return render_template("dashboard.html")

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
@login_required
@limiter.limit("15 per hour")
def followup():
    role = session.get("role")
    difficulty = session.get("difficulty")
    company = session.get("company")
    question = request.form.get("question")
    answer = request.form.get("answer")

    session["original_question"] = question
    session["original_answer"] = answer

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
@login_required
@limiter.limit("15 per hour")
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
            (user_id, role, difficulty, company, question, answer, followup_question, followup_answer, score, evaluation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, role, difficulty, company, question, answer, followup_question, followup_answer, score, evaluation))
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


# ─── Error Handlers ────────────────────────────────────────────────
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@app.errorhandler(429)
def rate_limit_error(error):
    return render_template("429.html"), 429


# ─── Route 5: View Interview History ──────────────────────────────
@app.route("/history")
@login_required
def history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM interview_history WHERE user_id = %s ORDER BY created_at DESC",
            (current_user.id,)
        )
        records = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database error:", e)
        records = []

    # Build chart data (oldest -> newest) from records with a numeric score.
    # Scores are stored as free text like "8/10" or "N/A", so we pull out
    # the first number we find and skip anything that isn't parseable.
    chart_labels = []
    chart_scores = []
    for record in reversed(records):
        match = re.search(r"(\d+(\.\d+)?)", record.get("score") or "")
        if not match:
            continue
        created_at = record.get("created_at")
        if hasattr(created_at, "strftime"):
            label = created_at.strftime("%b %d")
        else:
            label = str(created_at)
        chart_labels.append(label)
        chart_scores.append(float(match.group(1)))

    return render_template(
        "history.html",
        records=records,
        chart_labels=chart_labels,
        chart_scores=chart_scores,
    )


# ─── Route 6: Download PDF Report ─────────────────────────────────
@app.route("/download-pdf", methods=["POST"])
@login_required
def download_pdf():
    role = request.form.get("role")
    difficulty = request.form.get("difficulty")
    company = request.form.get("company")
    question = request.form.get("question")
    answer = request.form.get("answer")
    evaluation = request.form.get("evaluation")

    pdf_bytes = generate_pdf_report(role, difficulty, company, question, answer, evaluation)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="interview_report.pdf"
    )


# ─── Run App ──────────────────────────────────────────────────────
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
    app.run(debug=debug_mode)
    