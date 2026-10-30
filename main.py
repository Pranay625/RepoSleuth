import json
from collector.repo import RepositoryCollector

def main():
    # Test repository URL (e.g., FastAPI, Requests, or your own repo)

    repo_url = input("Enter GitHub Repository URL: ").strip()

    collector = RepositoryCollector()

    try:
        print(f"\n Parsing URL and fetching metadata...")

        owner, repo = collector.parse_github_url(repo_url)

        metadata = collector.fetch_repository_metadata(owner, repo)
        print(f" Repository Found: {metadata['full_name']}")
        print(f" Description: {metadata['description']}")
        print(f" Stars: {metadata['stargazers_count']} | Forks: {metadata['forks_count']} | Open Issues: {metadata['open_issues_count']}")

        print(f"\n Fetching recent issues...")
        issues = collector.fetch_issues(owner, repo, state = "all", max_pages = 2)
        print(f" Fetched {len(issues)} issues (excluding PRs).")

        # Display sample output
        if issues:
            print("\n--- Sample Issue ---")
            print(json.dumps(issues[0], indent = 2))

    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()