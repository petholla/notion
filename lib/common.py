import os
import requests
import configparser
from pprint import pprint
from dataclasses import dataclass

@dataclass
class Notion:
    token: str = ""
    def __post_init__(self):
        """Get token from ~/.notion.ini"""
        home = os.path.expanduser("~")
        config = configparser.ConfigParser()
        config.read(f"{home}/.notion.ini")
        if "DEFAULT" in config and "token" in config["DEFAULT"]:
            self.token = config["DEFAULT"]["token"]
        else:
            raise ValueError("Token not found in ~/.notion.ini")
        
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
        
        return response
    
    def get_databases(self):
        """Get all databases"""
        data = {
            "filter": {
                "property": "object",
                "value": "database"
            }
        }
        response = self.call_api("POST", "/search", data=data)
        return response.json().get("results", [])
