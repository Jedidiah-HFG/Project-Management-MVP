from crewai import Crew
from agents import PMAgents
from tasks import PMTasks


class PMCrew:
    def __init__(self, client_name, question):
        self.client_name = client_name
        self.question = question

    def run(self):

        # Create instances of the agents and tasks
        agents = PMAgents()
        tasks = PMTasks()

        # Assign agents to variables
        project_manager = agents.project_manager()
        interviewing_agent = agents.interviewing_agent()
        document_analyst = agents.document_analyst()
        writing_agent = agents.writing_agent()

        # Create tasks and assign agents to them
        create_interview_questions = tasks.create_interview_questions(
            agent=interviewing_agent
        )
        save_interview_questions = tasks.save_interview_questions(agent=writing_agent)
        create_project_workbook = tasks.create_project_workbook(
            agent=writing_agent,
        )

        answer_question_from_transcript = tasks.answer_question_from_transcript(
            agent=project_manager, question=self.question
        )

        # Define Crew
        crew = Crew(
            agents=[
                project_manager,
                interviewing_agent,
                document_analyst,
                writing_agent,
            ],
            tasks=[
                create_interview_questions,
                save_interview_questions,
                create_project_workbook,
                answer_question_from_transcript,
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":

    client_name = input("What is the client name?")
    question = input("What questions do you have?")

    pm_crew = PMCrew(client_name, question)

    result = pm_crew.run()

    print("\n\n################################################\n")
    print(result)
