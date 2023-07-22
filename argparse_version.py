import os
import time
from dotenv import load_dotenv
import requests
from colorama import init, Fore, Style

if os.name == "nt":
    os.system('cls')
else:
    os.system('clear')

init(autoreset=True)  # Initialize colorama to automatically reset color

load_dotenv()  # Load environment variables from .env file (just the GitHub access token for now)

def fetch_github_repositories(search_term, language=None, max_results=250):
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")

    if not access_token:
        access_token = input("Enter your GitHub access token: ")
        os.environ["GITHUB_ACCESS_TOKEN"] = access_token

    base_url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"Bearer {access_token}"}

    if language:
        language = language.lower()

    params = {"q": search_term, "language": language, "per_page": 250} if language else {"q": search_term, "per_page": 250}

    repositories = []
    page = 1
    total_results = 0  # Track the total number of results found

    while True:
        params["page"] = page
        response = requests.get(base_url, params=params, headers=headers)
        response_json = response.json()

        if response.status_code == 200:
            current_repositories = response_json["items"]
            if not current_repositories:
                break
            repositories.extend(current_repositories)
            total_results = response_json.get('total_count', 0)  # Update the total number of results
            page += 1
            if len(repositories) >= max_results or len(current_repositories) < 100:
                break
        else:
            print(f"{Fore.RED}Failed to fetch repositories. Status code: {response.status_code}")
            break

    # Sort repositories based on the 'updated_at' field (most recently updated to oldest updated)
    repositories.sort(key=lambda x: x.get('updated_at'), reverse=True)

    return repositories[:max_results], total_results

def display_repositories(repositories):
    for repo in repositories:
        print(f"{Fore.GREEN}Repository: {repo['name']}")
        print(f"{Fore.YELLOW}Description: {repo['description']}")
        print(f"{Fore.CYAN}URL: {repo['html_url']}")
        print(f"{Fore.MAGENTA}Language: {repo['language']}")

        # Check if the 'updated_at' field is available
        if repo.get('updated_at'):
            updated_at = repo['updated_at'].replace('T', ' ').replace('Z', ' UTC')
            print(f"{Fore.RESET}Last Updated: {updated_at}")
        else:
            print(f"{Fore.RESET}Last Updated: Not available")

        # Check if the repository is archived by the owner
        if repo.get('archived', False):
            print(f"{Fore.RED}Repository is archived by the owner.")

        print("=" * 60)

def fetch_github_users(search_term, max_results=250):
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")

    if not access_token:
        access_token = input("Enter your GitHub access token: ")
        os.environ["GITHUB_ACCESS_TOKEN"] = access_token

    base_url = "https://api.github.com/search/users"
    headers = {"Authorization": f"Bearer {access_token}"}

    params = {"q": search_term, "per_page": 250}

    users = []
    page = 1
    total_results = 0  # Track the total number of results found

    while True:
        params["page"] = page
        response = requests.get(base_url, params=params, headers=headers)
        response_json = response.json()

        if response.status_code == 200:
            current_users = response_json["items"]
            if not current_users:
                break
            users.extend(current_users)
            total_results = response_json.get('total_count', 0)  # Update the total number of results
            page += 1
            if len(users) >= max_results or len(current_users) < 100:
                break
        else:
            print(f"{Fore.RED}Failed to fetch users. Status code: {response.status_code}")
            break

    return users[:max_results], total_results

def display_github_users(users):
    for user in users:
        print(f"{Fore.GREEN}User: {user['login']}")
        print(f"{Fore.CYAN}Profile: {user['html_url']}")
        print("=" * 60)
        print("")

def get_github_access_token():
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")

    if not access_token:
        access_token = input(f"{Fore.YELLOW}Please enter your GitHub access token: {Fore.RESET}")
        with open(".env", "a") as env_file:
            env_file.write(f"GITHUB_ACCESS_TOKEN={access_token}\n")
        os.environ["GITHUB_ACCESS_TOKEN"] = access_token

def main():
    import argparse

    parser = argparse.ArgumentParser(prog="GitHunt", description="A Simple GitHub Search Tool")

    # Optional argument for GitHub access token
    parser.add_argument(
        "--token",
        action="store_true",
        help="Prompt to enter your GitHub access token. You can generate a personal access token from your GitHub Developer Settings.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--repo",
        action="store_true",
        help="Search for repositories",
    )
    group.add_argument(
        "--user",
        action="store_true",
        help="Search for users",
    )
    group.add_argument(
        "--both",
        action="store_true",
        help="Search for both repositories and users",
    )

    parser.add_argument(
        "search_term",
        type=str,
        help="The search term",
    )
    parser.add_argument(
        "--language",
        metavar="", # Annoying text removed
        type=str,
        help="Filter by programming language (applicable in repository search)",
    )
    parser.add_argument(
        "--max_results",
        metavar="", # Annoying text removed
        type=int,
        help="Maximum number of results to display",
    )

    args = parser.parse_args()

    if args.token:
        get_github_access_token()

    if args.repo:
        repositories, total_results = fetch_github_repositories(args.search_term, args.language, args.max_results)
        # Display repositories
        display_repositories(repositories)
    elif args.user:
        users, total_results = fetch_github_users(args.search_term, args.max_results)
        # Display users
        display_github_users(users)
    elif args.both:
        repositories, repo_total = fetch_github_repositories(args.search_term, args.language, args.max_results)
        users, user_total = fetch_github_users(args.search_term, args.max_results)

        # Display repositories
        print(f"{Fore.GREEN}Found {repo_total} repositories:")
        print("=" * 60)
        display_repositories(repositories)

        # Display users
        print(f"{Fore.GREEN}Found {user_total} users:")
        print("=" * 60)
        display_github_users(users)

    # Print example usage commands
    print(f"{Fore.CYAN}Example Usage:")
    print(f"{Fore.YELLOW} 1. Simplest Command:")
    print(f"{Fore.RESET}    GitHunt --user python")
    print(f"{Fore.YELLOW} 2. Search with Language Filter:")
    print(f"{Fore.RESET}    GitHunt --repo --language python --max_results 50")
    print(f"{Fore.YELLOW} 3. Search for Both Repositories and Users:")
    print(f"{Fore.RESET}    GitHunt --both --max_results 1000 openai")

if __name__ == "__main__":
    main()
