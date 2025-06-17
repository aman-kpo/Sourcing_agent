from advanced_sourcing_agent import JobDescriptionAnalyzer, QueryGenerator

def demo_query_templates():
    """Demonstrate the job-specific query template system"""
    analyzer = JobDescriptionAnalyzer()
    generator = QueryGenerator()
    
    # Sample job descriptions from the user's examples
    job_examples = [
        {
            "title": "🔧 DevOps Engineer at AI Startup",
            "description": """
            Senior DevOps Engineer San Francisco, California Engineering / On-site 
            Ivo AI is building tools to help every company in the world make sense of their contracts. 
            We're looking for a seasoned DevOps engineer to own and shape the future of our environment.
            
            What we're looking for:
            * Manage dozens, hundreds, thousands of customer deployments
            * Instrument our system for performance monitoring  
            * Get our CI/CD system running super quickly
            * Experience with Pulumi, Azure, GCP, Kubernetes, JavaScript
            * 5+ years experience with Infrastructure as Code
            * LLM experience is a plus
            """
        },
        {
            "title": "🤖 ML Engineer at Sales AI Company", 
            "description": """
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
        },
        {
            "title": "💰 Tax Director at Accounting Firm",
            "description": """
            Tax Director San Jose, California
            SingerLewak is a Top 100 accounting and consulting firm.
            We are seeking a Tax Director with CPA certification.
            
            Responsibilities:
            * Performs technical tax review and approval of all tax returns
            * Serves as a subject matter expert in tax discipline
            * Represents clients before taxing authorities
            * Seven to ten years' experience in public accounting
            * At least two years' experience representing clients before taxing authorities
            * Bachelor's degree in accounting required, master's degree in taxation preferred
            * Current and valid certified public accountant's license is required
            """
        },
        {
            "title": "💻 Frontend Engineer at SaaS Company",
            "description": """
            Senior Frontend Engineer - React/TypeScript
            We're building the next generation of customer experience tools.
            
            Requirements:
            * 5+ years of frontend development experience
            * Expert in React, TypeScript, CSS, HTML
            * Experience with modern build tools (Webpack, Vite)
            * Knowledge of testing frameworks (Jest, Cypress)
            * San Francisco Bay Area or Remote
            """
        }
    ]
    
    print("🎯 QUERY TEMPLATE DEMONSTRATION")
    print("="*60)
    print("Showing how job descriptions are analyzed and converted into targeted LinkedIn X-Ray searches")
    
    for i, example in enumerate(job_examples):
        print(f"\n{example['title']}")
        print("-" * 50)
        
        # Analyze the job description
        analysis = analyzer.analyze(example['description'])
        
        print("📊 JOB ANALYSIS:")
        print(f"   • Job Family: {analysis['job_family']}")
        print(f"   • Seniority Level: {analysis['seniority_level']}")
        print(f"   • Industry: {analysis['industry']}")
        print(f"   • Required Skills: {analysis['required_skills']}")
        print(f"   • Location: {analysis['location_data']}")
        print(f"   • Experience Range: {analysis['experience_range']}")
        print(f"   • Technical Role: {analysis['technical_role']}")
        print(f"   • Company Context: {analysis['company_context']}")
        
        # Generate targeted queries
        queries = generator.generate_queries(analysis)
        
        print(f"\n🔍 GENERATED X-RAY SEARCH QUERIES:")
        for j, query in enumerate(queries, 1):
            print(f"   Query {j}: {query}")
            print(f"   Length: {len(query)} characters")
        
        # Show role type determination
        role_type = generator._determine_role_type(analysis)
        print(f"\n🎯 Detected Role Type: {role_type}")
        
        # Show template mappings used
        templates = generator._get_templates_for_role(role_type)
        print(f"📋 Available Templates: {list(templates.keys())}")
        
        if i < len(job_examples) - 1:
            print("\n" + "="*60)

def show_template_library():
    """Show the complete template library"""
    generator = QueryGenerator()
    
    print("\n🏗️  COMPLETE TEMPLATE LIBRARY")
    print("="*60)
    
    for role_type, templates in generator.query_templates.items():
        print(f"\n📁 {role_type.upper().replace('_', ' ')} TEMPLATES:")
        for template_name, template in templates.items():
            print(f"   • {template_name}: {template}")
    
    print(f"\n🔧 KEYWORD MAPPINGS:")
    for domain, mappings in generator.keyword_mappings.items():
        print(f"\n   📂 {domain.upper()}:")
        for placeholder, keywords in mappings.items():
            print(f"      • {placeholder}: {keywords}")

if __name__ == "__main__":
    demo_query_templates()
    show_template_library()
    
    print(f"\n✨ KEY FEATURES DEMONSTRATED:")
    print("   • Job description parsing and classification")
    print("   • Industry-specific keyword extraction")
    print("   • Role-specific query template selection") 
    print("   • Dynamic placeholder replacement")
    print("   • Query length optimization")
    print("   • Multiple query strategies per role type")
    print("\n✅ Demo complete!") 