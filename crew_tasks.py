from crewai import Task
from textwrap import dedent


from crew_tools import PMTools


class PMTasks:
    def __init__(self, client_id):

        # Create an instance of the PMTools
        self.pm_tools = PMTools(client_id=client_id)

    def __project_workbook_elements(self):
        workbook_elements = [
            "Project Description",
            "Key Deliverables",
            "High-Level Risks",
            "High-Level Milestones",
            "Budget Summary",
            "Stakeholders",
            "Project Plan Version",
            "Approval Date",
            "Subsidiary Plans Included",
            "Current State of Strategy",
            "Current State of People",
            "Current State of Products",
            "Current State of Processes",
            "Scope Management Approach",
            "Scope Statement",
            "Scope Validation",
            "Scope Control",
            "Detailed Scope Description",
            "Deliverables",
            "Exclusions",
            "Constraints",
            "Assumptions",
            "Approval Date",
            "Key Milestones",
        ]

        return ", ".join(workbook_elements)

    def __tip_section(self):
        return "If you do your BEST WORK, you'll get a $10,000 bonus!"

    def create_interview_questions(self, agent, onboarding_form_response):
        return Task(
            description=dedent(
                f"""
            **Task**: To create a short list of interviewing questions to ask a client during the first meeting
            **Description**: Create a concise set of 5-7 open-ended questions for HFG to ask a client during their initial meeting. These carefully crafted questions should efficiently gather key project details to populate a project workbook, building on information already provided in the onboarding form.

            Key objectives:
            1. Limit the list to 5-7 impactful questions
            2. Capture essential project elements not covered in the onboarding form
            3. Allow for detailed, informative responses
            4. Enable HFG to comprehensively fill out the project workbook
            5. Avoid repetition of information from the onboarding form

            The goal is to maximize information gathering with minimal questioning, ensuring a focused and productive initial client meeting.

            **Elements of Project Workbook**: {self.__project_workbook_elements()}

            **Onboarding Form response**:
            {onboarding_form_response}
            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="A list of questions to ask during an interview",
            agent=agent,
        )

    def save_interview_questions(self, agent, title):
        return Task(
            description=dedent(
                f"""
            **Task**: To save a list of interviewing questions for a client
            **Description**: Save a list of interviewing questions for a client. The title should be {title}

            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="Interview questions saved successfully!",
            agent=agent,
            tools=[self.pm_tools.save_interview_questions],
        )

    def create_project_workbook_elements(self, agent, interview_calls_transcript):
        return Task(
            description=dedent(
                f"""
            **Task**: To create a project workbook for a client
            **Description**: Develop a focused project workbook based solely on the information provided in the client meeting transcripts. This workbook will adhere to PMBOK standards but will only include elements explicitly discussed or implied in the meetings. Any standard PMBOK components not covered in the transcripts will be omitted, ensuring the workbook accurately reflects the current state of project planning with the client. The workbook will serve as a clear, concise document capturing agreed-upon project elements, avoiding assumptions about undiscussed aspects. This approach ensures the workbook is a true representation of the client's understanding and agreements made during the recorded meetings


            **Elements of Project Workbook**: {self.__project_workbook_elements()}

            **Interview Calls Transcript**:
            {interview_calls_transcript}

            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="A structured text with the project workbook elements and their details",
            agent=agent,
        )

    def update_project_workbook_elements(self, agent):
        return Task(
            description=dedent(
                f"""
            **Task**: To update the details of a project workbook for a client
            **Description**: Update the details of a client's project workbook based on the new fields created and ensure all information is accurate.

            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="Workbook created successfully!",
            agent=agent,
            tools=[self.pm_tools.create_project_workbook_elements],
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

    def create_follow_up_interview_questions(self, agent):
        return Task(
            description=dedent(
                f"""
            **Task**: To create a short list of interviewing questions to ask a client during a follow-up meeting
            **Description**: Create a concise set of 5-7 open-ended questions for HFG to ask a client during a followup meeting. These carefully crafted questions should efficiently gather key project details to populate the missing elements in project workbook.

            Key objectives:
            1. Limit the list to 5-7 impactful questions
            2. Capture essential project elements not already populated in the project workbook
            3. Allow for detailed, informative responses
            4. Enable HFG to comprehensively fill out the project workbook

            **Elements of Project Workbook**: {self.__project_workbook_elements()}

            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="A list of questions to ask during a follow up interview",
            agent=agent,
        )
