from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from ai_outreach_crew.tools.custom_tools import pse, send_emails
from crewai_tools import WebsiteSearchTool, SerperDevTool

web_search_tool = WebsiteSearchTool(search_query="https://bluegrid.energy/")
serper_dev_tool = SerperDevTool()
# scraper_tool = ScrapeWebsiteTool(
#     website_url="""site:ca.linkedin.com/in ("Calgary * Canada") AND (Java AND Hibernate) AND (Spring OR MySQL)"""
# )
pse_tool = pse
email_tool = send_emails


@CrewBase
class RecruitmentCrew:
    """Recruitment Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        # self.LLM = Ollama(model="llama3")
        self.LLM = ChatGroq(temperature=0.6, model_name="llama3-8b-8192")

    #################################################################
    # Agents:
    #################################################################

    @agent
    def requirement_specification_agent(self) -> Agent:
        """Agent for gathering requirements and drafting a job advertisement"""

        return Agent(
            config=self.agents_config["requirement_specification_agent"],
            llm=self.LLM,
            tools=[web_search_tool],
            # cache=True,
        )

    @agent
    def talent_acquisition_agent(self) -> Agent:
        """Agent for scraping the web and obtaining LinkedIn profiles of relevant individuals"""
        return Agent(
            config=self.agents_config["talent_acquisition_agent"],
            llm=self.LLM,
            tools=[web_search_tool, pse_tool],
            # cache=True,
        )

    @agent
    def outreach_agent(self) -> Agent:
        """Agent for sending out job advertisements to applicable individuals and invite them to apply"""
        return Agent(
            config=self.agents_config["outreach_agent"],
            llm=self.LLM,
            tools=[email_tool],
        )

    #################################################################
    # Tasks:
    #################################################################

    @task
    def craft_job_ad_task(self) -> Task:
        """Task for crafting a job advertisement"""
        return Task(
            config=self.tasks_config["craft_job_ad_task"],
            agent=self.requirement_specification_agent(),
        )

    @task
    def talent_acquisition_task(self) -> Task:
        """Task for obtaining a list of individuals whose profiles are relevant to the job advertisement"""
        return Task(
            config=self.tasks_config["talent_acquisition_task"],
            agent=self.talent_acquisition_agent(),
            # context=[self.craft_job_ad_task],
        )

    def outreach_task(self) -> Task:
        """Task for sending out job advertisements to applicable individuals and invite them to apply"""
        return Task(
            config=self.tasks_config["outreach_task"],
            agent=self.outreach_agent(),
            # context=[self.craft_job_ad_task, self.talent_acquisition_task],
        )

    #################################################################
    # Crew:
    #################################################################

    @crew
    def recruitment_crew(self) -> Crew:
        """Crew for recruiting individuals for opening(s) in an organization"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
            share_crew=False,
        )
