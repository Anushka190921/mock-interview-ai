# 🎯 AI-Powered Mock Interview System

A web application that simulates real job interviews using AI.  
Select a role → get AI-generated questions → answer them → receive instant feedback.



## 🚀 Live Demo
> 🔗 [https://mock-interview-ai-1kjd.onrender.com](https://mock-interview-ai-1kjd.onrender.com)



## 💡 Features
- 7 job roles supported (SDE, ML Engineer, Data Scientist, PM and more)
- AI generates 5 role-specific interview questions per session
- Evaluates your answer and gives a score out of 10
- Shows strengths, improvements, and an ideal sample answer
- Clean and responsive UI



## 🛠️ Tech Stack

Backend - Python,Flask
AI - Groq API (LLaMA 3.3 70B)
Frontend - HTML, CSS, JavaScript 
Deployment - Render



## ⚙️ Run Locally

# Clone the repo
git clone https://github.com/Anushka190921/mock-interview-ai.git
cd mock-interview-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
# Create a .env file and add:
# GROQ_API_KEY=your_key_here

# Run the app
python app.py


Visit http://127.0.0.1:5000 in your browser.



## 📁 Project Structure
mock-interview-ai/
├── app.py                  # Flask routes
├── utils/
│   ├── llm.py              # Groq API integration
│   └── prompts.py          # AI prompt templates
├── templates/              # HTML pages
│   ├── index.html          # Home - role selection
│   ├── interview.html      # Questions page
│   └── feedback.html       # AI feedback page
├── static/css/
│   └── style.css           # Styling
├── requirements.txt
└── .env                    # API keys (not pushed to GitHub)




## 🧠 How It Works

1. User selects a job role on the home page
2. Flask sends the role to Groq API with a structured prompt
3. LLaMA 3.3 generates 5 role-specific interview questions
4. User picks a question and types their answer
5. AI evaluates the answer — gives score, strengths, improvements, and sample answer
6. Results displayed on the feedback page


## 📸 Screenshots

### Home Page
![Home](screenshots/home page.png)

### Interview Page
![Interview](screenshots/interview page.png)

### Feedback Page
![Feedback](screenshots/feedback page.png)


## 👩‍💻 Author
Anushka — BTech CSE (AI), 3rd Year  
LinkedIn - www.linkedin.com/in/anushka-773aa5337
• GitHub(https://github.com/Anushka190921)