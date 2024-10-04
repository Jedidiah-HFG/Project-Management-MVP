from pydantic import BaseModel, Field
from typing import List, Dict

from crewai_tools import tool, PDFSearchTool
from langchain.tools import tool
from notion.notion import Notion


class PMTools:

    # Define pmbok scrape tools
    get_pmbok_standards = PDFSearchTool(
        pdf="data/PMBOK Guide.pdf",
        config=dict(
            llm=dict(
                provider="openai",
                config=dict(
                    model="gpt-4o-mini",
                    # temperature=0.5,
                    # top_p=1,
                    # stream=true,
                ),
            ),
            embedder=dict(
                provider="openai",
                config=dict(
                    model="gpt-4o-mini",
                ),
            ),
        ),
    )

    def __init__(self, client_id):

        # Create an instance of notion
        PMTools.notion = Notion(client_id=client_id)

    class SaveInterviewQuestionInput(BaseModel):
        title: str = Field(description="The title of the interview questions")
        interview_questions: List[str] = Field(
            description="A list of interview questions on the project"
        )

    @tool(
        "save_interview_questions",
        args_schema=SaveInterviewQuestionInput,
        return_direct=True,
    )
    def save_interview_questions(title: str, interview_questions: List[str]) -> str:
        """
        Saves the interviewing questions for a client.

        Parameters:
        - title str: The title of the interview questions.
        - interview_questions (list[str]): The list of interview questions on the project.

        Returns:
        - A string representation of the result of the process.
        """

        try:
            # Add toggleable Notion block with the interview questions
            PMTools.notion.add_toggleable_notion_block(
                title=title, content=interview_questions
            )
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
        Creates a new project workbook for a client.

        Parameters:
        - workbook_contents (dict): The contents of the project workbook.
        Keys are strings representing workbook sections/elements.
        Values are either strings or lists of strings with section details.

        Returns:
        - A string representation of the result.
        """

        try:
            # Update the project workbook
            PMTools.notion.update_project_workbook(workbook_contents=workbook_contents)
            return "Workbook created successfully!"

        except Exception as e:
            return f"An error occurred while saving interview questions: {e}"
