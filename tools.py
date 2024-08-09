from pydantic import BaseModel, Field
from typing import List
from langchain.tools import tool
from crewai_tools import TXTSearchTool, PDFSearchTool
from notion import NotionAPI


# Define file path
_call_transcript_path = (
    "data/Client Script for POC (2024-06-26 10_34 GMT-3) - Transcript.txt"
)
get_client_transcript = TXTSearchTool(txt=_call_transcript_path)
get_pmbok_standards = PDFSearchTool(pdf="data/PMBOK Guide.pdf")


class CreateProjectWorkbookInput(BaseModel):
    project_title: float = Field(
        description="The title of the project to create a workbook for"
    )
    project_description: float = Field(description="The description of the project")


@tool(
    "create_project_workbook",
    args_schema=CreateProjectWorkbookInput,
    return_direct=True,
)
def create_project_workbook(project_title: str, project_description: str) -> str:
    """
    Creates a new project workbook for a client

    Parameters:
    - project_title (float): The title of the project to create a workbook for.
    - project_description (float): The description of the project.

    Returns:
    - A string representation of the result.
    """

    # Define the output file name
    output_file_path = "test.txt"

    # Open the file in append mode ('a') to add the output to the end of the file
    with open(output_file_path, "a") as file:
        file.write(f"Project Title: {project_title}\n")
        file.write(f"Project Description: {project_description}\n\n")

    return "Workbook created successfully!"


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
    Creates a new project workbook for a client

    Parameters:
    - project_title (float): The title of the project to create a workbook for.
    - project_description (float): The description of the project.

    Returns:
    - A string representation of the result.
    """

    try:
        # Create a NotionAPI instance for the client
        notion_api = NotionAPI(client_id="Dan Roberts")

        # Generate the body of the interview questions
        children_body = notion_api.generate_interview_questions_body(
            questions=interview_questions
        )
        # Add the content to the page
        notion_api.add_content_to_page(children=children_body)
        return "Workbook created successfully!"

    except Exception as e:
        return f"An error occurred while saving interview questions: {e}"
