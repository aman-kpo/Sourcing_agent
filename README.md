# 🧠 SRN Smart Sourcing Agent

**Elite Candidate Sourcing with AI-Powered Smart Hiring Criteria**

A next-generation recruiting system that combines advanced LinkedIn X-Ray search generation with the SRN FitScore methodology for conservative, elite-standard candidate evaluation.

## 🌟 Overview

This system revolutionizes technical recruiting by:

1. **🧠 Smart Context Detection** - Automatically analyzes job descriptions to identify industry, company type, role specifics, and technical requirements
2. **🧬 Elite Hiring Criteria Generation** - Creates demanding, role-specific standards based on top 1-2% performer benchmarks
3. **🎯 Dynamic Query Generation** - Generates multiple optimized LinkedIn X-Ray search strategies per role
4. **📊 SRN FitScore Evaluation** - Conservative 10-point scoring system that distinguishes truly exceptional candidates

## 🏆 Key Features

### Advanced Job Analysis
- **Industry Classification**: Tech, Finance, Healthcare, Legal, etc.
- **Role Family Detection**: Engineering, Data, Product, Sales, Finance, etc.
- **Seniority Assessment**: Entry, Mid, Senior, Executive levels
- **Technical Skills Extraction**: Regex-based detection of 200+ technologies
- **Company Context Analysis**: Startup vs Enterprise, funding stage, culture

### Smart Hiring Criteria
- **Education Standards**: Elite university requirements or equivalent excellence
- **Core Skills**: Mission-critical capabilities (what they must DO, not just know)
- **Domain Expertise**: Technical/functional depth requirements
- **Experience Markers**: Proof of ownership, scale, and impact
- **Company Caliber**: Preference for high-bar organizations
- **Red Flags**: Automatic detection of disqualifying patterns

### LinkedIn X-Ray Query Generation
- **Role-Specific Templates**: DevOps, ML Engineer, Tax Director, Software Engineer
- **Multi-Strategy Approach**: Primary, specialized, and industry-specific queries
- **Dynamic Placeholders**: Location, experience, tech stack, company context
- **Query Optimization**: Character limits, performance tracking

### SRN FitScore Methodology
Conservative evaluation across 7 weighted categories:

| Category | Weight | Description |
|----------|---------|-------------|
| 🎓 Education | 20% | Elite institutions, relevant degrees, certifications |
| 📈 Career Trajectory | 20% | Growth, ownership, increasing responsibility |
| 🏢 Company Relevance | 15% | High-caliber organizations, industry fit |
| ⏳ Tenure & Stability | 15% | 1.5-3 year averages, justified moves |
| 🎯 Core Skills | 20% | Mastery of mission-critical capabilities |
| 🌟 Bonus Signals | 5% | OSS, publications, speaking, founding |
| ❌ Red Flags | -15% | Dealbreakers, concerning patterns |

**Final Score Scale:**
- **8.5-10.0**: 🟢 STRONG HIRE - Exceptional candidate meeting elite standards
- **7.0-8.4**: 🟡 CONSIDER - Good candidate, requires additional evaluation  
- **5.5-6.9**: 🟠 WEAK - Below standards, significant concerns
- **0-5.4**: 🔴 NO HIRE - Does not meet minimum requirements

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

### Demo (No API Keys Required)
```bash
python3 demo_smart_evaluation.py
```

### Streamlit App
```bash
streamlit run streamlit_app.py
```

### Python Usage
```python
from advanced_sourcing_agent import AdvancedSourcingAgent

agent = AdvancedSourcingAgent()

job_description = """
Senior DevOps Engineer
San Francisco, California
Ivo AI is building tools to help every company make sense of their contracts.
Experience with Pulumi, Azure, GCP, Kubernetes, JavaScript
5+ years experience with Infrastructure as Code
"""

results = agent.search_candidates(job_description, num_candidates=10)

for candidate in results['candidates']:
    print(f"Candidate: {candidate['title']}")
    print(f"SRN Fit Score: {candidate['fit_score']}/10.0")
    print(f"Recommendation: {candidate['recommendation']}")
    print(f"Strengths: {candidate['smart_assessment']['evaluation']['strengths']}")
```

