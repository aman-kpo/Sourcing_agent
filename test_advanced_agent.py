from advanced_sourcing_agent import AdvancedSourcingAgent
import time

def test_job_examples():
    """Test the advanced sourcing agent with different job types"""
    agent = AdvancedSourcingAgent()
    
    # Test cases from the examples provided
    test_jobs = [
        {
            "name": "DevOps Engineer",
            "description": """
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
        },
        {
            "name": "ML Engineer",
            "description": """
            Machine Learning Engineer - Nooks.ai
            We have an ambitious product vision in a nascent area - AI-powered realtime collaboration.
            This is a role focused on implementing ML features into Nooks.
            
            Responsibilities:
            * Training production models for sales use cases
            * Realtime audio AI & precision/recall/latency tradeoffs
            * Smart call funnels & playbooks using GPT-3
            * Conversation embeddings & markov models
            * 3+ years of industry experience with ML models in production
            * Proficiency in Python, TensorFlow, PyTorch, scikit-learn
            * Expertise in NLP, Deep Learning, Transformers and Large Language Models
            """
        },
        {
            "name": "Tax Director", 
            "description": """
            Tax Director San Jose, California
            SingerLewak is a Top 100 accounting and consulting firm.
            
            Responsibilities:
            * Performs technical tax review and approval of all tax returns
            * Serves as a subject matter expert in tax discipline
            * Represents clients before taxing authorities
            * Seven to ten years' experience in public accounting
            * At least two years' experience representing clients before taxing authorities
            * Bachelor's degree in accounting required, master's degree in taxation preferred
            * Current and valid certified public accountant's license is required
            * $167,000 - $228,000 a year
            """
        }
    ]
    
    for i, job in enumerate(test_jobs):
        print(f"\n{'='*60}")
        print(f"TEST {i+1}: {job['name']}")
        print(f"{'='*60}")
        
        # Analyze the job to show the parsing capabilities
        print("\n📊 JOB ANALYSIS:")
        analysis = agent.analyzer.analyze(job['description'])
        print(f"   Job Family: {analysis['job_family']}")
        print(f"   Seniority: {analysis['seniority_level']}")
        print(f"   Industry: {analysis['industry']}")
        print(f"   Skills: {analysis['required_skills']}")
        print(f"   Location: {analysis['location_data']}")
        print(f"   Company Context: {analysis['company_context']}")
        
        # Generate and show the queries
        print("\n🎯 GENERATED QUERIES:")
        queries = agent.query_generator.generate_queries(analysis)
        for j, query in enumerate(queries):
            print(f"   Query {j+1}: {query}")
        
        # Search for candidates (limiting to 2 for demo)
        print(f"\n🔍 SEARCHING FOR CANDIDATES...")
        candidates = agent.find_top_candidates(job['description'], 2)
        
        print(f"\n🏆 TOP CANDIDATES:")
        for k, candidate in enumerate(candidates):
            print(f"   Candidate {k+1}:")
            print(f"     Overall Fit: {candidate['score'].get('overall_fit', 0)}/100")
            print(f"     Skills Match: {candidate['score'].get('skills_match', 0)}/100")
            print(f"     Title: {candidate['profile']['title']}")
            print(f"     URL: {candidate['profile']['url']}")
        
        # Add delay between tests
        if i < len(test_jobs) - 1:
            print("\n⏳ Waiting 5 seconds before next test...")
            time.sleep(5)

if __name__ == "__main__":
    print("🚀 ADVANCED SOURCING AGENT DEMO")
    print("Testing job-specific query templates and intelligent parsing")
    test_job_examples()
    print("\n✅ DEMO COMPLETE!") 