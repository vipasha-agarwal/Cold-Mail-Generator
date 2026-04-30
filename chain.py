import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def _extract_json_block(text):
    fenced_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1)
    return text


def _get_groq_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return None


class Chain:
    def __init__(self):
        api_key = _get_groq_api_key()
        if not api_key:
            raise ValueError(
                "Missing GROQ_API_KEY. Add it to Streamlit secrets or a local .env file."
            )

        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    def _complete(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""

    def extract_jobs(self, cleaned_text):
        prompt_extract = f"""
### SCRAPED TEXT FROM WEBSITE:
{cleaned_text}

### INSTRUCTION:
The scraped text is from a careers page or job post.
Extract job postings and return valid JSON only.

Return either:
- a JSON array of jobs, or
- one JSON object for a single job

Each job should contain these keys:
- role
- experience
- skills
- description

Rules:
- "skills" must be an array of strings
- do not include markdown
- do not include explanations
### VALID JSON:
"""
        raw_response = self._complete(prompt_extract)
        json_text = _extract_json_block(raw_response)

        try:
            parsed = json.loads(json_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "The model could not parse the job page into JSON. Try a simpler job URL."
            ) from exc

        jobs = parsed if isinstance(parsed, list) else [parsed]
        normalized_jobs = []
        for job in jobs:
            if not isinstance(job, dict):
                continue
            normalized_jobs.append(
                {
                    "role": job.get("role", ""),
                    "experience": job.get("experience", job.get("expirence", "")),
                    "skills": job.get("skills", []) or [],
                    "description": job.get("description", ""),
                }
            )
        return normalized_jobs

    def write_mail(self, job, links):
        prompt_email = f"""
### JOB DESCRIPTION:
{job}

### RELEVANT PORTFOLIO LINKS:
{links}

### INSTRUCTION:
You are Mohan, a business development executive at AtliQ.
AtliQ is an AI and Software Consulting company that helps clients automate processes,
scale operations, and improve efficiency with custom digital solutions.

Write a concise cold email to the hiring company about the role above.
Explain how AtliQ can help fulfill the requirements.
Mention only the most relevant portfolio links from the provided list.
Do not add any preamble or explanation outside the email.
"""
        return self._complete(prompt_email)
