import io
from dotenv import load_dotenv
import streamlit as st
from crew_workflow import PMCrew


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


def get_interview_calls_transcript():
    """
    Read the contents of multiple uploaded text files and combine them with headings.

    Returns:
    str or None: A single string containing all file contents with headings if successful, None otherwise
    """
    # Add a subheader
    st.subheader("Interview Call Transcripts")

    # File uploader for multiple files
    uploaded_files = st.file_uploader(
        "Upload the transcripts of the interview calls",
        type="txt",
        accept_multiple_files=True,
    )

    if uploaded_files:
        combined_contents = []
        for i, uploaded_file in enumerate(uploaded_files, 1):
            try:
                # Check if the file is a text file
                if uploaded_file.type == "text/plain":
                    # Read the contents of the file
                    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                    content = stringio.read()

                    # Add heading and content to the list
                    heading = f"******** MEETING TRANSCRIPT {i} ********\n"
                    combined_contents.append(heading + content + "\n\n")
                else:
                    st.error(
                        f"Please upload a text file. '{uploaded_file.name}' is not a text file."
                    )
            except Exception as e:
                st.error(
                    f"An error occurred while reading the file '{uploaded_file.name}': {str(e)}"
                )

        if combined_contents:
            return "".join(combined_contents)
        else:
            return None
    return None


def main():

    # Load environment variables
    load_dotenv()

    st.set_page_config(page_title="Project Management MVP", layout="wide")
    st.markdown(
        "<h1 style='text-align: center;'>Project Management MVP</h1>",
        unsafe_allow_html=True,
    )

    # Allow users select a client
    client_id = "new_client"

    onboarding_tab, interview_tab, results_tab = st.tabs(
        ["Onboarding", "Interview", "Results"]
    )

    with onboarding_tab:
        # Get the onboarding form response
        onboarding_form_response = get_onboarding_form_response()

        if onboarding_form_response:

            # Display file contents
            st.text_area(
                "Response",
                onboarding_form_response,
                height=400,
                label_visibility="hidden",
            )

            if st.button("Create Interview Questions"):

                with st.spinner("Creating interview questions"):

                    # Create an instance of PMCrew
                    pm_crew = PMCrew(client_id=client_id)
                    # Create and add interview questions
                    result = pm_crew.create_interview_questions(
                        onboarding_form_response
                    )

                st.success(result)

    with interview_tab:
        # Get the initial interview call transcript
        interview_calls_transcript = get_interview_calls_transcript()

        if interview_calls_transcript:

            # Display file contents
            st.text_area(
                "Transcript",
                interview_calls_transcript,
                height=400,
                label_visibility="hidden",
            )

            if st.button("Populate Workbook"):

                with st.spinner("Updating project workbook"):

                    # Create an instance of PMCrew
                    pm_crew = PMCrew(client_id=client_id)
                    # Populate project workbook
                    result = pm_crew.update_project_workbook(interview_calls_transcript)

                st.success(result)

    with results_tab:
        if "logs" not in st.session_state:
            st.session_state["logs"] = {}

        def render_results(data):
            rendered = []
            for key, value in data.items():
                # Add the key as a bold heading
                key = key.upper()
                rendered.append(f"**{key}**")

                # Process the value
                if isinstance(value, str):
                    # If it's a string, add it with "- " prefix
                    rendered.append(f"- {value}")
                elif isinstance(value, list):
                    # If it's a list, format each item with "- " prefix
                    for item in value:
                        rendered.append(f"- {item}")
                else:
                    # If it's neither string nor list, convert to string and add "- " prefix
                    rendered.append(f"- {str(value)}")

                # Add a blank line after each key-value pair
                rendered.append("")

            # Join all parts with newlines
            return "\n".join(rendered)

        st.write(render_results(st.session_state["logs"]))


if __name__ == "__main__":
    main()
