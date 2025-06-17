# (No code change, just move the file to the root directory.) 

import openai
import os
from dotenv import load_dotenv
import json
from pathlib import Path
from typing import List, Optional
from crewai.tools import BaseTool
import requests
import traceback

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class LinkedInSearchTool(BaseTool):
    name: str = "LinkedInSearchTool"
    description: str = "Tool for searching LinkedIn candidates"

    def _run(self, job_requirements: str) -> str:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            print("Tavily API key not set in environment variable TAVILY_API_KEY")
            return json.dumps([])
        query = f"site:linkedin.com/in {job_requirements}"
        try:
            response = requests.post(
                "https://api.tavily.com/search",
                headers={"Authorization": f"Bearer {tavily_api_key}"},
                json={"query": query, "search_depth": "advanced", "include_answer": False, "include_raw_content": False}
            )
            response.raise_for_status()
            data = response.json()
            # Extract LinkedIn profile URLs from results
            linkedin_profiles = [r["url"] for r in data.get("results", []) if "linkedin.com/in" in r.get("url", "")]
            if not linkedin_profiles:
                return json.dumps([])
            return json.dumps(linkedin_profiles)
        except Exception as e:
            print("Tavily API ERROR:", e)
            print(traceback.format_exc())
            return json.dumps({"error": str(e), "traceback": traceback.format_exc()})

class CandidateEvaluatorTool(BaseTool):
    name: str = "CandidateEvaluatorTool"
    description: str = "Tool for evaluating candidate fit for a job"

    def _run(self, candidate: str, job_requirements: str = "") -> str:
        try:
            prompt = f"""
            {job_requirements}\n\nCandidate Profile:\n{candidate}\n\n{self._get_srn_prompt()}
            """
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.2,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print("LLM ERROR:", e)
            print(traceback.format_exc())
            return f"LLM call failed: {e}\n{traceback.format_exc()}"

    def _get_srn_prompt(self) -> str:
        return """
        You are an elite candidate evaluator. Use the following job description and candidate profile to score the candidate using the SRN Smart Candidate Evaluation System.\n\n[Insert your full SRN Smart Candidate Evaluation System prompt here.]
        """

class PSE(BaseTool):
    name: str = "PSE"
    description: str = "A tool for evaluating candidate profiles"
    
    def __init__(self):
        super().__init__()
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="mixtral-8x7b-32768"
        )
    
    def _run(self, candidate_profile: str) -> str:
        evaluation_prompt = f"""
        Evaluate the following candidate profile:
        {candidate_profile}
        
        Provide a detailed evaluation including:
        1. Technical skills assessment
        2. Experience relevance
        3. Cultural fit
        4. Overall recommendation
        5. Final Fit Score (0-10)
        """
        evaluation = self.llm.invoke(evaluation_prompt)
        return evaluation 