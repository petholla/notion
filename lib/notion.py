import os
import requests
import configparser
from pprint import pprint
from dataclasses import dataclass, field
from lib.database import Database
from lib.common import get_config_value, get_logger

logger = get_logger()

@dataclass
class Notion:
    token: str = field(init=False, repr=False)
    def __post_init__(self):
        """Get token from credentials ini file"""
        try:
            self.token = get_config_value(section="notion", key="token")
        except configparser.Error as exception:
            logger.error(f"Could not get Notion token: {exception}")
            exit(1)
        
    def call_api(self, method, path, data=None):
        """Call Notion API"""
        headers = {"Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
        }

        base_url = "https://api.notion.com/v1/"

        url = base_url + path.lstrip("/")

        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        else:
            raise ValueError("Invalid method")
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exception:
            logger.error(exception)

        return response
    
    def get_databases(self, query: str = None):
        """Get all databases"""
        data = {
            "filter": {
                "property": "object",
                "value": "database"
            }
        }
        if query:
            data["query"] = query

        response = self.call_api("POST", "/search", data=data)
        
        for database_data in response.json().get("results", []):
            database = Database(notion=self, id=database_data["id"], data=database_data)
            yield database

    def get_database(self, title: str):
        """Get database by title."""
        for database in self.get_databases(query=title):
            print(database.title, title)
            if database.title == title:
                return database