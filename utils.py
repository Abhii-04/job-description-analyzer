"""
JD Analyzer — Groq-powered job description analysis
Model: llama-3.3-70b-versatile
"""
import json
import os
from dotenv import load_dotenv
from groq import Groq

def get_client() -> Groq | None:
    """Always reload .env so key changes are picked up without restart."""
    load_dotenv(override=True)
    api_key = os.getenv('GROQ_API_KEY', '').strip()
    if not api_key:
        return None
    return Groq(api_key=api_key)


# Primary model — best quality on Groq
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are a world-class HR consultant and technical recruiter. "
    "You always respond with valid JSON only — no markdown, no code blocks, no extra text."
)

ANALYSIS_PROMPT = """Analyze the following job description comprehensively and return a structured quality assessment in JSON.

Job Description:
---
{job_description}
---

Score each of the 5 dimensions from 0–100 and assign a letter grade (A=90+, B=75+, C=60+, D=40+, F=below 40).
Calculate overall_score as a weighted average: clarity 25%, inclusivity 20%, structure 20%, tone 15%, requirements 20%.
Verdict must match: Excellent (85+), Good (70+), Fair (55+), Needs Work (40+), Poor (below 40).

Return ONLY this JSON structure:
{
  "overall_score": <integer 0-100>,
  "verdict": "<Excellent|Good|Fair|Needs Work|Poor>",
  "executive_summary": "<2-3 sentences summarizing overall quality and key observations>",
  "categories": {
    "clarity": {
      "score": <integer 0-100>,
      "grade": "<A|B|C|D|F>",
      "summary": "<1-2 sentence assessment of writing clarity and precision>",
      "details": ["<observation>", "<observation>", "<observation>"]
    },
    "inclusivity": {
      "score": <integer 0-100>,
      "grade": "<A|B|C|D|F>",
      "summary": "<1-2 sentence assessment of inclusive and unbiased language>",
      "biased_terms": ["<term found in the JD>"],
      "details": ["<observation>", "<observation>"]
    },
    "structure": {
      "score": <integer 0-100>,
      "grade": "<A|B|C|D|F>",
      "summary": "<1-2 sentence assessment of organization, flow and completeness>",
      "details": ["<observation>", "<observation>"]
    },
    "tone": {
      "score": <integer 0-100>,
      "grade": "<A|B|C|D|F>",
      "summary": "<1-2 sentence assessment of professional tone and candidate appeal>",
      "details": ["<observation>", "<observation>"]
    },
    "requirements": {
      "score": <integer 0-100>,
      "grade": "<A|B|C|D|F>",
      "summary": "<1-2 sentence assessment of requirements clarity and reasonableness>",
      "details": ["<observation>", "<observation>"]
    }
  },
  "strengths": ["<strength>", "<strength>", "<strength>"],
  "issues": [
    {"severity": "<High|Medium|Low>", "category": "<category name>", "description": "<specific issue>"}
  ],
  "suggestions": [
    {"priority": "<High|Medium|Low>", "title": "<short actionable title>", "description": "<detailed, specific improvement suggestion with example if possible>"}
  ],
  "extracted_info": {
    "job_title": "<inferred job title or Not Specified>",
    "seniority": "<Junior|Mid-level|Senior|Lead|Executive|Not Specified>",
    "tech_skills": ["<skill>"],
    "soft_skills": ["<skill>"],
    "key_responsibilities": ["<concise responsibility>"]
  }
}"""


def analyze_jd(job_description: str) -> dict:
    """
    Analyze a job description using Groq (llama-3.3-70b-versatile).
    Returns a structured dict with comprehensive scores and insights.
    """
    client = get_client()
    if not client:
        return {'error': 'GROQ_API_KEY is missing. Add it to your .env file: GROQ_API_KEY=gsk_... (get a free key at console.groq.com)'}

    prompt = ANALYSIS_PROMPT.replace("{job_description}", job_description)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=4096
        )
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        msg = str(e)
        if '401' in msg or 'invalid_api_key' in msg.lower() or 'authentication' in msg.lower():
            return {'error': 'Invalid Groq API key. Please check your GROQ_API_KEY in the .env file.'}
        if '429' in msg or 'rate_limit' in msg.lower():
            return {'error': 'Groq rate limit hit. Please wait a moment and try again.'}
        if '503' in msg or '502' in msg:
            return {'error': 'Groq service temporarily unavailable. Please try again in a few seconds.'}
        return {'error': f'Analysis failed: {msg[:200]}'}
