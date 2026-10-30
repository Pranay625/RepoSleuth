import re
from collector.github_client import GitHubClient

class RespositoryCollector:
    def __init__(self):
        self.client = GitHubClient()

    @staticmethod
    def parse_github_url(url: str) -> tuple[str, str]:
        """Extracts (owner, repo) from standard or trailing-slash GitHub URLs."""
        clean_url = url.strip().rstrip("/")
        match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+)(?:\.git)?$", clean_url)

        if not match: 
            raise ValueError(f"Invalid GitHub repository URL: {url}")
        return match.group("owner"), match.group("repo")

    def fetch_repository_metadata(self, owner: str, repo: str) -> dict:
        data = self.client.get(f"repos/{owner}/{repo}")
        return {
            "name": data.get("name"),
            "full_name": data.get("full_name"),
            "description": data.get("description"),
            "html_url": data.get("html_url"),
            "default_branch": data.get("default_branch"),
            "stargazers_count": data.get("stargazers_count"),
            "forks_count": data.get("forks_count"),
            "open_issues_count": data.get("open_issues_count"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"), 
        }

    def fetch_issues(self, owner: str, repo: str, state: str = "all", per_page: int = 100, max_pages: int=3) -> list:
        """Fetches issues with pagination support (excluding pull requests which GitHub includes in issues API)."""

        issues = []
        page = 1

        while page <= max_pages:
            params = {
                "state": state,
                "per_page": per_page,
                "page": page,
                "sort": "updated", 
                "direction": "desc"
            }
            data = self.client.get(f"repos/{owner}/{repo}/issues", params)

            if not data:
                break

            for item in data:
                # GitHub API treats Pull Requests as issues; filter them out if needed

                if "pull_request" in item:
                    continue
                issues.append({
                    "number": item.get("number"),
                    "title": item.get("title"),
                    "state": item.get("state"),
                    "created_at": item.get("created_at"),
                    "updated_at": item.get("updated_at"),
                    "comments_count": item.get("comments"),
                    "html_url": item.get("html_url"),
                    "labels": [label["name"] for label in item.get("labels", [])]
                })

            if len(data) < per_page:
                break
            page += 1

        return issues

