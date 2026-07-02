import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024
    )
    return response.choices[0].message.content


import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="mock_interview_db"
    )

from fpdf import FPDF

def generate_pdf_report(role, difficulty, company, question, answer, evaluation):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "AI Mock Interview Report", ln=1, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Company: {company}  |  Role: {role}  |  Level: {difficulty}", ln=1)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Question:", ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, question)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Your Answer:", ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, answer)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "AI Evaluation:", ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, evaluation)

    return pdf.output(dest="S")
