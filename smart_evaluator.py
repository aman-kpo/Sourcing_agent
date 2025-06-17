import json
import re
from typing import Dict, List, Any
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SmartContextDetector:
    """Detects industry, company type, role type, and role subtype from job descriptions"""
    
    def __init__(self):
        self.industry_patterns = {
            "Tech": ["software", "ai", "ml", "saas", "startup", "tech", "developer", "engineer", "data", "cloud"],
            "Healthcare": ["hospital", "medical", "nurse", "doctor", "clinical", "patient", "healthcare", "pharma"],
            "Finance": ["finance", "investment", "banking", "trading", "fintech", "accounting", "cpa", "tax"],
            "Legal": ["law", "attorney", "lawyer", "legal", "litigation", "compliance", "paralegal"],
            "Retail": ["retail", "ecommerce", "consumer", "merchandising", "store", "sales"],
            "Education": ["education", "teacher", "professor", "university", "school", "academic"],
            "Government": ["government", "public sector", "federal", "state", "municipal", "agency"]
        }
        
        self.company_types = {
            "VC-backed Startup": ["startup", "series a", "series b", "series c", "vc", "venture", "funding", "round"],
            "Enterprise": ["enterprise", "fortune 500", "large company", "corporation", "multinational"],
            "Hospital Group": ["hospital", "health system", "medical center", "clinic"],
            "Public Sector": ["government", "public", "federal", "state", "city", "municipal"]
        }
        
        self.role_types = {
            "Software Engineer": ["software engineer", "developer", "programmer", "swe"],
            "DevOps Engineer": ["devops", "infrastructure", "site reliability", "platform engineer"],
            "Data Scientist": ["data scientist", "ml engineer", "ai engineer", "machine learning"],
            "Product Manager": ["product manager", "pm", "product owner"],
            "Designer": ["designer", "ux", "ui", "creative director"],
            "Sales": ["sales", "account manager", "business development", "revenue"],
            "Marketing": ["marketing", "growth", "content", "brand"],
            "Finance": ["finance", "accounting", "controller", "cfo", "analyst"],
            "Legal": ["lawyer", "attorney", "counsel", "legal"],
            "Operations": ["operations", "project manager", "program manager"]
        }

    def detect_context(self, job_description: str) -> Dict[str, str]:
        """Detect context parameters from job description"""
        text = job_description.lower()
        
        # Detect industry
        industry = self._detect_category(text, self.industry_patterns, "Tech")
        
        # Detect company type
        company_type = self._detect_category(text, self.company_types, "Enterprise")
        
        # Detect role type
        role_type = self._detect_category(text, self.role_types, "Software Engineer")
        
        # Detect role subtype (more specific)
        role_subtype = self._detect_role_subtype(text, role_type)
        
        return {
            "industry": industry,
            "company_type": company_type,
            "role_type": role_type,
            "role_subtype": role_subtype
        }
    
    def _detect_category(self, text: str, patterns: Dict[str, List[str]], default: str) -> str:
        """Detect category based on keyword patterns"""
        scores = {}
        for category, keywords in patterns.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[category] = score
        
        return max(scores.items(), key=lambda x: x[1])[0] if scores else default
    
    def _detect_role_subtype(self, text: str, role_type: str) -> str:
        """Detect specific role subtype"""
        subtypes = {
            "Software Engineer": {
                "Frontend": ["frontend", "react", "angular", "vue", "ui"],
                "Backend": ["backend", "api", "server", "database"],
                "Full-stack": ["full-stack", "fullstack"],
                "Mobile": ["mobile", "ios", "android", "react native"]
            },
            "DevOps Engineer": {
                "Cloud Infrastructure": ["cloud", "aws", "azure", "gcp"],
                "CI/CD": ["ci/cd", "jenkins", "pipeline"],
                "Security": ["security", "compliance", "devsecops"]
            },
            "Data Scientist": {
                "ML Engineer": ["ml engineer", "machine learning"],
                "Data Analyst": ["data analyst", "analytics"],
                "AI Researcher": ["ai research", "nlp", "computer vision"]
            }
        }
        
        if role_type in subtypes:
            for subtype, keywords in subtypes[role_type].items():
                if any(keyword in text for keyword in keywords):
                    return subtype
        
        return "General"

