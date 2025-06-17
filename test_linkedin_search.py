from dotenv import load_dotenv
load_dotenv()

from ai_outreach_crew.tools.custom_tools import LinkedInSearchTool

if __name__ == "__main__":
    tool = LinkedInSearchTool()
    job_requirements = "Sr Devops Engineer san francisco"
    result = tool._run(job_requirements)
    print("LinkedInSearchTool result:", result)
