from smart_sourcing_agent import SmartSourcingAgent
import json

def debug_agent():
    """Debug the smart sourcing agent step by step"""
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
    
    print("=== DEBUGGING SMART SOURCING AGENT ===\n")
    
    # Step 1: Extract job context
    print("1. Extracting job context...")
    try:
        criteria = agent.extract_job_context(job_description)
        print("✅ Job context extracted successfully")
        print(json.dumps(criteria, indent=2))
    except Exception as e:
        print(f"❌ Error extracting job context: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Step 2: Generate X-Ray query
    print("2. Generating X-Ray search query...")
    try:
        query = agent.generate_xray_query(criteria)
        print("✅ Query generated successfully")
        print(f"Query: {query}")
    except Exception as e:
        print(f"❌ Error generating query: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Step 3: Search LinkedIn profiles
    print("3. Searching LinkedIn profiles...")
    try:
        profiles = agent.search_linkedin_profiles(query, num_results=3)
        print(f"✅ Search completed - Found {len(profiles)} profiles")
        for i, profile in enumerate(profiles):
            print(f"\nProfile {i+1}:")
            print(f"  Title: {profile['title']}")
            print(f"  URL: {profile['url']}")
            print(f"  Snippet: {profile['snippet'][:100]}...")
    except Exception as e:
        print(f"❌ Error searching profiles: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Step 4: Evaluate candidates
    if profiles:
        print("4. Evaluating first candidate...")
        try:
            score = agent.evaluate_candidate(profiles[0], criteria)
            print("✅ Evaluation completed")
            print(json.dumps(score, indent=2))
        except Exception as e:
            print(f"❌ Error evaluating candidate: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Step 5: Full pipeline
    print("5. Running full pipeline...")
    try:
        top_candidates = agent.find_top_candidates(job_description, num_candidates=3)
        print(f"✅ Pipeline completed - Found {len(top_candidates)} candidates")
        for i, candidate in enumerate(top_candidates):
            print(f"\nCandidate {i+1}:")
            print(f"  Overall Fit: {candidate['score'].get('overall_fit', 0)}")
            print(f"  Title: {candidate['profile']['title']}")
    except Exception as e:
        print(f"❌ Error in full pipeline: {e}")

if __name__ == "__main__":
    debug_agent() 