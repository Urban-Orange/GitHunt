import os
import sys
from dotenv import load_dotenv
import requests

if sys.platform == "win32":
    os.system('cls')
else:
    os.system('clear')

load_dotenv()  # Load environment variables from .env file

def fetch_github_repositories(search_term, language=None):
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")

    if not access_token:
        access_token = input("Enter your GitHub access token: ")
        os.environ["GITHUB_ACCESS_TOKEN"] = access_token

    base_url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": search_term, "language": language} if language else {"q": search_term}

    response = requests.get(base_url, params=params, headers=headers)
    response_json = response.json()

    if response.status_code == 200:
        return response_json["items"]
    else:
        print(f"Failed to fetch repositories. Status code: {response.status_code}")
        return []

def display_repositories(repositories):
    for repo in repositories:
        print(f"Repository: {repo['name']}")
        print(f"Description: {repo['description']}")
        print(f"URL: {repo['html_url']}")
        print(f"Language: {repo['language']}")
        print("=" * 50)

if __name__ == "__main__":
    search_term = input("Enter the search term for GitHub repositories: ")
    language = input("Enter the programming language (optional): ")

    repositories = fetch_github_repositories(search_term, language)

    if repositories:
        print(f"Found {len(repositories)} repositories:")
        display_repositories(repositories)
    else:
        print("No repositories found.")