## 🏗 Architecture

### Core Components

1. **SmartContextDetector**
   - Industry pattern matching
   - Company type classification  
   - Role type and subtype detection
   - Technical vs non-technical role identification

2. **JobDescriptionAnalyzer**
   - Job family classification (11 categories)
   - Seniority level detection (4 levels)
   - Technical skills extraction (8 categories, 200+ technologies)
   - Location parsing
   - Leadership and remote eligibility assessment

3. **QueryGenerator**
   - Role-specific query templates
   - Dynamic placeholder replacement
   - Multiple search strategies per role
   - Query optimization and performance tracking

4. **SmartEvaluator**
   - Context-aware criteria generation
   - LLM-powered candidate assessment
   - Conservative scoring methodology
   - Elite institution and company recognition

5. **AdvancedSourcingAgent**
   - Orchestrates entire pipeline
   - Manages search execution
   - Deduplicates results
   - Performance analytics

### Supported Role Types

- **DevOps Engineer**: Infrastructure as Code, cloud platforms, CI/CD, monitoring
- **ML Engineer**: TensorFlow, PyTorch, production ML, model deployment
- **Software Engineer**: Full-stack, backend, frontend, mobile development
- **Tax Director**: CPA, public accounting, IRS representation, compliance
- **Data Scientist**: Analytics, machine learning, data engineering
- **Product Manager**: Roadmaps, user research, GTM strategy
- **And more...**

## 📊 Sample Results

### Job: Senior DevOps Engineer at Ivo AI

**Context Detected:**
- Industry: Tech
- Company Type: VC-backed Startup  
- Role Type: DevOps Engineer
- Role Subtype: Cloud Infrastructure

**Generated Queries:**
1. `site:linkedin.com/in/ ("DevOps Engineer" OR "Site Reliability Engineer") "San Francisco" "5+ years" (Pulumi OR GCP OR JavaScript)`
2. `site:linkedin.com/in/ "DevOps Engineer" (startup OR series) (Azure OR GCP) "Infrastructure as Code"`
3. `site:linkedin.com/in/ ("DevOps Engineer" OR "Infrastructure Engineer") (startup OR early stage)`

**Top Candidate Example:**
```
🎯 Senior DevOps Engineer at Google Cloud
💯 SRN Fit Score: 8.7/10.0
📋 Recommendation: 🟢 STRONG HIRE

Score Breakdown:
🎓 Education: 9.0/10 (Stanford CS)
📈 Career: 8.5/10 (Progressive growth)
🏢 Company: 9.5/10 (Google + Stripe)
⏳ Tenure: 8.0/10 (3+ years per role)
🎯 Skills: 9.0/10 (All core technologies)
🌟 Bonus: 3.0/5 (OSS contributions)
❌ Red Flags: 0.0
```

## 🎯 Intelligent Search Examples

The system generates context-aware search queries:

### DevOps Engineer (AI Startup)
```
Primary: site:linkedin.com/in/ ("DevOps Engineer" OR "SRE") "5+ years" (Pulumi OR Terraform)
AI Context: site:linkedin.com/in/ "DevOps Engineer" (LLM OR "Machine Learning") (Azure OR GCP)  
Startup: site:linkedin.com/in/ "Infrastructure Engineer" (startup OR "early stage")
```

### ML Engineer (Audio AI)
```
Primary: site:linkedin.com/in/ ("ML Engineer" OR "AI Engineer") (TensorFlow OR PyTorch)
Audio: site:linkedin.com/in/ "ML Engineer" ("speech recognition" OR "audio processing")
Production: site:linkedin.com/in/ "ML Engineer" ("production ML" OR "MLOps")
```

### Tax Director (CPA Firm)  
```
Primary: site:linkedin.com/in/ ("Tax Director" OR "Tax Manager") CPA "7+ years"
IRS: site:linkedin.com/in/ "Tax Director" ("IRS representation" OR "tax audit")
Public: site:linkedin.com/in/ "Tax Manager" ("public accounting" OR "Big 4")
```

