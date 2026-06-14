# AI-Powered Mock Interview System

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=280&color=0:4B0082,50:6A0DAD,100:8A2BE2&text=AI%20Mock%20Interview&fontColor=ffffff&fontSize=50&fontAlignY=38&animation=fadeIn"/>

<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=600&size=24&duration=2500&pause=1000&color=8A2BE2&center=true&vCenter=true&width=1000&lines=AI-Powered+Interview+Practice;Role-Specific+Question+Generation;Instant+AI+Feedback+%26+Scoring;Built+with+Flask+%2B+Groq+LLM;Live+Deployed+on+Render" />

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-LLaMA3.3-6A0DAD?style=for-the-badge)
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
for real job interviews. Select your target role and difficulty level,
answer AI-generated questions, and get instant detailed feedback
with scores, strengths, improvements, and ideal sample answers.

---

## ✨ Features

| Feature | Status |
|---------|--------|
| 15 Job Roles Supported | ✅ Done |
| 3 Difficulty Levels (Fresher/Mid/Senior) | ✅ Done |
| AI Question Generation | ✅ Done |
| Answer Evaluation with Score /10 | ✅ Done |
| Strengths & Improvements Feedback | ✅ Done |
| Ideal Sample Answer | ✅ Done |
| Live Deployment on Render | ✅ Done |
| Voice Input | ⏳ Coming Soon |
| Interview History | ⏳ Coming Soon |
| PDF Report Download | ⏳ Coming Soon |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| AI | Groq API (LLaMA 3.3 70B) |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render + Gunicorn |
| Security | python-dotenv |

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

1.User selects job role + difficulty level

↓
2.Flask sends prompt to Groq API

↓
3.LLaMA 3.3 generates 5 role-specific questions

↓
4.User picks a question and types their answer

↓
5.AI evaluates → Score + Strengths + Improvements + Sample Answer

↓
6.Results displayed on feedback page

---

## 📁 Project Structure

mock-interview-ai/

├── app.py                  ← Flask routes

├── utils/

│   ├── llm.py              ← Groq API integration

│   └── prompts.py          ← AI prompt templates

├── templates/

│   ├── index.html          ← Home page

│   ├── interview.html      ← Questions page

│   └── feedback.html       ← AI feedback page

├── static/css/

│   └── style.css

├── screenshots/

├── requirements.txt

└── .env                    ← API keys (not on GitHub)

---

## 🚀 Run Locally

```bash
git clone https://github.com/Anushka190921/mock-interview-ai.git
cd mock-interview-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Add GROQ_API_KEY to .env file
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

### 3. Session Management
- Used Flask `session` to persist data across multiple routes

### 4. First Deployment
- Configured Gunicorn + Render with secure environment variables

---

## 👩‍💻 Author

**Anushka** — BTech CSE (AI), 2nd Year

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anushka-773aa5337)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Anushka190921)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&section=footer&height=120&color=0:4B0082,50:6A0DAD,100:8A2BE2"/>