from typing import List, Dict, Any, Optional
import json
import re
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import time
import streamlit as st
# Import the SmartEvaluator
from smart_evaluator import SmartEvaluator

load_dotenv()

class JobDescriptionAnalyzer:
    """Enhanced analyzer for job descriptions with industry classification and skill extraction"""
    
    def __init__(self):
        self.job_families = {
            "engineering": ["engineer", "developer", "programmer", "swe", "devops", "infrastructure", "backend", "frontend", "fullstack", "mobile", "platform", "site reliability", "sre"],
            "data": ["data scientist", "ml engineer", "ai engineer", "data engineer", "analyst", "machine learning", "artificial intelligence", "data analyst"],
            "product": ["product manager", "pm", "product owner", "product lead", "chief product officer", "cpo"],
            "design": ["designer", "ux", "ui", "creative", "design lead", "art director", "visual designer"],
            "sales": ["sales", "account executive", "account manager", "sales rep", "business development", "bdr", "sdr"],
            "marketing": ["marketing", "growth", "content", "brand", "digital marketing", "social media", "seo", "sem"],
            "finance": ["finance", "accounting", "controller", "cfo", "analyst", "fp&a", "tax", "audit", "cpa"],
            "legal": ["lawyer", "attorney", "counsel", "legal", "paralegal", "compliance"],
            "operations": ["operations", "project manager", "program manager", "business analyst", "consultant"],
            "hr": ["hr", "human resources", "recruiter", "talent", "people operations", "chief people officer"],
            "executive": ["ceo", "cfo", "cto", "coo", "chief", "vp", "vice president", "director", "head of"]
        }
        
        self.seniority_levels = {
            "entry": ["junior", "entry", "associate", "intern", "new grad", "recent graduate", "1-2 years"],
            "mid": ["mid", "2-5 years", "3-6 years", "intermediate"],
            "senior": ["senior", "sr", "5+ years", "6+ years", "lead", "principal", "staff"],
            "executive": ["director", "vp", "vice president", "chief", "ceo", "cfo", "cto", "coo", "head of"]
        }
        
        self.industries = {
            "tech": ["tech", "software", "saas", "platform", "ai", "ml", "startup", "fintech", "edtech", "healthtech"],
            "finance": ["finance", "banking", "investment", "trading", "insurance", "fintech", "hedge fund", "private equity"],
            "healthcare": ["healthcare", "medical", "hospital", "pharma", "biotech", "health tech", "clinical"],
            "consulting": ["consulting", "mckinsey", "bain", "bcg", "deloitte", "pwc", "accenture"],
            "retail": ["retail", "ecommerce", "consumer", "fashion", "cpg", "fmcg"]
        }
        
        # Enhanced technical skills patterns
        self.technical_skills = {
            # Programming Languages
            "programming": r"\b(python|javascript|java|c\+\+|golang|rust|typescript|ruby|php|scala|kotlin|swift|objective-c|c#|r|matlab)\b",
            
            # Cloud & Infrastructure
            "cloud": r"\b(aws|azure|gcp|google cloud|amazon web services|docker|kubernetes|terraform|pulumi|cloudformation|helm|istio)\b",
            
            # Databases
            "databases": r"\b(postgresql|mysql|mongodb|redis|elasticsearch|dynamodb|cassandra|snowflake|bigquery|databricks)\b",
            
            # DevOps & Tools
            "devops": r"\b(jenkins|gitlab ci|github actions|ansible|chef|puppet|docker|kubernetes|prometheus|grafana|datadog|splunk)\b",
            
            # Frontend
            "frontend": r"\b(react|angular|vue|svelte|next\.js|nuxt|webpack|vite|sass|less|tailwind|bootstrap)\b",
            
            # Backend
            "backend": r"\b(node\.js|express|django|flask|spring|rails|laravel|fastapi|graphql|rest api|microservices)\b",
            
            # ML/AI
            "ml_ai": r"\b(tensorflow|pytorch|scikit-learn|pandas|numpy|jupyter|mlflow|kubeflow|langchain|openai|hugging face|transformers)\b",
            
            # Finance/Accounting
            "finance": r"\b(gaap|ifrs|sox|cpa|cfa|frm|quickbooks|sap|oracle financials|hyperion|cognos|tableau|power bi)\b",
            
            # Legal
            "legal": r"\b(westlaw|lexisnexis|clio|contracts|litigation|ip|patent|trademark|compliance|gdpr|ccpa)\b"
        }

    def analyze_job(self, job_description: str) -> Dict[str, Any]:
        """Comprehensive job analysis"""
        text = job_description.lower()
        
        # Analyze job family
        job_family = self._classify_job_family(text)
        
        # Analyze seniority
        seniority = self._detect_seniority(text)
        
        # Analyze industry
        industry = self._detect_industry(text)
        
        # Extract skills
        skills = self._extract_skills(text)
        
        # Extract locations
        locations = self._extract_locations(job_description)
        
        # Determine if role is technical/leadership/remote-eligible
        is_technical = job_family in ["engineering", "data"] or any(skills.values())
        is_leadership = seniority in ["senior", "executive"] or any(term in text for term in ["lead", "manager", "director", "head"])
        remote_eligible = any(term in text for term in ["remote", "distributed", "work from home", "wfh"])
        
        return {
            "job_family": job_family,
            "seniority": seniority,
            "industry": industry,
            "skills": skills,
            "locations": locations,
            "is_technical": is_technical,
            "is_leadership": is_leadership,
            "remote_eligible": remote_eligible,
            "total_skills": sum(len(v) for v in skills.values())
        }
    
    def _classify_job_family(self, text: str) -> str:
        """Classify job into family category"""
        family_scores = {}
        for family, keywords in self.job_families.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                family_scores[family] = score
        
        return max(family_scores.items(), key=lambda x: x[1])[0] if family_scores else "operations"
    
    def _detect_seniority(self, text: str) -> str:
        """Detect seniority level"""
        for level, keywords in self.seniority_levels.items():
            if any(keyword in text for keyword in keywords):
                return level
        return "mid"  # Default
    
    def _detect_industry(self, text: str) -> str:
        """Detect industry"""
        for industry, keywords in self.industries.items():
            if any(keyword in text for keyword in keywords):
                return industry
        return "tech"  # Default
    
    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract technical skills by category"""
        skills = {}
        for category, pattern in self.technical_skills.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills[category] = list(set(matches)) if matches else []
        return skills
    
    def _extract_locations(self, text: str) -> List[str]:
        """Extract location information"""
        # Common location patterns
        location_patterns = [
            r"\b([A-Z][a-z]+ [A-Z][a-z]+, [A-Z]{2})\b",  # City, State
            r"\b([A-Z][a-z]+, [A-Z]{2})\b",  # City, State  
            r"\b(New York|San Francisco|Los Angeles|Chicago|Boston|Seattle|Austin|Denver|Atlanta|Miami|remote)\b"
        ]
        
        locations = []
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            locations.extend(matches)
        
        return list(set(locations))

class QueryGenerator:
    """Generates optimized LinkedIn X-Ray search queries based on job analysis"""
    
    def __init__(self):
        # Role-specific query templates
        self.query_templates = {
            "devops_engineer": {
                "primary": 'site:linkedin.com/in/ ("DevOps Engineer" OR "Site Reliability Engineer" OR "Infrastructure Engineer") {location} {experience} {tech_stack}',
                "specialized": 'site:linkedin.com/in/ "DevOps Engineer" {company_context} ({cloud_platforms}) {iac_tools}',
                "industry_specific": 'site:linkedin.com/in/ ("DevOps Engineer" OR "Infrastructure Engineer") {industry_context} {certification}'
            },
            "ml_engineer": {
                "primary": 'site:linkedin.com/in/ ("ML Engineer" OR "Machine Learning Engineer" OR "AI Engineer") {location} {experience} {ml_frameworks}',
                "specialized": 'site:linkedin.com/in/ "ML Engineer" {company_context} ({production_ml}) {ai_domains}',
                "research_focused": 'site:linkedin.com/in/ ("ML Engineer" OR "Research Engineer") {research_context} {academic_background}'
            },
            "software_engineer": {
                "primary": 'site:linkedin.com/in/ ("Software Engineer" OR "Software Developer") {location} {experience} {programming_languages}',
                "specialized": 'site:linkedin.com/in/ "Software Engineer" {company_context} {tech_stack} {specialization}',
                "fullstack": 'site:linkedin.com/in/ ("Full Stack Engineer" OR "Full Stack Developer") {frontend_backend} {modern_stack}'
            },
            "tax_director": {
                "primary": 'site:linkedin.com/in/ ("Tax Director" OR "Tax Manager" OR "Senior Tax Manager") {location} {experience} {tax_credentials}',
                "specialized": 'site:linkedin.com/in/ "Tax Director" {company_size} {tax_specialization} {cpa_requirement}',
                "industry_specific": 'site:linkedin.com/in/ ("Tax Director" OR "Tax Manager") {industry_focus} {compliance_experience}'
            }
        }
        
        # Keyword mappings for different domains
        self.keyword_mappings = {
            "cloud_platforms": {
                "aws": ["AWS", "Amazon Web Services", "EC2", "S3", "Lambda"],
                "azure": ["Azure", "Microsoft Azure", "AKS", "ARM"],
                "gcp": ["GCP", "Google Cloud", "BigQuery", "GKE"]
            },
            "iac_tools": {
                "terraform": ["Terraform", "HCL"],
                "pulumi": ["Pulumi"],
                "cloudformation": ["CloudFormation", "AWS CloudFormation"]
            },
            "ml_frameworks": {
                "tensorflow": ["TensorFlow", "tf"],
                "pytorch": ["PyTorch", "torch"],
                "scikit": ["scikit-learn", "sklearn"]
            },
            "programming_languages": {
                "python": ["Python"],
                "javascript": ["JavaScript", "JS", "Node.js"],
                "java": ["Java"],
                "golang": ["Go", "Golang"]
            },
            "tax_credentials": {
                "cpa": ["CPA", "Certified Public Accountant"],
                "tax_llm": ["Tax LLM", "Master of Laws"],
                "ea": ["EA", "Enrolled Agent"]
            }
        }
    
    def generate_queries(self, job_analysis: Dict[str, Any], job_description: str, max_queries: int = 3) -> List[Dict[str, Any]]:
        """Generate multiple optimized search queries based on job analysis"""
        
        # Determine query strategy based on job family
        role_key = self._map_to_role_key(job_analysis["job_family"], job_description)
        
        # Get templates for this role
        templates = self.query_templates.get(role_key, self.query_templates["software_engineer"])
        
        queries = []
        
        # Generate primary query
        primary_query = self._build_query(
            templates["primary"], 
            job_analysis, 
            job_description,
            strategy="primary"
        )
        queries.append({
            "query": primary_query,
            "strategy": "primary",
            "description": "Broad role-based search with core requirements"
        })
        
        # Generate specialized query
        if "specialized" in templates:
            specialized_query = self._build_query(
                templates["specialized"], 
                job_analysis, 
                job_description,
                strategy="specialized"
            )
            queries.append({
                "query": specialized_query,
                "strategy": "specialized", 
                "description": "Targeted search with specific tech stack and company context"
            })
        
        # Generate industry-specific or alternative query
        third_template_key = list(templates.keys())[2] if len(templates) > 2 else "specialized"
        if third_template_key in templates:
            industry_query = self._build_query(
                templates[third_template_key], 
                job_analysis, 
                job_description,
                strategy="industry_specific"
            )
            queries.append({
                "query": industry_query,
                "strategy": third_template_key,
                "description": "Industry or domain-specific search"
            })
        
        return queries[:max_queries]
    
    def _map_to_role_key(self, job_family: str, job_description: str) -> str:
        """Map job family to specific role template key"""
        text = job_description.lower()
        
        if job_family == "engineering":
            if any(term in text for term in ["devops", "infrastructure", "site reliability", "platform"]):
                return "devops_engineer"
            else:
                return "software_engineer"
        elif job_family == "data":
            if any(term in text for term in ["ml engineer", "machine learning", "ai engineer"]):
                return "ml_engineer"
            else:
                return "software_engineer"
        elif job_family == "finance":
            if any(term in text for term in ["tax director", "tax manager", "tax"]):
                return "tax_director"
            else:
                return "software_engineer"
        else:
            return "software_engineer"
    
    def _build_query(self, template: str, job_analysis: Dict[str, Any], job_description: str, strategy: str) -> str:
        """Build a specific query from template and job analysis"""
        
        # Extract placeholders from template
        placeholders = re.findall(r'\{([^}]+)\}', template)
        
        # Generate replacement values
        replacements = {}
        for placeholder in placeholders:
            replacements[placeholder] = self._generate_placeholder_value(
                placeholder, job_analysis, job_description, strategy
            )
        
        # Replace placeholders
        query = template
        for placeholder, value in replacements.items():
            query = query.replace(f"{{{placeholder}}}", value)
        
        # Clean up query
        query = re.sub(r'\s+', ' ', query)  # Multiple spaces to single
        query = re.sub(r'\(\s*\)', '', query)  # Empty parentheses
        query = query.strip()
        
        return query
    
    def _generate_placeholder_value(self, placeholder: str, job_analysis: Dict[str, Any], job_description: str, strategy: str) -> str:
        """Generate value for a specific placeholder"""
        
        text = job_description.lower()
        
        if placeholder == "location":
            locations = job_analysis.get("locations", [])
            if locations:
                return f'"{locations[0]}"'
            return ""
        
        elif placeholder == "experience":
            seniority = job_analysis.get("seniority", "mid")
            if seniority == "senior":
                return '"5+ years" OR "6+ years" OR "senior"'
            elif seniority == "mid":
                return '"3+ years" OR "4+ years" OR "mid"'
            return ""
        
        elif placeholder == "tech_stack":
            skills = job_analysis.get("skills", {})
            tech_terms = []
            for category, skill_list in skills.items():
                tech_terms.extend(skill_list[:2])  # Top 2 from each category
            
            if tech_terms:
                term_strings = [f'"{term}"' for term in tech_terms[:4]]
                return f'({" OR ".join(term_strings)})'
            return ""
        
        elif placeholder == "cloud_platforms":
            if any(term in text for term in ["aws", "amazon web services"]):
                return "AWS OR Amazon Web Services"
            elif any(term in text for term in ["azure", "microsoft azure"]):
                return "Azure OR Microsoft Azure"
            elif any(term in text for term in ["gcp", "google cloud"]):
                return "GCP OR Google Cloud"
            return "AWS OR Azure OR GCP"
        
        elif placeholder == "iac_tools":
            if "pulumi" in text:
                return '"Pulumi"'
            elif "terraform" in text:
                return '"Terraform"'
            return '"Infrastructure as Code" OR "IaC"'
        
        elif placeholder == "ml_frameworks":
            frameworks = []
            if "tensorflow" in text:
                frameworks.append("TensorFlow")
            if "pytorch" in text:
                frameworks.append("PyTorch")
            if frameworks:
                return f'({" OR ".join(frameworks)})'
            return "(TensorFlow OR PyTorch OR scikit-learn)"
        
        elif placeholder == "company_context":
            if any(term in text for term in ["startup", "series"]):
                return "(startup OR early stage OR series)"
            elif any(term in text for term in ["enterprise", "large"]):
                return "(enterprise OR large company)"
            return ""
        
        elif placeholder == "programming_languages":
            languages = []
            for lang in ["python", "javascript", "java", "golang", "typescript"]:
                if lang in text:
                    languages.append(lang.capitalize())
            
            if languages:
                return f'({" OR ".join(languages)})'
            return ""
        
        elif placeholder == "tax_credentials":
            return '"CPA" OR "Certified Public Accountant"'
        
        elif placeholder == "industry_context":
            industry = job_analysis.get("industry", "tech")
            if industry == "tech":
                return "(startup OR early stage OR seed OR series)"
            elif industry == "finance":
                return "(financial services OR banking OR fintech)"
            return ""
        
        # Default empty for unknown placeholders
        return ""

class AdvancedSourcingAgent:
    """Advanced sourcing agent with role-specific query generation and smart evaluation"""
    
    def __init__(self):
        self.analyzer = JobDescriptionAnalyzer()
        self.query_generator = QueryGenerator()
        self.smart_evaluator = SmartEvaluator()
        
        # Performance tracking
        self.query_performance = []
        
        # API configuration
        self.search_url = "https://www.googleapis.com/customsearch/v1"
        self.api_key =st.secrets["GOOGLE_API_KEY"]  # Changed from GOOGLE_SEARCH_API_KEY
        self.search_engine_id = st.secrets["SEARCH_ENGINE_ID"]
    def search_candidates(self, job_description: str, num_candidates: int = 10) -> Dict[str, Any]:
        """Enhanced candidate search with smart evaluation"""
        print(f"🚀 Starting advanced candidate search for {num_candidates} candidates...")
        start_time = time.time()
        
        # Step 1: Analyze job description
        print("📊 Analyzing job description...")
        job_analysis = self.analyzer.analyze_job(job_description)
        print(f"✅ Analysis complete: {job_analysis['job_family']} role, {job_analysis['seniority']} level")
        
        # Step 2: Generate targeted search queries
        print("🎯 Generating targeted search queries...")
        queries = self.query_generator.generate_queries(job_analysis, job_description)
        print(f"✅ Generated {len(queries)} specialized queries")
        
        # Step 3: Execute searches
        all_candidates = []
        unique_urls = set()
        
        for i, query_info in enumerate(queries):
            print(f"🔍 Executing query {i+1}/{len(queries)}:")
            query = query_info["query"]
            
            # Execute search
            results = self._execute_search(query, num_candidates)
            
            if results:
                print(f"📈 Found {len(results)} total results, returned {len(results)} items")
                
                # Filter to LinkedIn profiles
                linkedin_profiles = self._filter_linkedin_profiles(results)
                print(f"🎯 Filtered to {len(linkedin_profiles)} LinkedIn profiles")
                
                # Track performance
                self.query_performance.append({
                    "query": query[:80] + "..." if len(query) > 80 else query,
                    "total_results": len(results),
                    "linkedin_profiles": len(linkedin_profiles),
                    "strategy": query_info["strategy"]
                })
                
                # Deduplicate based on URL
                for profile in linkedin_profiles:
                    if profile["link"] not in unique_urls:
                        unique_urls.add(profile["link"])
                        all_candidates.append(profile)
        
        print(f"🎯 Found {len(all_candidates)} unique profiles after deduplication")
        
        # Step 4: Smart evaluation using SRN FitScore
        evaluated_candidates = []
        candidates_to_evaluate = all_candidates[:min(num_candidates*2, len(all_candidates))]
        
        for i, candidate in enumerate(candidates_to_evaluate):
            print(f"📈 Evaluating candidate {i+1}/{len(candidates_to_evaluate)}")
            
            # Use SmartEvaluator for comprehensive assessment
            smart_assessment = self.smart_evaluator.evaluate_candidate_smart(candidate, job_description)
            
            # Combine original profile with smart assessment
            enhanced_candidate = {
                **candidate,
                "smart_assessment": smart_assessment,
                "fit_score": smart_assessment["fit_score"],
                "recommendation": smart_assessment["recommendation"],
                "context": smart_assessment["context"],
                "hiring_criteria": smart_assessment["hiring_criteria"]
            }
            
            evaluated_candidates.append(enhanced_candidate)
        
        # Step 5: Sort by fit score and return top candidates
        evaluated_candidates.sort(key=lambda x: x["fit_score"], reverse=True)
        top_candidates = evaluated_candidates[:num_candidates]
        
        end_time = time.time()
        print(f"✅ Search completed in {end_time - start_time:.2f} seconds")
        print(f"🏆 Returning {len(top_candidates)} top candidates")
        
        return {
            "candidates": top_candidates,
            "job_analysis": job_analysis,
            "queries_used": queries,
            "query_performance": self.query_performance,
            "total_time": end_time - start_time,
            "total_found": len(all_candidates)
        }
    
    def _execute_search(self, query: str, num_results: int = 10) -> List[Dict]:
        """Execute Google search for LinkedIn profiles"""
        print(f"🔍 Executing query: {query[:100]}...")
        
        try:
            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "q": query,
                "num": min(num_results, 10)  # Google API limit
            }
            
            response = requests.get(self.search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "items" in data:
                return data["items"]
            else:
                print(f"No items found in search results")
                return []
                
        except Exception as e:
            print(f"❌ Search failed: {str(e)}")
            return []
    
    def _filter_linkedin_profiles(self, search_results: List[Dict]) -> List[Dict]:
        """Filter and clean LinkedIn profile results"""
        linkedin_profiles = []
        
        for item in search_results:
            link = item.get("link", "")
            
            # Check if it's a LinkedIn profile
            if "linkedin.com/in/" in link:
                profile = {
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": link,
                    "source": "linkedin"
                }
                linkedin_profiles.append(profile)
        
        return linkedin_profiles
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get query performance analytics"""
        if not self.query_performance:
            return {
                "message": "No performance data available",
                "total_queries": 0,
                "queries": [],
                "avg_linkedin_profiles": 0,
                "success_rate": 0
            }
        
        return {
            "total_queries": len(self.query_performance),
            "queries": self.query_performance,
            "avg_linkedin_profiles": sum(q["linkedin_profiles"] for q in self.query_performance) / len(self.query_performance),
            "success_rate": sum(1 for q in self.query_performance if q["linkedin_profiles"] > 0) / len(self.query_performance) * 100
        }

