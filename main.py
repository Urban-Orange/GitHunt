import os
import sys
from dotenv import load_dotenv
import requests
from colorama import init, Fore, Style

if sys.platform == "win32":
    os.system('cls')
else:
    os.system('clear')

init(autoreset=True)  # Initialize colorama to automatically reset color

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
            print(f"{Fore.RED}Failed to fetch repositories. Status code: {response.status_code}")
            break

    # Filter repositories to match the specified language and optional keywords in the description
    if language or search_term:
        search_term = search_term.lower()
        repositories = [repo for repo in repositories if 
                        (not language or (repo['language'] and repo['language'].lower() == language)) and
                        (search_term in repo['name'].lower() or search_term in repo['description'].lower())]

    return repositories[:max_results]

def display_repositories(repositories):
    for repo in repositories:
        print(f"{Fore.GREEN}Repository: {repo['name']}")
        print(f"{Fore.YELLOW}Description: {repo['description']}")
        print(f"{Fore.CYAN}URL: {repo['html_url']}")
        print(f"{Fore.MAGENTA}Language: {repo['language']}")
        print(f"{Fore.RESET}{Style.BRIGHT}{'=' * 50}")

if __name__ == "__main__":
    search_term = input(f"{Fore.BLUE}Enter the search term for GitHub repositories: ")
    language = input(f"{Fore.BLUE}Enter the programming language (optional): ")

    repositories = fetch_github_repositories(search_term, language)

    if repositories:
        print(f"{Fore.GREEN}Found {len(repositories)} repositories:")
        display_repositories(repositories)
    else:
        print(f"{Fore.YELLOW}No repositories found.")
