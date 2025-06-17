# (No code change, just move the file to the root directory.) 

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def evaluate_candidate_gpt(candidate, job):
    """
    Evaluate a candidate's fit for a job using OpenAI GPT.
    """
    try:
        system_prompt = "You are an elite candidate evaluator. Use the following job description and candidate profile to score the candidate using the SRN Smart Candidate Evaluation System."
        user_prompt = f"""
        Evaluate the following candidate for the role:

        Candidate Profile:
        {candidate}

        Job Requirements:
        {job}

        Provide a detailed evaluation including:
        1. Skills match analysis
        2. Experience assessment
        3. Location compatibility
        4. Overall fit score (0-10)

        Format the response with clear sections and a final fit score.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=600,
            temperature=0.2,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("OpenAI LLM ERROR (evaluate_candidate_gpt):", e)
        return f"LLM call failed: {e}"

def generate_outreach_message_gpt(candidate, job):
    """
    Generate a personalized outreach message for a candidate using OpenAI GPT.
    """
    try:
        system_prompt = "You are an assistant that drafts personalized LinkedIn connection messages from a recruiter to a candidate. The message should be brief, polite, and reference the candidate's background and the job opportunity."
        user_prompt = f"""
        Write a personalized outreach message for the following candidate:

        Candidate Profile:
        {candidate}

        Job Details:
        {job}

        The message should:
        1. Be personalized based on their experience and skills
        2. Highlight relevant aspects of the role
        3. Be professional but conversational
        4. Include a clear call to action

        Keep the message concise and engaging.
        """
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
    except Exception as e:
        print("OpenAI LLM ERROR (generate_outreach_message_gpt):", e)
        return f"LLM call failed: {e}" 