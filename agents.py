import os
from dotenv import load_dotenv

from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from langchain.llms import Ollama

from tools import (
    get_client_transcript,
    get_pmbok_standards,
    save_interview_questions,
    create_project_workbook,
)


class PMAgents:

    def __init__(self):

        load_dotenv()

        self.OpenAI_GPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAI_GPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)

        self.Ollama = Ollama(model="llama3.1", base_url="http://localhost:11434")
        self.LMStudio = Ollama(model="llama3.1", base_url="http://localhost:11434")

        os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
        os.environ["OPENAI_API_KEY"] = "lm-studio"

    def project_manager(self):
        return Agent(
            role="Project Manager at Healthcare Facilitation Group (HFG)",
            backstory=dedent(
                """Veteran project manager with 15+ years of cross-industry experience. Expert in PMBOK-compliant workbooks, known for clear documentation that enhances team communication and project success"""
            ),
            goal=dedent(
                """Develop comprehensive, PMBOK-aligned project workbooks that effectively cover all elements of project management, tailored to meet unique client needs"""
            ),
            # llm=self.LMStudio,
        )

    def interviewing_agent(self):
        return Agent(
            role="Professional Interviewer",
            backstory=dedent(
                """Skilled interviewer adept at eliciting comprehensive project information through insightful, open-ended questions about risks, resources, and expectations"""
            ),
            goal=dedent(
                """Help clients articulate their vision and needs clearly, ensuring all essential project management aspects are covered during the interview process"""
            ),
            # llm=self.LMStudio,
        )

    def document_analyst(self):
        return Agent(
            role="Document Analysis Specialist",
            backstory=dedent(
                """Experienced analyst with keen eye for detail. Proficient in parsing complex documents, identifying key insights, and providing concise summaries to support project planning and execution"""
            ),
            goal=dedent(
                """Extract, analyze, and synthesize critical information from various project-related documents, ensuring comprehensive understanding and effective utilization of available data"""
            ),
            tools=[get_pmbok_standards, get_client_transcript],
            # llm=self.LMStudio,
        )

    def writing_agent(self):
        return Agent(
            role="Project Documentation Specialist",
            backstory=dedent(
                """Experienced in comprehensive project documentation. Expertly details scope, schedule, resources, risks, and stakeholder engagement. Delivers clear, concise, and structured workbooks for effective project management"""
            ),
            goal=dedent(
                """Create comprehensive, PMBOK-aligned project workbooks that ensure clarity and accountability throughout the project lifecycle."""
            ),
            tools=[save_interview_questions, create_project_workbook],
            # llm=self.LMStudio,
        )
