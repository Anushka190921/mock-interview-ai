def get_question_prompt(role, difficulty, num_questions=5):
    return f"""
You are an expert technical interviewer.
Generate {num_questions} interview questions for a {role} position.

Difficulty Level: {difficulty}
- Fresher: Basic concepts, fundamental knowledge, simple scenarios
- Mid: Intermediate concepts, some experience required, real-world scenarios
- Senior: Advanced concepts, leadership, system design, complex scenarios

Rules:
- Generate questions specifically for {difficulty} level
- Mix technical and behavioral questions
- Number each question (1. 2. 3. etc.)
- Only return the questions, nothing else

Role: {role}
Level: {difficulty}
"""

def get_evaluation_prompt(role, difficulty, question, answer):
    return f"""
You are an expert technical interviewer evaluating a {difficulty} level candidate.

Role: {role}
Level: {difficulty}
Interview Question: {question}
Candidate's Answer: {answer}

Evaluate the answer considering the {difficulty} level expectations and respond in this EXACT format:

SCORE: (give a score out of 10)

STRENGTHS:
(2-3 things the candidate did well)

IMPROVEMENTS:
(2-3 specific things they should improve)

SAMPLE ANSWER:
(write an ideal answer for a {difficulty} level candidate)
"""