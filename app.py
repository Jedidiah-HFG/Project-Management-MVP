import json
from dotenv import load_dotenv
import streamlit as st
from notion import NotionAPI

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Project Management MVP", layout="wide")
st.markdown(
    "<h1 style='text-align: center;'>Project Management MVP</h1>",
    unsafe_allow_html=True,
)

# Load data
with open("sample_data.json", "r") as f:
    sample_data = json.load(f)
with open("clients.json", "r") as f:
    all_clients_data = json.load(f)

# Allow users select a client
client_id = st.selectbox("Select a client", all_clients_data.keys())
# Get the data for the specified client
client_data = all_clients_data[client_id]
# Create a notion api
notion_api = NotionAPI(client_id=client_id)

# Initialize empty states
if "interview_question" not in st.session_state:
    st.session_state["interview_question"] = []

if st.button("Create Interview Questions"):

    with st.spinner("Creating interviewing questions"):
        # Read interviewing questions
        interview_questions = sample_data["interview_question"]

    # Save the interview questions to session state
    st.session_state["interview_question"] = interview_questions

    with st.spinner("Saving interviewing questions"):
        # Generate interview questions body
        interview_questions_body = notion_api.generate_interview_questions_body(
            questions=sample_data["interview_question"]
        )
        # Add interview_questions_body to notion
        notion_api.add_content_to_page(children=interview_questions_body)

    st.success("Interviewing questions saved to Notion")


if "interview_question" in st.session_state:

    with st.expander("Interviewing Questions"):
        # Display the interview questions
        st.write("- " + "\n\n- ".join(st.session_state["interview_question"]))

    # Allow user to upload their call transcript
    st.file_uploader("Upload your call transcript with the client")

    # Get the path for the call transcript
    file_path = client_data["call_transcript"]

    # Open the file in read mode
    with open(file_path, "r") as file:
        # Read the contents of the file
        file_contents = file.read()

    with st.expander("Initial Call Transcript"):
        # Display the contents of the file
        st.text(file_contents)


if st.button("Create Project Workbook"):

    with st.spinner("Creating project workbook"):
        # Read project workbook
        project_workbook = sample_data
        del project_workbook["interview_question"]

    # Save the project workbook to session state
    st.session_state["project_workbook"] = project_workbook

    with st.spinner("Saving project workbook"):
        # Generate project workbook body
        project_workbook_body = notion_api.generate_project_workbook_body(
            project_workbook
        )
        # Add project workbook to notion
        notion_api.add_content_to_page(children=project_workbook_body)

    st.success("Project workbook saved to Notion")
