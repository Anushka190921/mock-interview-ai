def get_question_prompt(role, difficulty, company, num_questions=5):
    company_styles = {
        "Google": "Focus on algorithms, data structures, system design, and problem-solving ability. Google values analytical thinking and coding efficiency.",
        "Microsoft": "Focus on coding, problem-solving, and collaborative scenarios. Microsoft values growth mindset and communication skills.",
        "Amazon": "Focus heavily on Amazon Leadership Principles like ownership, customer obsession, and delivering results. Mix technical and behavioral.",
        "Meta": "Focus on product thinking, coding, and system design. Meta values impact and moving fast.",
        "Apple": "Focus on attention to detail, innovation, and technical depth. Apple values quality and user experience.",
        "TCS": "Focus on basic programming concepts, logical reasoning, and communication skills. TCS values adaptability and learning ability.",
        "Infosys": "Focus on fundamental concepts, problem-solving, and teamwork. Infosys values process orientation and communication.",
        "Wipro": "Focus on core technical concepts, aptitude, and soft skills. Wipro values team collaboration.",
        "HCL": "Focus on technical fundamentals, project experience, and communication. HCL values practical knowledge.",
        "Early Stage Startup": "Focus on versatility, problem-solving, self-motivation, and ability to work independently. Startups value people who can wear multiple hats.",
        "Funded Startup": "Focus on technical depth, growth mindset, and ability to scale systems. Funded startups value speed and impact."
    }

    style = company_styles.get(company, "Focus on general technical and behavioral questions.")

    return f"""
You are an expert technical interviewer at {company}.
Generate {num_questions} interview questions for a {role} position.

Company: {company}
Interview Style: {style}
Difficulty Level: {difficulty}

Rules:
- Generate questions specifically matching {company} interview style
- Match {difficulty} level expectations
- Mix technical and behavioral questions
- Number each question (1. 2. 3. etc.)
- Only return the questions, nothing else
"""

def get_evaluation_prompt(role, difficulty, company, question, answer):
    return f"""
You are an expert technical interviewer at {company} evaluating a {difficulty} level candidate.

Company: {company}
Role: {role}
Level: {difficulty}
Interview Question: {question}
Candidate's Answer: {answer}

Evaluate the answer considering {company} interview standards and respond in this EXACT format:

SCORE: (give a score out of 10)

STRENGTHS:
(2-3 things the candidate did well)

IMPROVEMENTS:
(2-3 specific things they should improve based on {company} standards)

SAMPLE ANSWER:
(write an ideal answer that would impress {company} interviewers)
"""