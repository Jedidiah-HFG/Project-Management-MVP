from pydantic import BaseModel, Field
from langchain.tools import tool
from crewai_tools import TXTSearchTool, PDFSearchTool


class CrewAITools:

    # Define file path
    call_transcript_path = (
        "data/Client Script for POC (2024-06-26 10_34 GMT-3) - Transcript.txt"
    )
    get_client_transcript = TXTSearchTool(txt=call_transcript_path)
    get_pmbok_standards = PDFSearchTool(pdf="data/PMBOK Guide.pdf")


# Define a Pydantic model for the tool's input parameters
class CreateProjectWorkbookInput(BaseModel):
    client_name: str = Field(
        description="The name of the client to create a workbook for"
    )
    project_title: float = Field(
        description="The title of the project to create a workbook for"
    )
    project_description: float = Field(description="The description of the project")


@tool(
    "create_project_workbook",
    args_schema=CreateProjectWorkbookInput,
    return_direct=True,
)
def create_project_workbook(
    client_name: str, project_title: str, project_description: str
) -> str:
    """
    Creates a new project workbook for a client

    Parameters:
    - client_name (str): The name of the client to create a workbook for.
    - project_title (float): The title of the project to create a workbook for.
    - project_description (float): The description of the project.

    Returns:
    - A string representation of the result.
    """

    # Define the output file name
    output_file_path = f"{client_name}.txt"

    # Open the file in append mode ('a') to add the output to the end of the file
    with open(output_file_path, "a") as file:
        file.write(f"Project Title: {project_title}\n")
        file.write(f"Project Description: {project_description}\n\n")

    return "Workbook created successfully!"
