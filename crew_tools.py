from pydantic import BaseModel, Field
from typing import List, Dict
from langchain.tools import tool

# from crewai_tools import TXTSearchTool, PDFSearchTool
from notion import Notion


class PMTools:

    def __init__(self, client_id):

        # Create an instance of notion
        PMTools.notion = Notion(client_id=client_id)

        # Define langchain tools
        self.get_client_transcript = None  # TXTSearchTool(txt="data/Client Script for POC (2024-06-26 10_34 GMT-3) - Transcript.txt")
        self.get_pmbok_standards = None  # PDFSearchTool(pdf="data/PMBOK Guide.pdf")

    class SaveInterviewQuestionInput(BaseModel):
        interview_questions: List[str] = Field(
            description="A list of interview questions for the project"
        )

    @tool(
        "save_interview_questions",
        args_schema=SaveInterviewQuestionInput,
        return_direct=True,
    )
    def save_interview_questions(interview_questions: List[str]) -> str:
        """
        Saves the interviewing questions for a client

        Parameters:
        - interview_questions (list[str]): The list of interview questions for the project.

        Returns:
        - A string representation of the result of the process.
        """

        try:
            # Generate the body of the interview questions
            children_body = PMTools.notion.create_toggleable_notion_block(
                title="Interview Questions", content=interview_questions
            )
            # Add the content to the page
            PMTools.notion.add_content_to_page(children=children_body)
            return "Interviewing questions saved successfully!"

        except Exception as e:
            return f"An error occurred while saving interview questions: {e}"

    class CreateProjectWorkbookInput(BaseModel):
        workbook_contents: Dict = Field(
            description="The contents of the project workbook. The keys represent the elements of the workbook, and the values are the details of the elements"
        )

    @tool(
        "create_project_workbook",
        args_schema=CreateProjectWorkbookInput,
        return_direct=True,
    )
    def create_project_workbook_elements(workbook_contents: Dict) -> str:
        """
        Creates a new project workbook for a client

        Parameters:
        - workbook_contents (dict): The contents of the project workbook. The keys represent the elements of the workbook, and the values are the details of the elements.

        Returns:
        - A string representation of the result.
        """

        try:
            # Generate the body of the interview questions
            children_body = PMTools.notion.generate_project_workbook_body(
                workbook_contents=workbook_contents
            )
            # Add the content to the page
            PMTools.notion.add_content_to_page(children=children_body)
            return "Workbook created successfully!"

        except Exception as e:
            return f"An error occurred while saving interview questions: {e}"
