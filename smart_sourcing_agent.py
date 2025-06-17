from typing import List, Dict, Any, Optional
import json
from dataclasses import dataclass
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import time
import re

load_dotenv()

@dataclass
class AgentMemory:
    """Memory storage for the agent's learning and optimization"""
    successful_searches: List[Dict[str, Any]] = None
    candidate_evaluations: List[Dict[str, Any]] = None
    search_patterns: List[Dict[str, Any]] = None
    performance_metrics: Dict[str, float] = None
    
    def __post_init__(self):
        if self.successful_searches is None:
            self.successful_searches = []
        if self.candidate_evaluations is None:
            self.candidate_evaluations = []
        if self.search_patterns is None:
            self.search_patterns = []
        if self.performance_metrics is None:
            self.performance_metrics = {
                "search_success_rate": 0.0,
                "candidate_match_rate": 0.0,
                "average_response_time": 0.0
            }

class SmartSourcingAgent:
    def __init__(self):
        """Initialize the smart sourcing agent with memory and tools"""
        self.memory = AgentMemory()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    def call_openai(self, prompt: str) -> str:
        """Make a direct call to OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return ""

    def extract_job_context(self, job_description: str) -> Dict:
        """Extract structured hiring criteria from job description using LLM"""
        prompt = (
            "You are an expert recruiter. Analyze the following job description and extract the following as JSON: "
            "industry, company_type, role_type, role_subtype, critical_skills, education_requirements, "
            "experience_requirements, company_preferences, location_preferences, bonus_signals, red_flags.\n"
            f"Job Description:\n{job_description}"
        )
        
        response = self.call_openai(prompt)
        try:
            criteria = json.loads(response)
        except Exception:
            # fallback: try to extract JSON from the response
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                try:
                    criteria = json.loads(match.group(0))
                except:
                    criteria = {"error": "Could not parse response"}
            else:
                criteria = {"error": "No JSON found in response"}
        
        self.memory.successful_searches.append({
            "timestamp": datetime.now(),
            "criteria": criteria
        })
        return criteria

    def generate_xray_query(self, criteria: Dict) -> str:
        """Generate a LinkedIn X-Ray search query based on job criteria"""
        prompt = f"""Generate a LinkedIn X-Ray search query based on the following job criteria:
        {json.dumps(criteria, indent=2)}
        
        Create a Google X-Ray search query that will find relevant LinkedIn profiles.
        Use Boolean operators and specific filters to target the right candidates.
        Return only the search query string."""
        
        response = self.call_openai(prompt)
        return response.strip()

    def evaluate_candidate(self, profile: Dict, criteria: Dict) -> Dict:
        """Evaluate a candidate's profile against job criteria"""
        prompt = f"""Evaluate the candidate's profile against the job requirements:
        Candidate Profile: {json.dumps(profile, indent=2)}
        Job Context: {json.dumps(criteria, indent=2)}
        
        Score the candidate on:
        1. skills_match (0-100)
        2. experience_level (0-100)
        3. industry_fit (0-100)
        4. education_match (0-100)
        5. overall_fit (0-100)
        
        Return ONLY a JSON object with these exact keys and numeric values."""
        
        response = self.call_openai(prompt)
        
        try:
            score = json.loads(response)
        except Exception:
            # fallback: try to extract JSON from the response
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                try:
                    score = json.loads(match.group(0))
                except:
                    score = {
                        "skills_match": 50,
                        "experience_level": 50,
                        "industry_fit": 50,
                        "education_match": 50,
                        "overall_fit": 50
                    }
            else:
                score = {
                    "skills_match": 50,
                    "experience_level": 50,
                    "industry_fit": 50,
                    "education_match": 50,
                    "overall_fit": 50
                }
        
        self.memory.candidate_evaluations.append({
            "timestamp": datetime.now(),
            "profile": profile,
            "score": score
        })
        return score

    def search_linkedin_profiles(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search for LinkedIn profiles using Google Custom Search API"""
        profiles = []
        params = {
            "key": self.google_api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": min(num_results, 10)
        }
        
        print(f"🔍 Searching with query: {query}")
        print(f"📊 Requesting {min(num_results, 10)} results")
        
        try:
            response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
            print(f"📡 API Response Status: {response.status_code}")
            response.raise_for_status()
            results = response.json()
            
            total_results = results.get('searchInformation', {}).get('totalResults', 0)
            items = results.get("items", [])
            print(f"📈 Total results available: {total_results}")
            print(f"📦 Items returned by API: {len(items)}")
            
            for i, item in enumerate(items):
                link = item.get("link", "")
                title = item.get("title", "")
                print(f"  {i+1}. Checking: {title}")
                print(f"     URL: {link}")
                print(f"     Has linkedin.com/in/: {'linkedin.com/in/' in link}")
                
                if "linkedin.com/in/" in link:
                    profiles.append({
                        "url": link,
                        "title": title,
                        "snippet": item.get("snippet", "")
                    })
                    print(f"     ✅ Added to results")
                else:
                    print(f"     ❌ Filtered out")
            
            print(f"🎯 Final filtered profiles: {len(profiles)}")
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            print(f"🔧 Using mock data fallback")
            # Return mock data for testing
            profiles = [
                {
                    "url": "https://www.linkedin.com/in/test-frontend-engineer-1",
                    "title": "John Doe - Senior Frontend Engineer - Tech Startup",
                    "snippet": "Senior Frontend Engineer with 6+ years experience in React, TypeScript, and modern frontend architecture. Previously worked at AI startup building scalable web applications."
                },
                {
                    "url": "https://www.linkedin.com/in/test-frontend-engineer-2", 
                    "title": "Jane Smith - Lead Frontend Developer - YC Startup",
                    "snippet": "Lead Frontend Developer specializing in React, Redux, and TypeScript. 5+ years experience with CI/CD pipelines and testing frameworks. Computer Science degree from Stanford."
                },
                {
                    "url": "https://www.linkedin.com/in/test-frontend-engineer-3",
                    "title": "Mike Johnson - Senior React Developer - San Francisco",
                    "snippet": "Frontend engineer focused on React, Next.js, and WebGL. Experience with state management and modern testing. Open source contributor with projects on GitHub."
                }
            ]
        return profiles[:num_results]

    def find_top_candidates(self, job_description: str, num_candidates: int = 5) -> List[Dict]:
        """Find and evaluate top candidates for a job description"""
        start_time = time.time()
        
        print(f"Starting candidate search for {num_candidates} candidates...")
        
        # Extract job context
        print("Extracting job context...")
        criteria = self.extract_job_context(job_description)
        print(f"Job context extracted: {len(criteria)} criteria found")
        
        # Generate and execute search
        print("Generating search query...")
        query = self.generate_xray_query(criteria)
        print(f"Generated query: {query[:100]}...")
        
        print("Searching LinkedIn profiles...")
        profiles = self.search_linkedin_profiles(query, num_results=num_candidates)
        print(f"Found {len(profiles)} profiles")
        
        # Evaluate and rank candidates
        evaluated_profiles = []
        print("Evaluating candidates...")
        for i, profile in enumerate(profiles):
            print(f"Evaluating candidate {i+1}/{len(profiles)}")
            score = self.evaluate_candidate(profile, criteria)
            evaluated_profiles.append({
                "profile": profile,
                "score": score
            })
        
        print(f"Evaluated {len(evaluated_profiles)} candidates")
        
        # Sort by overall fit score
        evaluated_profiles.sort(key=lambda x: x["score"].get("overall_fit", 0), reverse=True)
        
        end_time = time.time()
        print(f"Search completed in {end_time - start_time:.2f} seconds")
        print(f"Returning {len(evaluated_profiles[:num_candidates])} candidates")
        
        return evaluated_profiles[:num_candidates]

if __name__ == "__main__":
    agent = SmartSourcingAgent()
    job_description = """
    Senior Frontend Engineer
    We're looking for a Senior Frontend Engineer to join our team at a fast-growing AI startup. 
    You'll be responsible for building and maintaining our core product's user interface.
    Requirements:
    - 5+ years of experience with React and TypeScript
    - Strong understanding of modern frontend architecture
    - Experience with state management (Redux, MobX, etc.)
    - Knowledge of testing frameworks (Jest, React Testing Library)
    - Experience with CI/CD pipelines
    - Bachelor's degree in Computer Science or related field
    Nice to have:
    - Experience with Next.js
    - Contributions to open source projects
    - Experience with WebGL or Three.js
    - Experience at a YC-backed startup
    Location: San Francisco (hybrid)
    """
    top_candidates = agent.find_top_candidates(job_description)
    for candidate in top_candidates:
        print(f"\nScore: {candidate['score'].get('overall_fit', 0)}")
        print(f"Profile: {candidate['profile']}") 