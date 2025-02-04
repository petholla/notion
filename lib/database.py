from dataclasses import dataclass, field
from pprint import pprint
from lib.page import Page

@dataclass
class Database:
    notion: "Notion"
    id: str
    data: dict = field(repr=False)

    @property
    def title(self):
        """Database title."""
        title = self.data.get("title")
        if title:
            return title[0].get("plain_text")

    def get_pages(self, title_contains=None):
        """Get all pages in this database"""
        data = {}

        if title_contains:
            data["filter"] = {
                "property": "Name",
                "title": {
                    "contains": title_contains
                }
            }
        response = self.notion.call_api("POST", f"/databases/{self.id}/query", data=data)
        response_data = response.json()
        results = response_data.get("results", [])
        print(f"Number of results: {len(results)}")
        for page_data in results:
            page = Page(notion=self.notion, id=page_data["id"], data=page_data)
            yield page
    
    def add_page(self, title: str):
        """Add a database page."""

        data = {
            "parent": {
                "database_id": self.id,
            },
            "properties": {
                "Name": {
                    "title": {
                        "text": {
                            "content": title
                        }
                    }
                }
            }
        }

        response = self.notion.call_api("POST", f"/databases/v1/pages", data=data)