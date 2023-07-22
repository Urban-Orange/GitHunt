import os
import sys
import time
from dotenv import load_dotenv
import requests
from colorama import init, Fore, Style

if sys.platform == "win32":
    os.system('cls')
else:
    os.system('clear')

init(autoreset=True)  # Initialize colorama to automatically reset color

load_dotenv()  # Load environment variables from .env file (just the github access token for now)

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

while True:
    
    print(f"""{Fore.BLUE}
   _____ _ _     _    _             _   
  / ____(_) |   | |  | |           | |  
 | |  __ _| |_  | |__| |_   _ _ __ | |_ 
 | | |_ | | __| |  __  | | | | '_ \| __|
 | |__| | | |_  | |  | | |_| | | | | |_ 
  \_____|_|\__| |_|  |_|\__,_|_| |_|\__|
                                        
                                        
                                        
A Simple GitHub Search 🔎 Tool
{Fore.RESET}""")
    
    search_term = input(f"{Fore.CYAN}Enter the search term: {Fore.RESET}")
    
    if not search_term:
        print(f"{Fore.YELLOW}Search term cannot be empty. Please try again.")
        time.sleep(3)
        if sys.platform == "win32":
            os.system('cls')
        else:
            os.system('clear')
        print(f"""{Fore.BLUE}
   _____ _ _     _    _             _   
  / ____(_) |   | |  | |           | |  
 | |  __ _| |_  | |__| |_   _ _ __ | |_ 
 | | |_ | | __| |  __  | | | | '_ \| __|
 | |__| | | |_  | |  | | |_| | | | | |_ 
  \_____|_|\__| |_|  |_|\__,_|_| |_|\__|
                                        
                                        
                                        
A Simple GitHub Search 🔎 Tool
{Fore.RESET}""")
        continue
        

    search_mode = input(f"{Fore.CYAN}Choose a search mode (1: Repositories, 2: Users, 3: Both): {Fore.RESET}")

    if search_mode == '1':
        language = input(f"{Fore.CYAN}Enter the programming language (optional): {Fore.RESET}")
        max_results_input = input(f"{Fore.CYAN}Enter the maximum number of repositories to show [Press ENTER for default 250]: {Fore.RESET}")
        print("")

        try:
            max_results = int(max_results_input) if max_results_input else 250
            repositories, total_results = fetch_github_repositories(search_term, language, max_results)

            if repositories:
                found_count = min(len(repositories), total_results)
                print(f"{Fore.GREEN}Found {total_results} repositories, displaying the first {found_count} repositories:")
                print("")
                display_repositories(repositories)
            else:
                print(f"{Fore.YELLOW}No repositories found.")
        except ValueError:
            print(f"{Fore.RED}Invalid input for maximum results. Please enter a number.")
            time.sleep(3)
            if sys.platform == "win32":
                os.system('cls')
            else:
                os.system('clear')

    elif search_mode == '2':
        max_results_input = input(f"{Fore.CYAN}Enter the maximum number of users to show [Press ENTER for default 250]: {Fore.RESET}")
        print("")

        try:
            max_results = int(max_results_input) if max_results_input else 250
            users, total_results = fetch_github_users(search_term, max_results)

            if users:
                found_count = min(len(users), total_results)
                if found_count == 1:
                    print(f"{Fore.GREEN}Found {total_results} user with the search term {Fore.BLUE}{search_term}{Fore.GREEN}, displaying the first/only user:")
                else:
                    print(f"{Fore.GREEN}Found {total_results} users with the search term {Fore.BLUE}{search_term}{Fore.GREEN}, displaying the first {found_count} users:")
                print("")
                display_github_users(users)
            else:
                print(f"{Fore.YELLOW}No users found.")
        except ValueError:
            print(f"{Fore.RED}Invalid input for maximum results. Please enter a number.")
            time.sleep(3)
            if sys.platform == "win32":
                os.system('cls')
            else:
                os.system('clear')

    elif search_mode == '3':
        language = input(f"{Fore.CYAN}Enter the programming language [optional]: {Fore.RESET}")
        max_results_input = input(f"{Fore.CYAN}Enter the maximum number of repositories and users to show [Press ENTER for default 250]: {Fore.RESET}")
        print("")

        try:
            max_results = int(max_results_input) if max_results_input else 250
            repositories, repo_total = fetch_github_repositories(search_term, language, max_results)
            users, user_total = fetch_github_users(search_term, max_results)

            print(f"{Fore.GREEN}Found {repo_total} repositories and {user_total} users ")
            print("")

            if repositories:
                found_count = min(len(repositories), repo_total)
                print(f"{Fore.GREEN}Displaying the first {found_count} repositories:")
                print("")
                display_repositories(repositories)
            else:
                print(f"{Fore.YELLOW}No repositories found.")
                print("=" * 70)

            if users:
                found_count = min(len(users), total_results)
                if found_count == 1:
                    print(f"{Fore.GREEN}Found {total_results} user with the search term {Fore.BLUE}{search_term}{Fore.GREEN}, displaying the first/only user:")
                else:
                    print(f"{Fore.GREEN}Found {total_results} users with the search term {Fore.BLUE}{search_term}{Fore.GREEN}, displaying the first {found_count} users:")
                print("")
                display_github_users(users)
            else:
                print(f"{Fore.YELLOW}No users found.")
                print("")

        except ValueError:
            print(f"{Fore.RED}Invalid input for maximum results. Please enter a number.")
            print('')
            time.sleep(3)
            if sys.platform == "win32":
                os.system('cls')
            else:
                os.system('clear')

    else:
        print(f"{Fore.RED}Invalid input. Please enter 1, 2, or 3.")
        time.sleep(3)
        if sys.platform == "win32":
            os.system('cls')
        else:
            os.system('clear')

    # Ask if the user wants to perform another search or exit the program
    exit_choice = input(f"{Fore.CYAN}Search query finished. Press Enter to exit or ['R'] to Reset Program: {Fore.RESET}")
    exit_choice = exit_choice.upper()
    if exit_choice != 'R':
        break
    else:
        if sys.platform == "win32":
            os.system('cls')
        else:
            os.system('clear')
            

print(f"{Fore.YELLOW}Thank you for using GitHunt. Goodbye!{Fore.RESET}")