if __name__ == "__main__":
    # Test the advanced sourcing agent
    agent = AdvancedSourcingAgent()
    
    # Sample job description
    job_description = """
    Senior DevOps Engineer
    San Francisco, California
    Engineering / On-site
    
    Ivo AI is building tools to help every company in the world make sense of their contracts. 
    The tools are getting popular - we've just raised a $16M Series A. Now, we need your help.
    
    What we're looking for:
    We're looking for a seasoned DevOps engineer to:
    - Own and shape the future of our environment
    - Manage dozens, hundreds, thousands of customer deployments
    - Instrument our system so we understand performance bottlenecks, errors, etc.
    - Get our CI/CD system running super quickly (it currently takes ~12 minutes)
    
    About you:
    - Passionate about orchestration and Infrastructure as Code. We're currently using Pulumi
    - Want to move quickly while striving for best practices
    - Can write code, preferably JavaScript
    - Experienced with either Azure and or GCP
    - Deeply knowledgeable about computers. Linux systems, containers, SQL databases, cloud infrastructure
    - 5+ years experience with Infrastructure as Code
    """
    
    # Search for candidates
    results = agent.search_candidates(job_description, num_candidates=5)
    
    print("\n" + "="*80)
    print("ADVANCED SOURCING RESULTS")
    print("="*80)
    
    # Show job analysis
    job_analysis = results["job_analysis"]
    print(f"\n📊 Job Analysis:")
    print(f"   Family: {job_analysis['job_family']}")
    print(f"   Seniority: {job_analysis['seniority']}")
    print(f"   Industry: {job_analysis['industry']}")
    print(f"   Skills Found: {job_analysis['total_skills']}")
    print(f"   Technical Role: {job_analysis['is_technical']}")
    
    # Show queries used
    print(f"\n🎯 Search Queries Used:")
    for i, query_info in enumerate(results["queries_used"]):
        print(f"   {i+1}. {query_info['strategy']}: {query_info['description']}")
    
    # Show top candidates with smart evaluation
    print(f"\n🏆 Top Candidates (Smart Evaluated):")
    for i, candidate in enumerate(results["candidates"][:3]):
        print(f"\n   Candidate {i+1}:")
        print(f"   Title: {candidate['title']}")
        print(f"   Smart Fit Score: {candidate['fit_score']}/10.0")
        print(f"   Recommendation: {candidate['recommendation']}")
        print(f"   Context: {candidate['context']}")
        print(f"   Strengths: {candidate['smart_assessment']['evaluation']['strengths']}")
        print(f"   Profile: {candidate['link']}")
    
    # Show performance summary
    performance = agent.get_performance_summary()
    print(f"\n📊 Query Performance Summary:")
    if "total_queries" in performance:
        print(f"   Total Queries: {performance['total_queries']}")
        print(f"   Success Rate: {performance['success_rate']:.1f}%")
        for query in performance["queries"]:
            print(f"   Query: {query['query']}")
            print(f"   Results: {query['linkedin_profiles']}/{query['total_results']} (Success Rate: {(query['linkedin_profiles']/max(query['total_results'], 1)*100):.2f}%)")
    else:
        print(f"   {performance.get('message', 'No performance data available')}")
