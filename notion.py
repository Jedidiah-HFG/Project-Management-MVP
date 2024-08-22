import os
import json
import time
import requests
import datetime
import pytz
import streamlit as st


class Notion:

    colors = [
        "blue",
        "brown",
        "default",
        "gray",
        "green",
        "orange",
        "yellow",
        "green",
        "pink",
        "purple",
        "red",
    ]

    bg_colors = [
        "blue_background",
        "brown_background",
        "gray_background",
        "green_background",
        "orange_background",
        "pink_background",
        "purple_background",
        "red_background",
        "yellow_background",
    ]

    def __init__(self, client_id: str):

        self.dev = False

        # Retrieve the Notion API key from environment variable
        NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
        if self.dev:
            return

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

        # Load the clients data
        self.CLIENTS_DATA = self._load_clients_data()

        # Store the client ID
        self.client_id = client_id
        # Retrieve the client data
        self.client_data = self.CLIENTS_DATA.get(
            client_id, self.CLIENTS_DATA["new_client"]
        )

        self.notion_page_id = self.client_data["notion_page_id"]

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
        print(f"Successfully updated json data for {self.client_id}")

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

        # Get the current date and time in EST
        est = pytz.timezone("US/Eastern")
        current_datetime_est = datetime.datetime.now(est)

        # Format the date and time
        formatted_datetime = current_datetime_est.strftime("%Y-%m-%d %H:%M")

        # Create the page title with the date and time
        page_title = f"{client_name}'s Workbook - {formatted_datetime}"

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
            print("Successfully created a new page in Notion")
            # Return the id of the created page
            return response.json()["id"]
        else:
            print(f"Failed to create the page. Status code: {response.status_code}")
            print(response.text)
            return None

    def _generate_bulleted_list_items(self, list_contents):
        contents_list = []
        for content in list_contents:
            child = {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                },
            }
            contents_list.append(child)

        return contents_list

    def _add_content_to_page(self, children):
        """
        Add content blocks to the Notion page in batches of 10.

        Args:
            children (list): List of content blocks to add.

        Prints success or failure message.
        """
        if self.dev:
            return

        batch_size = 50
        for i in range(0, len(children), batch_size):
            batch = children[i : i + batch_size]

            # Create the request body for this batch
            data = {"children": batch}

            url = f"https://api.notion.com/v1/blocks/{self.notion_page_id}/children"
            # Make a PATCH request to update the block children
            response = requests.patch(url, headers=self.headers, json=data)

            # Check the response
            if response.status_code == 200:
                print(
                    f"Successfully updated page in Notion (batch {i//batch_size + 1})"
                )

            elif response.status_code == 400:
                error_data = response.json()
                if error_data.get(
                    "code"
                ) == "validation_error" and "archived" in error_data.get("message", ""):
                    print(
                        "Block is archived or doesn't exist. Attempting to create a new block."
                    )

                    # Create a new page for the client and store the page ID
                    self.notion_page_id = self._create_page()
                    self.client_data["notion_page_id"] = self.notion_page_id
                    self._save_clients_data()

                    # Retry adding this batch to the new page
                    self._add_content_to_page(batch)

                else:
                    print(
                        f"Failed to update the block children (batch {i//batch_size + 1}). Status code: {response.status_code}"
                    )
                    print(response.text)
            else:
                print(
                    f"Failed to update the block children (batch {i//batch_size + 1}). Status code: {response.status_code}"
                )
                print(response.text)

            # Add a small delay between batches to avoid rate limiting
            time.sleep(1)

    def add_toggleable_notion_block(self, title, content):
        """
        Create a toggleable Notion block with a title and content, either as plain text or a bulleted list.

        Args:
            title (str): The title for the toggleable block.
            content (str or list): The content to be added. If is_list is True, this should be a list of strings.

        Returns:
            list: A list containing a single dictionary representing a Notion
                'heading_2' block with toggleable content, either as plain text or
                bulleted list items.
        """

        content_block = {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": title}}],
                "is_toggleable": True,
                "children": [],
            },
        }

        if isinstance(content, list):
            content_block["heading_2"]["children"] = self._generate_bulleted_list_items(
                content
            )
        else:
            content_block["heading_2"]["children"] = [
                {
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    },
                }
            ]

        st.session_state["logs"][title] = content

        # Add the content to the page
        self._add_content_to_page(children=[content_block])

        return

    def update_project_workbook(self, workbook_contents):

        children = []

        # children.append(
        #     {
        #         "type": "heading_1",
        #         "heading_1": {
        #             "rich_text": [
        #                 {"type": "text", "text": {"content": "Project Charter"}}
        #             ],
        #             "color": "red_background",
        #         },
        #     }
        # )

        def get_title_element(text_content):
            return {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": text_content}}],
                    "color": "purple_background",
                },
            }

        for key, value in workbook_contents.items():

            # Convert the key to title case
            title = key.replace("_", " ").title()

            # Add the title element
            children.append(get_title_element(title))
            # Add the bulleted list items

            if isinstance(value, list):
                children.extend(self._generate_bulleted_list_items(value))
            else:
                children.extend(self._generate_bulleted_list_items([value]))

            # st.session_state["logs"][title] = value

        # Add the content to the page
        self._add_content_to_page(children=children)

        return
