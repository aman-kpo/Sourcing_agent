from typing import List, Dict
import json
from dataclasses import dataclass
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class JobContext(BaseModel):
    industry: str = Field(description="The industry of the company (e.g., Tech, Healthcare, Finance)")
    company_type: str = Field(description="The type of company (e.g., Startup, Enterprise, Agency)")
    role_type: str = Field(description="The main role type (e.g., Software Engineer, Product Manager)")
    role_subtype: str = Field(description="The specific subtype of the role (e.g., Frontend, Backend, Full-stack)")
    critical_skills: List[str] = Field(description="List of critical skills required for the role")
    education_requirements: List[str] = Field(description="List of education requirements")
    experience_requirements: List[str] = Field(description="List of experience requirements")
    company_preferences: List[str] = Field(description="Preferred types of companies in candidate's background")
    location_preferences: List[str] = Field(description="Preferred locations for candidates")
    bonus_signals: List[str] = Field(description="Bonus signals that would make a candidate stand out")
    red_flags: List[str] = Field(description="Red flags that would disqualify a candidate")

class JobContextExtractor:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0
        )
        self.parser = PydanticOutputParser(pydantic_object=JobContext)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert recruiter and hiring manager. Your task is to analyze job descriptions and extract structured hiring criteria.
            
            Follow these guidelines:
            1. Be extremely selective and maintain high standards
            2. Focus on elite candidates who would be in the top 1% of their field
            3. Consider both technical skills and soft skills
            4. Look for signals of excellence and achievement
            5. Identify potential red flags
            
            Extract the following information:
            - Industry and company type
            - Role type and subtype
            - Critical skills (focus on what they must be able to DO, not just tools they know)
            - Education requirements (be specific about degrees and institutions)
            - Experience requirements (focus on outcomes and achievements)
            - Company preferences (e.g., FAANG, YC startups, Fortune 500)
            - Location preferences
            - Bonus signals (e.g., patents, publications, open source contributions)
            - Red flags (e.g., job hopping, lack of ownership)
            
            Format the output as a JSON object matching the JobContext schema."""),
            ("user", "Analyze this job description and extract the hiring criteria:\n\n{job_description}"),
        ])

    def extract_context(self, job_description: str) -> JobContext:
        """Extract structured hiring criteria from a job description"""
        # Format the prompt with the job description
        formatted_prompt = self.prompt.format_messages(job_description=job_description)
        
        # Get response from GPT-4
        response = self.llm(formatted_prompt)
        
        # Parse the response into a JobContext object
        try:
            context = self.parser.parse(response.content)
            return context
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Raw response: {response.content}")
            raise

# Example usage
if __name__ == "__main__":
    extractor = JobContextExtractor()
    
    # Example job description
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
    
    # Extract context
    context = extractor.extract_context(job_description)
    
    # Print results
    print(json.dumps(context.dict(), indent=2)) 