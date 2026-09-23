import streamlit as st
from pypdf import PdfReader
from agent import review_resume

st.set_page_config(page_title="AI Resume Reviewer", page_icon="📄", layout="centered")

st.title("📄 AI Resume Reviewer")
st.write("Upload your resume (PDF or paste text) and optionally a job description. "
         "The AI agent will review it and give you clear, actionable feedback.")

# ---------- Helper: extract text from PDF ----------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


# ---------- Resume input ----------
st.subheader("1. Your Resume")
input_method = st.radio("How do you want to provide your resume?", ["Upload PDF", "Paste text"])

resume_text = ""

if input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("Reading your PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)
        if resume_text:
            st.success("Resume text extracted successfully.")
        else:
            st.error("Couldn't extract text from this PDF. Try pasting the text instead.")
else:
    resume_text = st.text_area("Paste your resume text here", height=250)

# ---------- Job description (optional) ----------
st.subheader("2. Job Description (optional)")
job_description = st.text_area(
    "Paste the job description to get feedback tailored to this role",
    height=150,
    placeholder="Leave blank for a general resume review"
)

# ---------- Run review ----------
st.subheader("3. Get Feedback")

if st.button("Review My Resume", type="primary"):
    if not resume_text.strip():
        st.warning("Please upload or paste your resume first.")
    else:
        with st.spinner("The AI agent is reviewing your resume... this can take a moment."):
            try:
                feedback = review_resume(resume_text, job_description)
                st.markdown("### 📝 Feedback")
                st.markdown(feedback)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown("---")
st.caption("Built with Streamlit, CrewAI, and Groq.")
