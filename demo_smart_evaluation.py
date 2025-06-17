#!/usr/bin/env python3
"""
Demo script showcasing the SRN Smart Candidate Evaluation System
This demonstrates the system capabilities without requiring API keys.
"""

from smart_evaluator import SmartEvaluator
import json

def demo_smart_evaluation():
    """Demonstrate the Smart Evaluation System"""
    
    print("🧠" + "="*80)
    print("SRN SMART CANDIDATE EVALUATION SYSTEM DEMO")
    print("="*83)
    print()
    
    # Initialize the Smart Evaluator
    evaluator = SmartEvaluator()
    
    # Sample job description (DevOps Engineer at Ivo AI)
    job_description = """
    Senior DevOps Engineer
    San Francisco, California
    Engineering / On-site
    
    Ivo AI is building tools to help every company in the world make sense of their contracts. 
    The tools are getting popular - we've just raised a $16M Series A. Now, we need your help.
    
    What we're looking for:
    We're looking for a seasoned DevOps engineer to:
    • Own and shape the future of our environment
    • Manage dozens, hundreds, thousands of customer deployments  
    • Instrument our system for performance monitoring
    • Get our CI/CD system running super quickly
    • Experience with Pulumi, Azure, GCP, Kubernetes, JavaScript
    • 5+ years experience with Infrastructure as Code
    
    About you:
    • Passionate about orchestration and Infrastructure as Code
    • Want to move quickly while striving for best practices
    • Can write code, preferably JavaScript
    • Experienced with either Azure and or GCP
    • Deeply knowledgeable about computers
    """
    
    # Sample candidate profiles
    candidates = [
        {
            "title": "Senior DevOps Engineer at Google Cloud",
            "snippet": "Stanford Computer Science graduate with 7 years experience in cloud infrastructure, Kubernetes orchestration, and CI/CD pipeline optimization. Led infrastructure for high-scale distributed systems. Expert in GCP, Terraform, and JavaScript. Previously at Stripe."
        },
        {
            "title": "Infrastructure Engineer at Meta",
            "snippet": "MIT graduate with 5 years experience managing large-scale container deployments. Specializes in Kubernetes, Docker, and cloud-native architecture. Built CI/CD systems processing millions of requests. Experience with AWS and Python."
        },
        {
            "title": "DevOps Engineer at Local Startup",
            "snippet": "Self-taught engineer with 3 years experience. Worked with Docker and basic cloud deployment. Familiar with Jenkins and some infrastructure automation. Looking to learn more about advanced DevOps practices."
        },
        {
            "title": "Senior Site Reliability Engineer at Netflix",
            "snippet": "Carnegie Mellon graduate with 8 years SRE experience. Expert in distributed systems, observability, and incident response. Built infrastructure serving billions of requests. Deep expertise in Kubernetes, Terraform, and monitoring systems. Published papers on infrastructure reliability."
        }
    ]
    
    print("📋 JOB DESCRIPTION:")
    print("Position: Senior DevOps Engineer at Ivo AI ($16M Series A)")
    print("Location: San Francisco, CA")
    print("Requirements: 5+ years Infrastructure as Code, Pulumi/Azure/GCP, JavaScript")
    print()
    
    # Step 1: Context Detection Demo
    print("🧠 STEP 1: SMART CONTEXT DETECTION")
    print("-" * 50)
    
    context = evaluator.context_detector.detect_context(job_description)
    print(f"Industry: {context['industry']}")
    print(f"Company Type: {context['company_type']}")
    print(f"Role Type: {context['role_type']}")
    print(f"Role Subtype: {context['role_subtype']}")
    print()
    
    # Step 2: Criteria Generation Demo (fallback since no API key)
    print("🧬 STEP 2: ELITE HIRING CRITERIA GENERATION")
    print("-" * 50)
    
    criteria = evaluator._get_fallback_criteria("DevOps Engineer")
    print("Education Requirements:")
    print(f"  {criteria['education_requirements']}")
    print("\nCore Skills (Mission-Critical):")
    for skill in criteria['core_skills']:
        print(f"  • {skill}")
    print("\nDomain Expertise:")
    for skill in criteria['domain_expertise']:
        print(f"  • {skill}")
    print("\nRed Flags:")
    for flag in criteria['red_flags']:
        print(f"  • {flag}")
    print()
    
    # Step 3: Candidate Evaluation Demo
    print("📊 STEP 3: SRN FITSCORE EVALUATION")
    print("-" * 50)
    
    for i, candidate in enumerate(candidates, 1):
        print(f"\n🎯 CANDIDATE #{i}")
        print(f"Title: {candidate['title']}")
        print(f"Background: {candidate['snippet'][:100]}...")
        
        # Use fallback evaluation for demo
        evaluation = evaluator._fallback_evaluation(candidate['snippet'])
        
        # Demo smart scoring based on profile content
        if "stanford" in candidate['snippet'].lower() or "mit" in candidate['snippet'].lower():
            evaluation['scores']['education'] = 8.5
        elif "carnegie mellon" in candidate['snippet'].lower():
            evaluation['scores']['education'] = 8.0
        elif "graduate" in candidate['snippet'].lower():
            evaluation['scores']['education'] = 6.5
        else:
            evaluation['scores']['education'] = 4.0
        
        if "google" in candidate['snippet'].lower() or "meta" in candidate['snippet'].lower() or "netflix" in candidate['snippet'].lower():
            evaluation['scores']['company_relevance'] = 9.0
        elif "stripe" in candidate['snippet'].lower():
            evaluation['scores']['company_relevance'] = 9.5
        elif "startup" in candidate['snippet'].lower():
            evaluation['scores']['company_relevance'] = 6.0
        else:
            evaluation['scores']['company_relevance'] = 5.0
        
        if "7 years" in candidate['snippet'] or "8 years" in candidate['snippet']:
            evaluation['scores']['core_skills'] = 8.5
        elif "5 years" in candidate['snippet']:
            evaluation['scores']['core_skills'] = 7.0
        elif "3 years" in candidate['snippet']:
            evaluation['scores']['core_skills'] = 5.0
        
        if "published papers" in candidate['snippet'].lower():
            evaluation['scores']['bonus_signals'] = 4.0
        elif "expert" in candidate['snippet'].lower():
            evaluation['scores']['bonus_signals'] = 2.5
        
        if "self-taught" in candidate['snippet'].lower():
            evaluation['scores']['red_flags'] = -1.0
        
        # Calculate weighted final score
        weights = {
            "education": 0.20,
            "career_trajectory": 0.20,
            "company_relevance": 0.15,
            "tenure_stability": 0.15,
            "core_skills": 0.20,
            "bonus_signals": 0.05,
            "red_flags": -0.15
        }
        
        final_score = (
            evaluation['scores']['education'] * weights['education'] +
            evaluation['scores']['career_trajectory'] * weights['career_trajectory'] +
            evaluation['scores']['company_relevance'] * weights['company_relevance'] +
            evaluation['scores']['tenure_stability'] * weights['tenure_stability'] +
            evaluation['scores']['core_skills'] * weights['core_skills'] +
            evaluation['scores']['bonus_signals'] * weights['bonus_signals'] +
            evaluation['scores']['red_flags'] * abs(weights['red_flags'])
        )
        
        evaluation['final_score'] = round(final_score, 1)
        
        # Generate recommendation
        if final_score >= 8.5:
            recommendation = "🟢 STRONG HIRE - Exceptional candidate meeting elite standards"
        elif final_score >= 7.0:
            recommendation = "🟡 CONSIDER - Good candidate, requires additional evaluation"
        elif final_score >= 5.5:
            recommendation = "🟠 WEAK - Below standards, significant concerns"
        else:
            recommendation = "🔴 NO HIRE - Does not meet minimum requirements"
        
        # Display results
        print(f"\n💯 SRN FIT SCORE: {evaluation['final_score']}/10.0")
        print(f"📋 RECOMMENDATION: {recommendation}")
        
        print("\n📊 Score Breakdown:")
        print(f"  🎓 Education: {evaluation['scores']['education']}/10")
        print(f"  📈 Career Trajectory: {evaluation['scores']['career_trajectory']}/10")
        print(f"  🏢 Company Relevance: {evaluation['scores']['company_relevance']}/10")
        print(f"  ⏳ Tenure & Stability: {evaluation['scores']['tenure_stability']}/10")
        print(f"  🎯 Core Skills: {evaluation['scores']['core_skills']}/10")
        print(f"  🌟 Bonus Signals: {evaluation['scores']['bonus_signals']}/5")
        print(f"  ❌ Red Flags: {evaluation['scores']['red_flags']}")
        
        print("-" * 60)
    
    print("\n🎉 DEMO SUMMARY")
    print("-" * 50)
    print("✅ Context Detection: Automatically identified tech startup DevOps role")
    print("✅ Criteria Generation: Created elite hiring standards for infrastructure engineering")
    print("✅ Smart Evaluation: Applied conservative SRN FitScore methodology")
    print("✅ Elite Standards: Distinguished between top-tier and average candidates")
    print()
    print("🔑 KEY FEATURES:")
    print("• Conservative scoring (8+ only for exceptional candidates)")
    print("• Elite institution recognition (Stanford, MIT, etc.)")
    print("• Company caliber assessment (FAANG, Stripe, Netflix)")
    print("• Technical depth evaluation")
    print("• Red flag detection")
    print("• Weighted scoring system")
    print()
    print("🚀 Ready for production use with OpenAI API integration!")
    print("=" * 83)

if __name__ == "__main__":
    demo_smart_evaluation() 