import io
from dotenv import load_dotenv
import streamlit as st
from crew_workflow import PMCrew


# Load environment variables
load_dotenv()

st.set_page_config(page_title="Project Management MVP", layout="wide")
st.markdown(
    "<h1 style='text-align: center;'>Project Management MVP</h1>",
    unsafe_allow_html=True,
)


def get_onboarding_form_response():
    """
    Read the contents of an uploaded text file.

    Returns:
    str or None: The contents of the file as a string if successful, None otherwise
    """
    # Add a subheader
    st.subheader("Onboarding Form Response")

    # File uploader
    uploaded_file = st.file_uploader("Upload the onboarding form response", type="txt")

    if uploaded_file is not None:
        try:
            # Check if the file is a text file
            if uploaded_file.type == "text/plain":
                # Read the contents of the file
                stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                file_contents = stringio.read()
                return file_contents
            else:
                st.error("Please upload a text file.")
                return None
        except Exception as e:
            st.error(f"An error occurred while reading the file: {str(e)}")
            return None
    return None


def get_interview_call_transcript():
    """
    Read the contents of an uploaded text file.

    Returns:
    str or None: The contents of the file as a string if successful, None otherwise
    """
    # Add a subheader
    st.subheader("Interview Call Transcript")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload the transcript of the interview call", type="txt"
    )

    if uploaded_file is not None:
        try:
            # Check if the file is a text file
            if uploaded_file.type == "text/plain":
                # Read the contents of the file
                stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                file_contents = stringio.read()
                return file_contents
            else:
                st.error("Please upload a text file.")
                return None
        except Exception as e:
            st.error(f"An error occurred while reading the file: {str(e)}")
            return None
    return None


def main():

    # Allow users select a client
    client_id = "new_client"

    # Create an instance of PMCrew
    pm_crew = PMCrew(client_id=client_id)

    onboarding_tab, interview_tab, follow_up_tab = st.tabs(
        ["Onboarding", "Interview", "Follow-up"]
    )

    with onboarding_tab:
        # Get the onboarding form response
        onboarding_form_response = get_onboarding_form_response()

        if onboarding_form_response is None:
            st.stop()

        # Display file contents
        st.text_area(
            "Response",
            onboarding_form_response,
            height=400,
            label_visibility="hidden",
        )

        if st.button("Create Interview Questions"):

            with st.spinner("Creating interview questions"):
                # Create and add interview questions
                result = pm_crew.create_interview_questions(onboarding_form_response)

            st.success(result)

    with interview_tab:
        # Get the initial interview call transcript
        interview_call_transcript = get_interview_call_transcript()

        if interview_call_transcript is None:
            st.stop()

        # Display file contents
        st.text_area(
            "Transcript",
            interview_call_transcript,
            height=400,
            label_visibility="hidden",
        )

        if st.button("Populate Workbook"):

            with st.spinner("Updating project workbook"):
                # Populate project workbook
                result = pm_crew.update_project_workbook(interview_call_transcript)

            st.success(result)


if __name__ == "__main__":
    main()


quit()


if True:

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
