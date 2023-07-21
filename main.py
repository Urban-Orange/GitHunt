import os
import sys
from dotenv import load_dotenv
import requests

if sys.platform == "win32":
    os.system('cls')
else:
    os.system('clear')

load_dotenv()  # Load environment variables from .env file

def fetch_github_repositories(search_term, language=None, max_results=100):
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")

    if not access_token:
        access_token = input("Enter your GitHub access token: ")
        os.environ["GITHUB_ACCESS_TOKEN"] = access_token

    base_url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    if language:
        language = language.lower()
    
    params = {"q": search_term, "language": language, "per_page": 100} if language else {"q": search_term, "per_page": 100}

    repositories = []
    page = 1

    while True:
        params["page"] = page
        response = requests.get(base_url, params=params, headers=headers)
        response_json = response.json()

        if response.status_code == 200:
            current_repositories = response_json["items"]
            if not current_repositories:
                break
            repositories.extend(current_repositories)
            page += 1
            if len(repositories) >= max_results:
                break
        else:
            print(f"Failed to fetch repositories. Status code: {response.status_code}")
            break

    # Filter repositories to match the specified language
    if language:
        repositories = [repo for repo in repositories if repo['language'] and repo['language'].lower() == language]

    return repositories[:max_results]

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
