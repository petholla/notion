from dataclasses import dataclass, field
from pprint import pprint
from lib.page import Page

@dataclass
class Database:
    notion: "Notion"
    id: str
    data: dict = field(repr=False)

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
        pprint(response.json())
        for page_data in response.json().get("results", []):
            page = Page(notion=self.notion, id=page_data["id"], data=page_data)
            yield page