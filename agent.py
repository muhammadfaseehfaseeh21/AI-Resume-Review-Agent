import streamlit as st
from crewai import Agent, Task, Crew, LLM

# ---------- LLM setup (Groq, key from Streamlit secrets) ----------
llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=st.secrets["GROQ_API_KEY"],
)

# ---------- Agent ----------
resume_reviewer = Agent(
    role="Senior Resume Reviewer",
    goal="Give clear, honest, and actionable feedback to help the candidate improve their resume "
         "and their chances of getting an interview.",
    backstory=(
        "You are an experienced hiring manager and resume coach who has reviewed thousands of resumes "
        "across many industries. You know what makes a resume stand out, what recruiters skim for, "
        "and how applicant tracking systems (ATS) scan resumes for keywords."
    ),
    llm=llm,
    verbose=False,
)


def build_task_description(resume_text: str, job_description: str) -> str:
    base = f"""
Review the following resume and give detailed, constructive feedback.

RESUME:
{resume_text}
"""

    if job_description and job_description.strip():
        base += f"""
JOB DESCRIPTION (tailor your feedback to this role):
{job_description}
"""

    base += """
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
    return base


def review_resume(resume_text: str, job_description: str = "") -> str:
    task = Task(
        description=build_task_description(resume_text, job_description),
        expected_output="Well-structured Markdown feedback following the requested format.",
        agent=resume_reviewer,
    )

    crew = Crew(agents=[resume_reviewer], tasks=[task], verbose=False)
    result = crew.kickoff()
    return str(result)