class SmartEvaluator:
    """Main class implementing SRN Smart Candidate Evaluation System"""
    
    def __init__(self):
        self.context_detector = SmartContextDetector()
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def evaluate_candidate_smart(self, candidate_profile: Dict, job_description: str) -> Dict[str, Any]:
        """Complete smart evaluation pipeline"""
        
        # Step 1: Detect context
        context = self.context_detector.detect_context(job_description)
        
        # Step 2: Generate hiring criteria
        criteria = self._generate_criteria(context, job_description)
        
        # Step 3: Evaluate candidate using SRN FitScore
        evaluation = self._evaluate_candidate(candidate_profile, criteria, context)
        
        return {
            "context": context,
            "hiring_criteria": criteria,
            "evaluation": evaluation,
            "fit_score": evaluation["final_score"],
            "recommendation": self._generate_recommendation(evaluation["final_score"])
        }
    
    def _generate_criteria(self, context: Dict[str, str], job_description: str) -> Dict[str, Any]:
        """Generate elite hiring criteria based on context"""
        
        prompt = f"""
        Generate elite hiring criteria for this role using SRN Smart Hiring standards:
        
        Industry: {context['industry']}
        Company Type: {context['company_type']}
        Role Type: {context['role_type']}
        Role Subtype: {context['role_subtype']}
        
        Job Description:
        {job_description}
        
        Create criteria for top 1-2% performers who can thrive in elite environments like:
        - Tech: Stripe, Anthropic, OpenAI, Databricks, Google, Apple
        - Finance: Goldman Sachs, Blackstone, Jane Street, McKinsey
        - Healthcare: Mayo Clinic, Johns Hopkins, Cleveland Clinic
        
        Return a JSON object with:
        {{
            "education_requirements": "Elite university requirements or equivalent excellence",
            "core_skills": ["4-6 mission-critical skills - what they must DO, not just know"],
            "domain_expertise": ["4-6 technical/domain specific capabilities"],
            "experience_markers": ["3-4 indicators of high performance and ownership"],
            "company_preferences": ["Preferred company types, stages, or caliber"],
            "red_flags": ["3-4 disqualifying factors or concerning patterns"],
            "bonus_signals": ["3-4 exceptional indicators like OSS, publications, awards"]
        }}
        
        Be demanding - these are elite hiring standards for top 1-2% performers.
        """
        
        try:
            response = self._call_openai(prompt)
            criteria = json.loads(response)
        except Exception:
            # Fallback criteria
            criteria = self._get_fallback_criteria(context['role_type'])
        
        return criteria
    
    def _evaluate_candidate(self, candidate_profile: Dict, criteria: Dict, context: Dict) -> Dict[str, Any]:
        """Evaluate candidate using SRN FitScore methodology"""
        
        candidate_text = f"{candidate_profile.get('title', '')} {candidate_profile.get('snippet', '')}"
        
        evaluation_prompt = f"""
        Evaluate this candidate using the SRN FitScore methodology on a 0-10 scale.
        
        CONTEXT:
        Industry: {context['industry']}
        Company Type: {context['company_type']}
        Role: {context['role_type']} - {context['role_subtype']}
        
        ELITE HIRING CRITERIA:
        Education: {criteria.get('education_requirements', '')}
        Core Skills: {criteria.get('core_skills', [])}
        Domain Expertise: {criteria.get('domain_expertise', [])}
        Experience Markers: {criteria.get('experience_markers', [])}
        Company Preferences: {criteria.get('company_preferences', [])}
        Red Flags: {criteria.get('red_flags', [])}
        Bonus Signals: {criteria.get('bonus_signals', [])}
        
        CANDIDATE PROFILE:
        {candidate_text}
        
        Score each category (be conservative - 8+ only for exceptional candidates):
        
        1. 🎓 Education (0-10): Elite institutions, degrees, certifications
        2. 📈 Career Trajectory (0-10): Growth, ownership, increasing responsibility  
        3. 🏢 Company Relevance (0-10): High-caliber organizations, industry fit
        4. ⏳ Tenure & Stability (0-10): 1.5-3 year averages, justified moves
        5. 🎯 Core Skills (0-10): Mastery of mission-critical capabilities
        6. 🌟 Bonus Signals (0-5): Exceptional achievements, publications, OSS
        7. ❌ Red Flags (-5 to 0): Dealbreakers, concerning patterns
        
        Calculate final weighted score:
        - Education: 20%
        - Career Trajectory: 20% 
        - Company Relevance: 15%
        - Tenure & Stability: 15%
        - Core Skills: 20%
        - Bonus Signals: 5%
        - Red Flags: -15%
        
        Return JSON:
        {{
            "scores": {{
                "education": 0-10,
                "career_trajectory": 0-10,
                "company_relevance": 0-10,
                "tenure_stability": 0-10,
                "core_skills": 0-10,
                "bonus_signals": 0-5,
                "red_flags": -5 to 0
            }},
            "final_score": "calculated weighted score 0-10",
            "strengths": ["2-3 key strengths"],
            "weaknesses": ["2-3 key concerns or gaps"],
            "rationale": "2-3 sentence assessment of overall fit",
            "override_signal": "true if extraordinary signal despite lower score"
        }}
        
        Be conservative in scoring - these are elite standards.
        """
        
        try:
            response = self._call_openai(evaluation_prompt)
            evaluation = json.loads(response)
        except Exception:
            # Fallback evaluation
            evaluation = self._fallback_evaluation(candidate_text)
        
        return evaluation
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    def _get_fallback_criteria(self, role_type: str) -> Dict[str, Any]:
        """Fallback criteria when API fails"""
        return {
            "education_requirements": "Bachelor's+ from top-tier university or equivalent excellence",
            "core_skills": ["System design", "Production ownership", "Technical leadership", "Problem solving"],
            "domain_expertise": ["Cloud platforms", "Scalability", "Best practices", "Modern tools"],
            "experience_markers": ["Ownership of outcomes", "Scale challenges", "Technical impact"],
            "company_preferences": ["High-growth companies", "Technical excellence culture"],
            "red_flags": ["Job hopping", "No ownership", "Buzzword resumes"],
            "bonus_signals": ["Open source", "Technical writing", "Speaking", "Awards"]
        }
    
    def _fallback_evaluation(self, candidate_text: str) -> Dict[str, Any]:
        """Fallback evaluation when API fails"""
        return {
            "scores": {
                "education": 6.0,
                "career_trajectory": 6.0,
                "company_relevance": 6.0,
                "tenure_stability": 6.0,
                "core_skills": 6.0,
                "bonus_signals": 2.0,
                "red_flags": 0.0
            },
            "final_score": 6.0,
            "strengths": ["Professional experience visible"],
            "weaknesses": ["Limited profile information"],
            "rationale": "Assessment based on limited LinkedIn data. Full evaluation requires detailed resume.",
            "override_signal": False
        }
    
    def _generate_recommendation(self, score: float) -> str:
        """Generate hiring recommendation based on SRN FitScore"""
        if score >= 8.5:
            return "🟢 STRONG HIRE - Exceptional candidate meeting elite standards"
        elif score >= 7.0:
            return "🟡 CONSIDER - Good candidate, requires additional evaluation"
        elif score >= 5.5:
            return "🟠 WEAK - Below standards, significant concerns"
        else:
            return "🔴 NO HIRE - Does not meet minimum requirements"

