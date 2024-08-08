import requests
import os
from pprint import pprint

# Retrieve the Notion API key from environment variable
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")

# API endpoint
url = "https://api.notion.com/v1/pages"

# Headers
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Request body
data = {
    "parent": {"type": "page_id", "page_id": "343f6e7933e043629c38d81ee01d789f"},
    "icon": {"emoji": "👨‍💻"},
    "cover": {
        "external": {
            "url": "https://images.unsplash.com/photo-1526948531399-320e7e40f0ca?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        }
    },
    "properties": {
        "title": [{"text": {"content": "Dan's Workbook"}}],
    },
    "children": [
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Can you tell us more about your goals and objectives for this project?"
                        },
                    },
                ],
            },
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "What are the key challenges you're facing, and how do you think this project can help address them?"
                        },
                    },
                ],
            },
        },
        # "content": "How do you envision this project contributing to your overall business strategy?"
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Project Details"}}],
            },
        },
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
        },
    ],
}


# Make the POST request
response = requests.post(url, headers=headers, json=data)

# Check the response
if response.status_code == 200:
    print("Successfully created the page in Notion")
    pprint(response.json())
else:
    print(f"Failed to create the page. Status code: {response.status_code}")
    print(response.text)
