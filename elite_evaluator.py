import os
import openai
import requests
from typing import Dict, Any

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SMARTLEAD_API_KEY = os.getenv("SMARTLEAD_API_KEY", "")

openai.api_key = OPENAI_API_KEY

def build_elite_eval_prompt(candidate: Dict[str, Any], job: Dict[str, Any]) -> str:
    # Build the evaluation prompt using the provided rubric
    return f"""
You are an elite candidate evaluator. Use the following job description and candidate profile to score the candidate using the SRN Smart Candidate Evaluation System.

Job Description:
{job['description']}

Candidate Profile:
{candidate}

Step 1: Extract context (Industry, Company Type, Role Type, Role Subtype).
Step 2: Generate elite hiring criteria for this context.
Step 3: Score the candidate using the following rubric (100 → 10.0 scale):
- Education (20%)
- Career Trajectory (20%)
- Company Relevance (15%)
- Tenure & Stability (15%)
- Most Important Skills (20%)
- Bonus Signals (5%)
- Red Flags (−15%)

Output format:
Final Fit Score: X.X / 10.0
Breakdown:
* Education: x/10
* Career trajectory: x/10
* Company relevance: x/10
* Tenure & stability: x/10
* Most important skills: x/10
* Bonus signals: x/5
* Red flags: −x
Summary (3–5 lines):
Strengths: ...
Weaknesses: ...
Rationale: ...
Override Signal: [yes/no, with reason if yes]
"""

def evaluate_candidate_gpt(candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    prompt = build_elite_eval_prompt(candidate, job)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.2,
    )
    return response['choices'][0]['message']['content']

def build_outreach_prompt(candidate: Dict[str, Any], job: Dict[str, Any]) -> str:
    return f"""
Draft a personalized LinkedIn connection message for the following scenario:
- Job Title: {job['role']} at {job['organization']} ({job['description']})
- Candidate: {candidate['name']}, {candidate.get('current_role', 'Professional')} ({candidate.get('experience', '')})
- Commonalities: {job.get('commonalities', '')}
The message should mention one of their skills and invite them to chat about the role. Be brief, polite, and reference the candidate's background and the job opportunity.
"""

def generate_outreach_message_gpt(candidate: Dict[str, Any], job: Dict[str, Any]) -> str:
    system_prompt = "You are an assistant that drafts personalized LinkedIn connection messages from a recruiter to a candidate. The message should be brief, polite, and reference the candidate's background and the job opportunity."
    user_prompt = build_outreach_prompt(candidate, job)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content']

def send_smartlead_email(candidate: Dict[str, Any], message: str, job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder for Smartlead API integration. Sends an email via Smartlead.
    """
    if not SMARTLEAD_API_KEY:
        return {"status": "error", "message": "SMARTLEAD_API_KEY not set"}
    # Example API call (replace with actual Smartlead API endpoint and payload)
    url = "https://api.smartlead.ai/v1/send"
    payload = {
        "to": candidate["email"],
        "subject": f"Opportunity: {job['role']} at {job['organization']}",
        "body": message,
        "from": os.getenv("EMAIL_ID", "")
    }
    headers = {"Authorization": f"Bearer {SMARTLEAD_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json() 