if __name__ == "__main__":
    # Test the smart evaluator
    evaluator = SmartEvaluator()
    
    job_description = """
    Senior DevOps Engineer San Francisco, California Engineering / On-site 
    Ivo AI is building tools to help every company in the world make sense of their contracts. 
    We're looking for a seasoned DevOps engineer to own and shape the future of our environment.
    
    Responsibilities:
    * Manage dozens, hundreds, thousands of customer deployments
    * Instrument our system for performance monitoring
    * Get our CI/CD system running super quickly
    * Experience with Pulumi, Azure, GCP, Kubernetes, JavaScript
    * 5+ years experience with Infrastructure as Code
    """
    
    candidate_profile = {
        "title": "Senior DevOps Engineer at Google Cloud",
        "snippet": "Stanford Computer Science graduate with 7 years experience in cloud infrastructure, Kubernetes orchestration, and CI/CD pipeline optimization. Led infrastructure for high-scale distributed systems."
    }
    
    result = evaluator.evaluate_candidate_smart(candidate_profile, job_description)
    
    print("🧠 SRN Smart Evaluation Result:")
    print(f"📊 Context: {result['context']}")
    print(f"🎯 Fit Score: {result['fit_score']}/10.0")
    print(f"💡 Recommendation: {result['recommendation']}")
    print(f"✅ Strengths: {result['evaluation']['strengths']}")
    print(f"⚠️  Weaknesses: {result['evaluation']['weaknesses']}")
