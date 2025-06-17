# (No code change, just move the file to the root directory.) 

from crewai import Crew, Agent, Task
from .tools.custom_tools import LinkedInSearchTool, CandidateEvaluatorTool
from .elite_evaluator import evaluate_candidate_gpt, generate_outreach_message_gpt

class RecruitmentCrew:
    def __init__(self):
        self.linkedin_search_tool = LinkedInSearchTool()
        self.candidate_evaluator_tool = CandidateEvaluatorTool()

    def recruitment_crew(self):
        # Define the agents
        researcher = Agent(
            role='LinkedIn Researcher',
            goal='Find qualified candidates on LinkedIn based on job requirements',
            backstory='Expert at finding and analyzing LinkedIn profiles to identify potential candidates',
            tools=[self.linkedin_search_tool],
            verbose=True
        )

        evaluator = Agent(
            role='Candidate Evaluator',
            goal='Evaluate candidates and determine their fit for the role',
            backstory='Experienced recruiter with deep knowledge of technical roles and requirements',
            tools=[self.candidate_evaluator_tool],
            verbose=True
        )

        # Define the tasks
        research_task = Task(
            description="""
            Search LinkedIn for potential candidates based on the following job requirements:
            - Role: {role}
            - Organization: {organization}
            - Location: {location}
            - Description: {description}
            
            Return a list of candidate profiles that match the requirements.
            """,
            expected_output="A list of candidate profiles that match the requirements.",
            agent=researcher
        )

        evaluation_task = Task(
            description="""
            Evaluate the candidates found by the researcher and determine their fit for the role.
            Consider:
            - Skills match
            - Experience level
            - Location compatibility
            - Overall fit score
            
            Return a detailed evaluation for each candidate.
            """,
            expected_output="A detailed evaluation for each candidate, including a fit score and rationale.",
            agent=evaluator
        )

        # Create the crew
        crew = Crew(
            agents=[researcher, evaluator],
            tasks=[research_task, evaluation_task],
            verbose=True
        )

        return crew 