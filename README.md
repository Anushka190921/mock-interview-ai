# AI-Powered Mock Interview System

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=280&color=0:4B0082,50:6A0DAD,100:8A2BE2&text=AI%20Mock%20Interview&fontColor=ffffff&fontSize=50&fontAlignY=38&animation=fadeIn"/>

<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=600&size=24&duration=2500&pause=1000&color=8A2BE2&center=true&vCenter=true&width=1000&lines=AI-Powered+Interview+Practice;Role-Specific+Question+Generation;Instant+AI+Feedback+%26+Scoring;Secure+User+Authentication;Built+with+Flask+%2B+Groq+LLM;Live+Deployed+on+Render" />

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Flask-Login](https://img.shields.io/badge/Flask--Login-Auth-6A0DAD?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq_API-LLaMA3.3-6A0DAD?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-Aiven_Cloud-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=for-the-badge)

<br/>

![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

<br/>

### 🔗 [Live Demo](https://mock-interview-ai-1kjd.onrender.com) • [GitHub](https://github.com/Anushka190921/mock-interview-ai)

</div>

---

## 📌 About

An AI-powered mock interview web app that helps candidates practice
for real job interviews. Create a free account, select your target
role and difficulty level, answer AI-generated questions, and get
instant detailed feedback with scores, strengths, improvements, and
ideal sample answers — with your full interview history saved
privately to your own account.

---

## ✨ Features

| Feature | Status |
|---------|--------|
| User Authentication (Register/Login/Logout) | ✅ Done |
| Per-User Private Interview History | ✅ Done |
| 15 Job Roles Supported | ✅ Done |
| 3 Difficulty Levels (Fresher/Mid/Senior) | ✅ Done |
| 11 Company-Specific Interview Styles | ✅ Done |
| AI Question Generation | ✅ Done |
| Answer Evaluation with Score /10 | ✅ Done |
| Strengths & Improvements Feedback | ✅ Done |
| Ideal Sample Answer | ✅ Done |
| Smart Follow-up Questions | ✅ Done |
| Live Deployment on Render | ✅ Done |
| Cloud MySQL Database (Aiven) | ✅ Done |
| PDF Report Download | ✅ Done |
| Voice Input (Web Speech API) | ⏳ Coming Soon |
| Resume-Based Question Generation | ⏳ Coming Soon |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Authentication | Flask-Login, Werkzeug password hashing |
| AI | Groq API (LLaMA 3.3 70B) |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render + Gunicorn |
| Security | python-dotenv, environment-based secrets |
| Database | MySQL (Aiven Cloud, SSL-secured) |

---

## 📸 Screenshots

### Home Page
![Home](screenshots/home.png)

### Interview Page
![Interview](screenshots/interview.png)

### Feedback Page
![Feedback](screenshots/feedback.png)

---

## 🧠 How It Works

1. User registers or logs in to a personal account

↓
2. User selects job role + difficulty level + company style

↓
3. Flask sends a tailored prompt to the Groq API

↓
4. LLaMA 3.3 generates role-specific questions

↓
5. User answers, optionally receives an adaptive follow-up question

↓
6. AI evaluates → Score + Strengths + Improvements + Sample Answer

↓
7. Results saved privately to the user's own interview history

---

## 📁 Project Structure

mock-interview-ai/

├── app.py                  ← Flask routes (auth + interview flow)

├── utils/

│   ├── llm.py              ← Groq API + MySQL integration

│   ├── models.py           ← User model + Flask-Login integration

│   └── prompts.py          ← AI prompt templates

├── templates/

│   ├── index.html          ← Public landing page

│   ├── dashboard.html      ← Role/difficulty/company selection

│   ├── login.html          ← Login page

│   ├── register.html       ← Registration page

│   ├── _navbar.html        ← Shared navbar partial

│   ├── interview.html      ← Questions page

│   ├── followup.html       ← Follow-up question page

│   └── feedback.html       ← AI feedback page

├── static/css/

│   └── style.css

├── screenshots/

├── requirements.txt

└── .env                    ← API keys & DB credentials (not on GitHub)

---

## 🚀 Run Locally

```bash
git clone https://github.com/Anushka190921/mock-interview-ai.git
cd mock-interview-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with:
```
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_generated_secret_key
MYSQL_HOST=your_mysql_host
MYSQL_PORT=your_mysql_port
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_mysql_database
```

```bash
python app.py
```

Visit `http://127.0.0.1:5000`

---

## 🚧 Challenges & Learnings

### 1. Model Deprecation
- Faced `BadRequestError` when Groq deprecated `llama3-8b-8192`
- Fixed by migrating to `llama-3.3-70b-versatile`

### 2. Prompt Engineering
- Designed strict output formats for consistent AI responses
- Used labeled sections (SCORE, STRENGTHS, IMPROVEMENTS)

### 3. Authentication & Session Security
- Implemented Flask-Login with hashed passwords (never stored in plaintext)
- Learned the hard way that a randomly regenerated `SECRET_KEY` on every
  restart silently logs every user out — fixed by persisting a fixed key
  via environment variables

### 4. Debugging a Hidden Production Bug
- Discovered that the database connection was hardcoded to `localhost`,
  which worked locally but silently failed in production the entire time
  (masked by broad exception handling)
- Migrated to a cloud-hosted MySQL instance (Aiven) with SSL, and made
  all connection details configurable via environment variables

### 5. First Deployment
- Configured Gunicorn + Render with secure environment variables

---

## 👩‍💻 Author

**Anushka** — BTech CSE (AI), 3rd Year

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anushka-773aa5337)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Anushka190921)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&section=footer&height=120&color=0:4B0082,50:6A0DAD,100:8A2BE2"/>