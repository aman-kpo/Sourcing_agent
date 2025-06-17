from advanced_sourcing_agent import JobDescriptionAnalyzer, QueryGenerator

def test_ml_detection():
    analyzer = JobDescriptionAnalyzer()
    generator = QueryGenerator()
    
    ml_job = """
    Machine Learning Engineer - Nooks.ai
    We have an ambitious product vision in AI-powered realtime collaboration.
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
    
    analysis = analyzer.analyze(ml_job)
    
    print("DEBUG: ML Job Analysis")
    print(f"Job Family: {analysis['job_family']}")
    print(f"Required Skills: {analysis['required_skills']}")
    print(f"Full analysis as string: {str(analysis)}")
    
    # Test role detection
    role_type = generator._determine_role_type(analysis)
    print(f"Detected Role Type: {role_type}")
    
    # Test if specific phrases are found
    job_text = str(analysis).lower()
    print(f"\nPhrase detection:")
    phrases = ["machine learning", "ml engineer", "ai engineer", "data scientist", "tensorflow", "pytorch", "scikit-learn", "nlp", "deep learning"]
    for phrase in phrases:
        if phrase in job_text:
            print(f"  ✅ Found: {phrase}")
        else:
            print(f"  ❌ Not found: {phrase}")

if __name__ == "__main__":
    test_ml_detection() 