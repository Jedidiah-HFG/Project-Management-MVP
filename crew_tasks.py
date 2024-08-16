from crewai import Task
from textwrap import dedent


from crew_tools import PMTools


class PMTasks:
    def __init__(self, client_id):

        # Create an instance of the PMTools
        self.pm_tools = PMTools(client_id=client_id)

    def __project_workbook_elements(self):
        return "Project Description, Key Deliverables, High-Level Risks, High-Level Milestones, Budget Summary, Stakeholders."

    def __tip_section(self):
        return "If you do your BEST WORK, you'll get a $10,000 bonus!"

    def create_interview_questions(self, agent, onboarding_form_response):
        return Task(
            description=dedent(
                f"""
            **Task**: To create a short list of interviewing questions to ask a client during the first meeting
            **Description**: Create a list of open-ended interviewing questions that HFG (your company) can ask a client to capture specific details about a project and have enough information to be able to fill a project workbook. You should ask as little questions as possible and the questions don't have to be direct but they should try to capture as much elements of the workbook as possible.

            The client has already filled an initial onboarding form.

            **Elements of Project Workbook**: {self.__project_workbook_elements()}

            **Onboarding Form response**:
            {onboarding_form_response}
            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="A list of questions to ask during an interview",
            agent=agent,
        )

    def save_interview_questions(self, agent):
        return Task(
            description=dedent(
                f"""
            **Task**: To save a list of interviewing questions for a client
            **Description**: Save a list of interviewing questions for a client.

            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="Interview questions saved successfully!",
            agent=agent,
            tools=[self.pm_tools.save_interview_questions],
        )

    def update_project_workbook(self, agent):
        return Task(
            description=dedent(
                f"""
            **Task**: To create a project workbook for a client
            **Description**: Create a comprehensive project workbook for a client, in accordance with the PMBOK Standard.

            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="Workbook created successfully!",
            agent=agent,
            tools=[self.pm_tools.create_project_workbook],
        )

    def answer_question_from_transcript(self, agent, question):
        return Task(
            description=dedent(
                f"""
            **Task**: To answer questions about a project based on a call transcript with a client
            **Description**: Create a comprehensive project workbook for a client, in accordance with the PMBOK Standard .

            **Note**: {self.__tip_section()}

            **Question**: {question}
        """
            ),
            expected_output="A through answer to the question based on the call transcript",
            agent=agent,
        )