## 🧬 Elite Hiring Standards

### Example: Senior DevOps Engineer

**Education Requirements:**
Bachelor's+ in Computer Science or equivalent infrastructure expertise from top-tier universities (MIT, Stanford, CMU, Berkeley, etc.)

**Core Skills (Mission-Critical):**
- Infrastructure as Code (Terraform, Pulumi, CloudFormation)
- Multi-tenant architecture design and implementation
- Incident response leadership and post-mortem ownership
- Scalability optimization for high-growth environments

**Domain Expertise:**
- Cloud platforms (AWS/GCP/Azure) with production experience
- Container orchestration (Kubernetes, Docker) at scale
- Monitoring/Observability stack design and implementation
- Security best practices and compliance frameworks

**Experience Markers:**
- Infrastructure ownership for 100+ services or high-scale deployments
- Uptime responsibility and SLA management experience
- Performance optimization delivering measurable improvements
- Cross-functional collaboration with engineering teams

**Company Preferences:**
- High-scale tech companies (1M+ users or $100M+ revenue)
- VC-backed startups with proven traction (Series A+)
- Infrastructure-heavy environments (fintech, healthcare, enterprise SaaS)

**Red Flags:**
- IT support or help desk background without infrastructure ownership
- No cloud platform experience or certifications
- Job hopping without increasing scope or impact
- Resume focused on tools rather than business outcomes

**Bonus Signals:**
- Open source infrastructure projects or contributions
- Technical blog posts or conference speaking on infrastructure topics
- Infrastructure certifications (AWS/GCP/Azure Professional level)
- Previous experience at infrastructure-focused companies

## 🔧 Configuration

### Query Templates
Customize search strategies in `QueryGenerator.query_templates`:

```python
"devops_engineer": {
    "primary": 'site:linkedin.com/in/ ("DevOps Engineer" OR "SRE") {location} {experience} {tech_stack}',
    "specialized": 'site:linkedin.com/in/ "DevOps Engineer" {company_context} {cloud_platforms}',
    "industry_specific": 'site:linkedin.com/in/ "Infrastructure Engineer" {industry_context}'
}
```

### Scoring Weights
Adjust evaluation weights in `SRNFitScoreEvaluator.weights`:

```python
weights = {
    "education": 0.20,
    "career_trajectory": 0.20,
    "company_relevance": 0.15,
    "tenure_stability": 0.15,
    "core_skills": 0.20,
    "bonus_signals": 0.05,
    "red_flags": -0.15
}
```

### Elite Institutions
Update recognition lists in `SRNFitScoreEvaluator.elite_institutions`:

```python
"universities": [
    "MIT", "Stanford", "CMU", "Berkeley", "Caltech", 
    "Harvard", "Princeton", "UIUC", "University of Washington"
],
"companies": {
    "tech": ["Google", "Apple", "Microsoft", "Amazon", "Meta", "Netflix"],
    "finance": ["Goldman Sachs", "Morgan Stanley", "JPMorgan"],
    "consulting": ["McKinsey", "Bain", "BCG"]
}
```

## 📈 Performance Features

- **Query Performance Tracking**: Success rates, result counts, timing
- **Deduplication**: URL-based candidate deduplication across queries  
- **Parallel Search Execution**: Multiple queries run simultaneously
- **Caching**: Results caching to avoid redundant API calls
- **Rate Limiting**: Respectful API usage patterns

## 🔮 Future Enhancements

- **Resume Integration**: Parse and evaluate full resume documents
- **Social Media Analysis**: GitHub, Twitter, personal websites  
- **Video Interview Scoring**: AI-powered interview assessment
- **Team Fit Analysis**: Cultural and working style compatibility
- **Salary Benchmarking**: Market rate analysis and recommendations
- **Diversity Scoring**: DE&I metrics and bias detection
- **Reference Network**: Mutual connections and endorsements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by elite hiring practices at top tech companies
- Built on the shoulders of open-source AI and search technologies
- Designed for recruiters who demand exceptional candidate quality

---

**Ready to find the top 1% of talent? Start sourcing smarter with SRN today!** 🚀
