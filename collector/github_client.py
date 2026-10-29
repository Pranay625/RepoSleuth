import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GitHubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = ""
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-22-28"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers = self.headers, params = params)

        if response.status_code == 401:
            raise Exception("Github API authentication failed. Check your GITHUB_TOKEN.")
        elif response.status_code == 403:
            raise Exception("GitHub API rate limit exceeded or access forbidden.")
        elif response.status_code == 404:
            raise Exception(f"Resource not found: {url}")

        response.raise_for_status()
        return response.json()