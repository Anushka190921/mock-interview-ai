import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv(REMOVED" "))

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

def text_to_pdf(text_content, output_filename):
    # Initialize the PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set a standard font (Arial, Helvetica, or Times)
    pdf.set_font("Helvetica", size=12)
    
    # Split the text by newlines and add it line-by-line
    # Setting 'ln=1' moves the cursor to the next line automatically
    for line in text_content.split('\n'):
        pdf.cell(200, 10, txt=line, ln=1)
        
    # Save the output file
    pdf.output(output_filename)

# Example Usage
my_text = "Hello World!\nThis is a simple text to PDF conversion using Python."
text_to_pdf(my_text, "output.pdf")
