import os
import json
import requests


class NotionAPI:

    def __init__(self, client_id: str):

        # Retrieve the Notion API key from environment variable
        NOTION_API_KEY = os.environ.get("NOTION_API_KEY")

        # Load the clients data
        self.CLIENTS_DATA = self._load_clients_data()

        # Store the client ID
        self.client_id = client_id
        self.client_data = self.CLIENTS_DATA[client_id]

        self.notion_page_id = self.client_data["notion_page_id"]

        # Create the headers for the API requests
        self.headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        # Define the parent page for the new page
        self.parent_page = {
            "type": "page_id",
            "page_id": "343f6e7933e043629c38d81ee01d789f",
        }

        if self.notion_page_id is None:
            # Create a new page for the client and store the page ID
            self.notion_page_id = self._create_page()
            self.client_data["notion_page_id"] = self.notion_page_id
            self._save_clients_data()

    def _load_clients_data(self):
        """Load clients data from JSON file."""
        try:
            with open("clients.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("clients.json not found. Creating an empty dictionary.")
            return {}

    def _save_clients_data(self):
        """Save updated clients data to JSON file."""
        self.CLIENTS_DATA[self.client_id] = self.client_data
        with open("clients.json", "w") as f:
            json.dump(self.CLIENTS_DATA, f, indent=2)
        print(f"Updated data for client {self.client_id} saved successfully.")

    def _create_page(self):
        """
        Create a new Notion page for the client.

        Uses client data to set the page title, icon, and cover.
        Creates the page as a child of self.parent_page.

        Returns:
            str or None: The ID of the new page if successful, None otherwise.
        """

        # Get the client's page details
        client_name = self.client_data["client_name"]
        notion_page_emoji = self.client_data["notion_page_emoji"]
        notion_page_cover_url = self.client_data["notion_page_cover_url"]

        page_title = f"{client_name}'s Workbook"

        # API endpoint for pages
        self.base_url = "https://api.notion.com/v1/pages"
        # Create the request body
        data = {
            "parent": self.parent_page,
            "icon": {"emoji": notion_page_emoji},
            "cover": {"external": {"url": notion_page_cover_url}},
            "properties": {
                "title": [{"text": {"content": page_title}}],
            },
        }

        # Make the POST request
        response = requests.post(self.base_url, headers=self.headers, json=data)

        # Check the response
        if response.status_code == 200:
            print("Successfully created the page in Notion")
            # Return the id of the created page
            return response.json()["id"]
        else:
            print(f"Failed to create the page. Status code: {response.status_code}")
            print(response.text)
            return None

    def add_content_to_page(self, children):
        """
        Add content blocks to the Notion page.

        Args:
            children (list): List of content blocks to add.

        Prints success or failure message.
        """

        # Create the request body
        data = {"children": children}

        url = f"https://api.notion.com/v1/blocks/{self.notion_page_id}/children"
        # Make a PATCH request to update the block children
        response = requests.patch(url, headers=self.headers, json=data)

        # Check the response
        if response.status_code == 200:
            print("Successfully updated the block children in Notion")
        else:
            print(
                f"Failed to update the block children. Status code: {response.status_code}"
            )
            print(response.text)

    def _generate_bulleted_list_items(self, contents):
        contents_list = []
        for content in contents:
            child = {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                },
            }
            contents_list.append(child)

        return contents_list

    def generate_interview_questions_body(self, questions):
        """
        Generate a Notion-compatible body for interview questions.

        Args:
            questions (list): List of interview questions as strings.

        Returns:
            list: A list containing a single dictionary representing a Notion
                'heading_2' block with toggleable interview questions as
                bulleted list items.
        """

        interview_questions = {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Interviewing Question"}}
                ],
                "is_toggleable": True,
                "children": self._generate_bulleted_list_items(questions),
            },
        }

        children = [interview_questions]

        return children

    def generate_project_workbook_body(self):

        children = []

        children.append(
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Project Charter"}}
                    ],
                },
            }
        )
        children.append(
            {
                "object": "block",
                "type": "heading_3",
                "heading_2": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Project Description"}}
                    ],
                },
            }
        )
        children.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Details of the project",
                            },
                        }
                    ]
                },
            }
        )
        return children
