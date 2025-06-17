from smart_sourcing_agent import SmartSourcingAgent
import json
from datetime import datetime

def test_agent():
    # Initialize the agent
    agent = SmartSourcingAgent()
    
    # Test job description
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
    
    print("Starting agent test...")
    print("\n1. Finding candidates...")
    candidates = agent.find_top_candidates(job_description, num_candidates=5)
    
    print("\n2. Results:")
    for i, candidate in enumerate(candidates, 1):
        print(f"\nCandidate {i}:")
        print(f"Score: {sum(candidate['score'].values())}")
        print(f"Profile: {json.dumps(candidate['profile'], indent=2)}")
        print("---")
    
    print("\n3. Agent Performance Metrics:")
    print(json.dumps(agent.memory.performance_metrics, indent=2))
    
    print("\n4. Successful Search Patterns:")
    print(json.dumps(agent.memory.search_patterns, indent=2))
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_agent() 