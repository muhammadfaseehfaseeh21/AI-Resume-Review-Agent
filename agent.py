import streamlit as st
from groq import Groq

# ---------- Groq client (key from Streamlit secrets) ----------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = (
    "You are a Senior Resume Reviewer: an experienced hiring manager and resume coach who has "
    "reviewed thousands of resumes across many industries. You know what makes a resume stand out, "
    "what recruiters skim for, and how applicant tracking systems (ATS) scan resumes for keywords. "
    "Give clear, honest, and actionable feedback to help the candidate improve their resume and "
    "their chances of getting an interview."
)


def build_user_prompt(resume_text: str, job_description: str) -> str:
    prompt = f"""Review the following resume and give detailed, constructive feedback.

RESUME:
{resume_text}
"""

    if job_description and job_description.strip():
        prompt += f"""
JOB DESCRIPTION (tailor your feedback to this role):
{job_description}
"""

    prompt += """
Structure your feedback in this format using Markdown:

1. **Overall Impression** - a short summary (2-3 sentences)
2. **Strengths** - bullet points of what works well
3. **Areas to Improve** - bullet points of specific, actionable fixes
4. **Missing Keywords / Skills** - only if a job description was provided, list important keywords
   from the job description that are missing from the resume
5. **ATS Compatibility Notes** - quick notes on formatting or structure issues that could hurt
   parsing by applicant tracking systems
6. **Overall Score** - a score out of 10 with a one-line reason

Be specific and reference actual content from the resume. Be encouraging but honest.
"""
    return prompt


def review_resume(resume_text: str, job_description: str = "") -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(resume_text, job_description)},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content
