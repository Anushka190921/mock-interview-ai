def get_question_prompt(role, num_questions=5):
    return f"""
You are an expert technical interviewer.
Generate {num_questions} interview questions for a {role} position.

Rules:
- Mix easy, medium and hard questions
- Include both technical and behavioral questions
- Number each question (1. 2. 3. etc.)
- Only return the questions, nothing else

Role: {role}
"""

def get_evaluation_prompt(role, question, answer):
    return f"""
You are an expert technical interviewer evaluating a candidate's answer.

Role they are applying for: {role}
Interview Question: {question}
Candidate's Answer: {answer}

Evaluate the answer and respond in this EXACT format:

SCORE: (give a score out of 10)

STRENGTHS:
(2-3 things the candidate did well)

IMPROVEMENTS:
(2-3 specific things they should improve)

SAMPLE ANSWER:
(write an ideal answer for this question)
"""