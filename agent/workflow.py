from crewai import Crew, Process
from agent.agents import PMAgents
from agent.tasks import PMTasks


class PMCrew:
    def __init__(self, client_id):
        self.client_id = client_id

        # Create instances of the agents and tasks
        self.agents = PMAgents()
        self.tasks = PMTasks(client_id)

    def create_interview_questions(self, onboarding_form_response):

        # Assign agents to variables
        interviewing_agent = self.agents.interviewing_agent()
        writing_agent = self.agents.writing_agent()

        # Assign tasks to agents
        create_interview_questions = self.tasks.create_interview_questions(
            agent=interviewing_agent,
            onboarding_form_response=onboarding_form_response,
        )
        save_interview_questions = self.tasks.save_interview_questions(
            agent=writing_agent, title="First Interviewing Questions"
        )

        # Define Crew
        crew = Crew(
            agents=[
                interviewing_agent,
                writing_agent,
            ],
            tasks=[
                create_interview_questions,
                save_interview_questions,
            ],
            process=Process.sequential,
            memory=True,
            verbose=True,
        )

        result = crew.kickoff()
        return result

    def update_project_workbook(self, interview_calls_transcript):

        # Assign onboarding form response to self
        self.interview_calls_transcript = interview_calls_transcript

        # Assign agents to variables
        project_manager = self.agents.project_manager()
        interviewing_agent = self.agents.interviewing_agent()
        document_analyst = self.agents.document_analyst()
        writing_agent = self.agents.writing_agent()

        # Create tasks and assign agents to them
        create_project_workbook_elements = self.tasks.create_project_workbook_elements(
            agent=project_manager, interview_calls_transcript=interview_calls_transcript
        )
        update_project_workbook_elements = self.tasks.update_project_workbook_elements(
            agent=writing_agent
        )
        create_follow_up_interview_questions = (
            self.tasks.create_follow_up_interview_questions(agent=interviewing_agent)
        )
        save_interview_questions = self.tasks.save_interview_questions(
            agent=writing_agent, title="Recommended Follow-Up Questions"
        )

        # Define Crew
        crew = Crew(
            agents=[project_manager, writing_agent, interviewing_agent],
            tasks=[
                create_project_workbook_elements,
                update_project_workbook_elements,
                create_follow_up_interview_questions,
                save_interview_questions,
            ],
            process=Process.sequential,
            memory=True,
            verbose=True,
        )

        result = crew.kickoff()
        return result

    def test_crew(self, onboarding_form_response):

        # Assign agents to variables
        interviewing_agent = self.agents.interviewing_agent()
        writing_agent = self.agents.writing_agent()

        # Assign tasks to agents
        create_interview_questions = self.tasks.create_interview_questions(
            agent=interviewing_agent,
            onboarding_form_response=onboarding_form_response,
        )
        save_interview_questions = self.tasks.save_interview_questions(
            agent=writing_agent, title="First Interviewing Questions"
        )

        crew = Crew(
            agents=[
                interviewing_agent,
                writing_agent,
            ],
            tasks=[
                create_interview_questions,
                save_interview_questions,
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,
            # long_term_memory=EnhanceLongTermMemory(
            #     storage=LTMSQLiteStorage(
            #         db_path="/my_data_dir/my_crew1/long_term_memory_storage.db"
            #     )
            # ),
            # short_term_memory=EnhanceShortTermMemory(
            #     storage=CustomRAGStorage(
            #         crew_name="my_crew",
            #         storage_type="short_term",
            #         data_dir="//my_data_dir",
            #         model=embedder["model"],
            #         dimension=embedder["dimension"],
            #     ),
            # ),
            # entity_memory=EnhanceEntityMemory(
            #     storage=CustomRAGStorage(
            #         crew_name="my_crew",
            #         storage_type="entities",
            #         data_dir="//my_data_dir",
            #         model=embedder["model"],
            #         dimension=embedder["dimension"],
            #     ),
            # ),
        )
