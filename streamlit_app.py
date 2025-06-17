import streamlit as st
import json
import time
from advanced_sourcing_agent import AdvancedSourcingAgent
from smart_evaluator import SmartEvaluator

# Page configuration
st.set_page_config(
    page_title="🧠 SRN Smart Sourcing Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .candidate-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .fit-score {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
    }
    .score-excellent { color: #28a745; }
    .score-good { color: #ffc107; }
    .score-fair { color: #fd7e14; }
    .score-poor { color: #dc3545; }
    .criteria-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'agent' not in st.session_state:
        st.session_state.agent = AdvancedSourcingAgent()
    if 'smart_evaluator' not in st.session_state:
        st.session_state.smart_evaluator = SmartEvaluator()
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None

def get_sample_jobs():
    """Sample job descriptions for testing"""
    return {
        "Senior DevOps Engineer (Ivo AI)": """
Senior DevOps Engineer
San Francisco, California
Engineering / On-site

Ivo AI is building tools to help every company in the world make sense of their contracts. The tools are getting popular - we've just raised a $16M Series A. Now, we need your help.

What we're looking for:
We're looking for a seasoned DevOps engineer to:
• Own and shape the future of our environment. We still have a relatively minimal footprint, giving you a lot of freedom to design the system.
• Manage dozens, hundreds, thousands (?) of customer deployments. Customers are cagey about their contracts, so each customer gets their own containers, database, VPC, etc. It's a lot to orchestrate.
• Instrument our system so we understand performance bottlenecks, errors, etc.
• Aggregate metrics/logs/health checks into slick dashboards and pager alerts
• Be on call and lead infrastructure related incidents
• Get our CI/CD system running super quickly (it currently takes ~12 minutes, boo)

In addition to helping us run a solid, high-performance distributed system, we'd love someone who's as excited about LLMs as we are. You'd be deeply embedded into the engineering team and encouraged to push the DevOps frontier by, for example:
• Developing on-the-fly LLM evals to monitor the real-time accuracy of our responses
• Building autonomous agents to detect and diagnose production issues before they become major fires

About you:
• Passionate about orchestration and Infrastructure as Code. We're currently using Pulumi but open to change if you have strong opinions here.
• Want to move quickly while striving for best practices.
• Relentlessly resourceful.
• Can write code, preferably JavaScript.
• Experienced with either Azure and or GCP
• Deeply knowledgeable about computers. Linux systems, containers, SQL databases, cloud infrastructure, etc.
• 5+ years experience with Infrastructure as Code

Compensation: $170K-$260K base salary
        """,
        
        "ML Engineer (Audio AI Startup)": """
Machine Learning Engineer
Remote (US/Canada)
Engineering / Remote

We're building the future of conversational AI for sales teams. Our platform uses cutting-edge audio AI to understand and optimize sales conversations in real-time.

What you'll do:
• Design and implement ML models for speech recognition, natural language understanding, and conversation analysis
• Build production ML pipelines that process millions of sales calls daily
• Develop real-time inference systems with sub-100ms latency requirements
• Create ML-powered features like sentiment analysis, objection detection, and coaching recommendations
• Work on audio signal processing, speaker diarization, and voice activity detection
• Optimize models for both accuracy and computational efficiency

Requirements:
• 4+ years of production ML experience, particularly in audio/speech domains
• Strong background in TensorFlow or PyTorch for deep learning
• Experience with speech recognition, NLP, or conversational AI systems
• Proficiency in Python and modern ML tools (MLflow, Kubeflow, etc.)
• Experience deploying ML models at scale in cloud environments
• Understanding of audio signal processing and feature extraction
• Familiarity with transformer architectures and attention mechanisms

Preferred:
• PhD in ML, Computer Science, or related field
• Experience with real-time audio processing
• Background in sales technology or CRM systems
• Open source contributions to ML projects

Compensation: $180K-$280K + equity
        """,
        
        "Tax Director (Mid-Size CPA Firm)": """
Tax Director
Los Angeles, California
Finance / On-site

SingerLewak, a leading CPA and advisory firm serving privately-held businesses, is seeking an experienced Tax Director to join our growing tax practice.

Responsibilities:
• Lead and manage a team of 8-12 tax professionals including managers and senior associates
• Oversee tax compliance and planning for high-net-worth individuals and complex business entities
• Represent clients before the IRS and state tax authorities during audits and examinations
• Develop tax strategies for mergers, acquisitions, and business restructuring
• Manage client relationships and serve as primary tax advisor for key accounts
• Supervise preparation of federal and state tax returns for individuals, partnerships, S-corps, and C-corps
• Provide tax research and technical guidance on complex matters
• Mentor and develop junior staff members

Requirements:
• CPA license (active and in good standing)
• 7-10 years of progressive tax experience in public accounting
• Bachelor's degree in Accounting, Finance, or related field
• Strong experience with tax research, planning, and compliance
• Proven supervisory and client management skills
• Experience with IRS representation and audit defense
• Knowledge of tax software (ProSystem fx, CCH Axcess, or similar)
• Strong communication and presentation skills

Preferred:
• Master's in Taxation or Tax LLM
• Experience with high-net-worth tax planning
• Knowledge of estate and gift tax matters
• Prior experience in regional or Big 4 accounting firm

Compensation: $140K-$180K + bonus + benefits
        """,
        
        "Senior Software Engineer (Fintech)": """
Senior Software Engineer
New York, NY / Remote
Engineering / Hybrid

Join our mission to revolutionize financial infrastructure. We're building next-generation payment systems that power millions of transactions for leading fintech companies.

What you'll build:
• High-performance payment processing systems handling billions in transaction volume
• Real-time fraud detection and risk management systems
• APIs and microservices used by hundreds of fintech partners
• Data pipelines for financial reporting and compliance
• Developer tools and SDKs for payment integration

Tech stack:
• Backend: Python, Java, Go, PostgreSQL, Redis, Kafka
• Infrastructure: AWS, Kubernetes, Terraform, DataDog
• Frontend: React, TypeScript, GraphQL

Requirements:
• 5+ years of software engineering experience
• Strong background in building scalable backend systems
• Experience with financial systems, payments, or regulated industries
• Proficiency in at least two programming languages (Python, Java, Go, etc.)
• Knowledge of microservices architecture and distributed systems
• Experience with cloud platforms (AWS preferred)
• Understanding of database design and optimization

Preferred:
• Experience in fintech, banking, or payments industry
• Knowledge of financial regulations (PCI DSS, SOX, etc.)
• Contributions to open source projects
• Computer Science degree from top-tier university

Compensation: $180K-$250K + equity + benefits
        """
    }

def display_job_analysis(analysis):
    """Display job analysis results"""
    st.subheader("📊 Smart Job Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Job Family", analysis.get('job_family', 'Unknown'))
    with col2:
        st.metric("Seniority Level", analysis.get('seniority', 'Unknown'))
    with col3:
        st.metric("Industry", analysis.get('industry', 'Unknown'))
    with col4:
        st.metric("Skills Found", analysis.get('total_skills', 0))
    
    # Additional details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Technical Role:**", "✅ Yes" if analysis.get('is_technical') else "❌ No")
    with col2:
        st.write("**Leadership Role:**", "✅ Yes" if analysis.get('is_leadership') else "❌ No")
    with col3:
        st.write("**Remote Eligible:**", "✅ Yes" if analysis.get('remote_eligible') else "❌ No")
    
    # Skills breakdown
    if analysis.get('skills'):
        with st.expander("🛠 Technical Skills Detected"):
            for category, skills in analysis['skills'].items():
                if skills:
                    st.write(f"**{category.replace('_', ' ').title()}:** {', '.join(skills)}")

def display_smart_criteria(criteria):
    """Display generated smart hiring criteria"""
    st.subheader("🧬 Elite Hiring Criteria (SRN Smart)")
    
    with st.expander("📋 View Complete Hiring Criteria", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎓 Education Requirements")
            st.write(criteria.get('education_requirements', 'Not specified'))
            
            st.markdown("### 🎯 Core Skills (Mission-Critical)")
            for skill in criteria.get('core_skills', []):
                st.write(f"• {skill}")
            
            st.markdown("### 🛠 Domain Expertise")
            for skill in criteria.get('domain_expertise', []):
                st.write(f"• {skill}")
        
        with col2:
            st.markdown("### 📈 Experience Markers")
            for marker in criteria.get('experience_markers', []):
                st.write(f"• {marker}")
            
            st.markdown("### 🏢 Company Preferences")
            for pref in criteria.get('company_preferences', []):
                st.write(f"• {pref}")
            
            st.markdown("### 🌟 Bonus Signals")
            for signal in criteria.get('bonus_signals', []):
                st.write(f"• {signal}")
        
        st.markdown("### ❌ Red Flags")
        for flag in criteria.get('red_flags', []):
            st.write(f"• {flag}")

def display_search_queries(queries):
    """Display generated search queries"""
    st.subheader("🎯 Generated X-Ray Search Queries")
    
    for i, query_info in enumerate(queries):
        with st.expander(f"Query {i+1}: {query_info['strategy'].title()} Strategy"):
            st.write(f"**Description:** {query_info['description']}")
            st.code(query_info['query'], language="text")
            st.write(f"**Character Count:** {len(query_info['query'])}")

def get_score_color_class(score):
    """Get CSS class for score color"""
    if score >= 8.5:
        return "score-excellent"
    elif score >= 7.0:
        return "score-good"
    elif score >= 5.5:
        return "score-fair"
    else:
        return "score-poor"

def display_candidate_card(candidate, rank):
    """Display individual candidate card with smart evaluation"""
    with st.container():
        # Create candidate card
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Fit Score
            score_class = get_score_color_class(candidate['fit_score'])
            st.markdown(f"""
            <div class="fit-score {score_class}">
                {candidate['fit_score']}/10.0
            </div>
            <div style="text-align: center; font-weight: bold;">SRN Fit Score</div>
            """, unsafe_allow_html=True)
            
            # Recommendation
            rec_color = {
                "🟢 STRONG HIRE": "#28a745",
                "🟡 CONSIDER": "#ffc107", 
                "🟠 WEAK": "#fd7e14",
                "🔴 NO HIRE": "#dc3545"
            }
            recommendation = candidate['recommendation']
            color = rec_color.get(recommendation.split(" - ")[0], "#6c757d")
            
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 0.5rem; border-radius: 5px; text-align: center; margin-top: 1rem;">
                <strong>{recommendation.split(" - ")[0]}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Candidate Details
            st.markdown(f"### Candidate #{rank}")
            st.write(f"**Title:** {candidate['title']}")
            st.write(f"**Profile:** [View LinkedIn]({candidate['link']})")
            
            # Context
            context = candidate['context']
            st.write(f"**Detected Context:** {context['industry']} | {context['role_type']} - {context['role_subtype']}")
            
            # Assessment Summary
            evaluation = candidate['smart_assessment']['evaluation']
            st.write(f"**Rationale:** {evaluation['rationale']}")
        
        with col3:
            # Score Breakdown
            st.write("**Score Breakdown:**")
            scores = evaluation['scores']
            
            score_items = [
                ("🎓 Education", scores.get('education', 0)),
                ("📈 Career", scores.get('career_trajectory', 0)),
                ("🏢 Company", scores.get('company_relevance', 0)),
                ("⏳ Tenure", scores.get('tenure_stability', 0)),
                ("🎯 Skills", scores.get('core_skills', 0)),
                ("🌟 Bonus", scores.get('bonus_signals', 0)),
                ("❌ Red Flags", scores.get('red_flags', 0))
            ]
            
            for label, score in score_items:
                if "Red Flags" in label:
                    st.write(f"{label}: {score}")
                else:
                    st.write(f"{label}: {score}/10")
        
        # Detailed Assessment
        with st.expander(f"📝 Detailed Assessment - Candidate #{rank}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ Strengths:**")
                for strength in evaluation['strengths']:
                    st.write(f"• {strength}")
            
            with col2:
                st.markdown("**⚠️ Weaknesses:**")
                for weakness in evaluation['weaknesses']:
                    st.write(f"• {weakness}")
            
            # Show hiring criteria used
            st.markdown("**🧬 Hiring Criteria Applied:**")
            criteria = candidate['hiring_criteria']
            st.write(f"**Education:** {criteria.get('education_requirements', 'N/A')}")
            st.write(f"**Core Skills:** {', '.join(criteria.get('core_skills', []))}")
            
            if evaluation.get('override_signal'):
                st.warning("⚡ **Override Signal:** This candidate shows extraordinary potential despite lower scores and should be considered for manual review.")
        
        st.markdown("---")

def display_performance_metrics(performance):
    """Display query performance metrics"""
    st.subheader("📊 Query Performance Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Queries", performance['total_queries'])
    with col2:
        st.metric("Success Rate", f"{performance['success_rate']:.1f}%")
    with col3:
        st.metric("Avg Profiles/Query", f"{performance['avg_linkedin_profiles']:.1f}")
    
    # Detailed query performance
    with st.expander("🔍 Detailed Query Performance"):
        for i, query in enumerate(performance['queries']):
            st.write(f"**Query {i+1} ({query['strategy']}):**")
            st.write(f"Query: `{query['query']}`")
            st.write(f"Results: {query['linkedin_profiles']}/{query['total_results']} profiles")
            success_rate = (query['linkedin_profiles']/max(query['total_results'], 1)*100)
            st.write(f"Success Rate: {success_rate:.1f}%")
            st.write("---")

def main():
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">🧠 SRN Smart Sourcing Agent</div>', unsafe_allow_html=True)
    st.markdown("### Elite Candidate Sourcing with AI-Powered Smart Hiring Criteria")
    
    # Sidebar with advanced features
    with st.sidebar:
        st.header("🎛 Smart Sourcing Controls")
        
        # Sample job selector
        st.subheader("📋 Sample Jobs")
        sample_jobs = get_sample_jobs()
        selected_job = st.selectbox("Choose a sample job:", list(sample_jobs.keys()))
        
        if st.button("Load Sample Job"):
            st.session_state.job_description = sample_jobs[selected_job]
        
        st.markdown("---")
        
        # Search parameters
        st.subheader("🔧 Search Parameters")
        num_candidates = st.slider("Number of candidates to find:", 3, 15, 5)
        
        st.markdown("---")
        
        # Advanced features info
        st.subheader("🌟 Smart Features")
        st.markdown("""
        **🧠 Context Detection:**
        - Auto-detects industry, role type, seniority
        - Identifies technical vs. non-technical roles
        
        **🧬 Smart Criteria Generation:**
        - Creates elite hiring standards
        - Role-specific requirements
        - Industry benchmarks
        
        **🎯 Dynamic Query Generation:**
        - Multiple search strategies per role
        - LinkedIn X-Ray optimization
        - Tech stack-specific targeting
        
        **📊 SRN FitScore Evaluation:**
        - Conservative 10-point scoring
        - Weighted category assessment
        - Elite institution recognition
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Job description input
        st.subheader("📝 Job Description")
        job_description = st.text_area(
            "Paste the job description here:",
            value=st.session_state.get('job_description', ''),
            height=300,
            help="Paste a complete job description. The system will automatically analyze it and generate targeted search strategies."
        )
    
    with col2:
        # Quick actions
        st.subheader("🚀 Quick Actions")
        
        if st.button("🧠 Analyze Job Only", type="secondary"):
            if job_description:
                with st.spinner("Analyzing job description..."):
                    analysis = st.session_state.agent.analyzer.analyze_job(job_description)
                    st.success("Analysis complete!")
                    display_job_analysis(analysis)
                    
                    # Generate criteria
                    context = st.session_state.smart_evaluator.context_detector.detect_context(job_description)
                    criteria = st.session_state.smart_evaluator._generate_criteria(context, job_description)
                    display_smart_criteria(criteria)
            else:
                st.error("Please enter a job description first!")
        
        if st.button("🎯 Generate Queries Only", type="secondary"):
            if job_description:
                with st.spinner("Generating search queries..."):
                    analysis = st.session_state.agent.analyzer.analyze_job(job_description)
                    queries = st.session_state.agent.query_generator.generate_queries(analysis, job_description)
                    st.success("Queries generated!")
                    display_search_queries(queries)
            else:
                st.error("Please enter a job description first!")
        
        if st.button("🔍 SEARCH CANDIDATES", type="primary"):
            if job_description:
                with st.spinner("🚀 Running smart candidate search..."):
                    start_time = time.time()
                    
                    # Execute search
                    results = st.session_state.agent.search_candidates(job_description, num_candidates)
                    st.session_state.search_results = results
                    
                    end_time = time.time()
                    st.success(f"Search completed in {end_time - start_time:.1f} seconds!")
            else:
                st.error("Please enter a job description first!")
    
    # Display results if available
    if st.session_state.search_results:
        results = st.session_state.search_results
        
        st.markdown("---")
        st.header("🎉 Smart Search Results")
        
        # Job analysis
        display_job_analysis(results['job_analysis'])
        
        # Smart criteria
        if results['candidates']:
            sample_criteria = results['candidates'][0]['hiring_criteria']
            display_smart_criteria(sample_criteria)
        
        # Search queries used
        display_search_queries(results['queries_used'])
        
        # Performance metrics
        performance = st.session_state.agent.get_performance_summary()
        display_performance_metrics(performance)
        
        # Candidates
        st.subheader(f"🏆 Top {len(results['candidates'])} Candidates (SRN Smart Evaluated)")
        
        if results['candidates']:
            for i, candidate in enumerate(results['candidates']):
                display_candidate_card(candidate, i + 1)
        else:
            st.warning("No candidates found. Try adjusting your search criteria or job description.")
        
        # Summary statistics
        st.subheader("📈 Search Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Found", results['total_found'])
        with col2:
            st.metric("Evaluated", len(results['candidates']))
        with col3:
            avg_score = sum(c['fit_score'] for c in results['candidates']) / len(results['candidates']) if results['candidates'] else 0
            st.metric("Avg Fit Score", f"{avg_score:.1f}/10")
        with col4:
            st.metric("Search Time", f"{results['total_time']:.1f}s")
        
        # Download results
        if st.button("📥 Download Results as JSON"):
            st.download_button(
                label="Download Search Results",
                data=json.dumps(results, indent=2, default=str),
                file_name=f"srn_search_results_{int(time.time())}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main() 