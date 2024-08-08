from crewai import Task
from textwrap import dedent


class PMTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, you'll get a $10,000 bonus!"

    def create_interviewing_questions(self, agent):
        return Task(
            description=dedent(
                f"""
            **Task**: To create a list of interviewing questions to ask a client during the first meeting
            **Description**: Create a list of interviewing questions that HFG (your company) can ask a client during the first meeting to capture all relevant details about a project and have enough information to be able to create a complete project workbook. The questions should be open-ended and designed to gather as much information as possible about the client's needs, preferences, and expectations.

            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="A list of questions to ask during an interview",
            agent=agent,
        )

    def create_project_workbook(self, agent):
        return Task(
            description=dedent(
                f"""
            **Task**: To create a project workbook for a client
            **Description**: Create a comprehensive project workbook for a client, in accordance with the PMBOK Standard .

            **Note**: {self.__tip_section()}
        """
            ),
            expected_output="Workbook created successfully!",
            agent=agent,
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

    def gather_city_info(self, agent, city, travel_dates, interests):
        return Task(
            description=dedent(
                f"""
                    **Task**:  Gather In-depth City Guide Information
                    **Description**: Compile an in-depth guide for the selected city, gathering information about 
                        key attractions, local customs, special events, and daily activity recommendations. 
                        This guide should provide a thorough overview of what the city has to offer, including 
                        hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high-level costs.

                    **Parameters**: 
                    - Cities: {city}
                    - Interests: {interests}
                    - Travel Date: {travel_dates}

                    **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
        )
