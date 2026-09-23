# 📄 AI Resume Reviewer

A simple AI agent that reviews resumes and gives clear, actionable feedback — built with
**Streamlit**, **CrewAI**, and **Groq**.

## Features
- Upload a resume as PDF, or paste the text directly
- Optionally paste a job description for tailored feedback
- Get structured feedback: strengths, areas to improve, missing keywords, ATS notes, and a score out of 10

## Project structure
```
resume-reviewer/
├── app.py                          # Streamlit UI
├── agent.py                        # CrewAI agent + task logic
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── secrets.toml.example        # copy to secrets.toml locally (not committed)
```

## Deploy on Streamlit Cloud (no local setup needed)
1. Push this folder to a new GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app from that repo.
3. Set the main file to `app.py`.
4. In the app's **Settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```
5. Deploy. That's it — no API key is ever entered in the app itself.

## Get a free Groq API key
Sign up at [console.groq.com](https://console.groq.com) and create an API key.

## Run locally (optional)
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml with your real key
streamlit run app.py
```
