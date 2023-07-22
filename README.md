# GitHunt - A Simple GitHub Search Tool 🔎

GitHunt is a Python-based GitHub Search tool that allows users to find relevant repositories and users on GitHub based on their search terms and preferred programming language. There are two versions of the tool available: `main.py` and `argparse_version.py`. Each version offers a different way to interact with the program.

## main.py Version

### Description

The `main.py` version of GitHunt is a user-friendly command-line tool that provides a simple interface for searching GitHub repositories and users. The program prompts the user to enter a search term and select from three search modes: repositories, users, or both. It also allows users to filter repositories by programming language and specify the maximum number of results to display.

### Requirements

- Python 3.x (Python 2.x version coming soon)
- `requests`
- `python-dotenv`
- `colorama` modules

### Usage

1. Clone the repository or download it from the latest release section.

2. Install the required modules by using the command `pip install requests python-dotenv colorama` in your terminal.

3. The first time you run the program, it will ask you to enter your GitHub access token. For subsequent runs, the program will use the stored token from the environment variable.

4. Run the program using the command `python main.py`.

5. Follow the on-screen prompts to enter your search term and select the search mode (repositories, users, or both). Optionally, you can filter repositories by programming language and specify the maximum number of results to display.

6. The program will fetch and display the search results based on your input.

## argparse_version.py Version

### Description

The `argparse_version.py` version of GitHunt uses the `argparse` library to provide a more flexible and structured command-line interface. Users can specify search options and arguments directly from the command line, making it easier to automate and integrate the tool with other scripts or workflows.

### Requirements

- Python 3.x (Python 2.x version coming soon)
- `requests`
- `python-dotenv`
- `colorama` modules

### Usage

1. Clone the repository or download it from the latest release section.

2. Install the required modules by using the command `pip install requests python-dotenv colorama` in your terminal.

3. The first time you run the program, it will ask you to enter your GitHub access token. For subsequent runs, the program will use the stored token from the environment variable.

4. Run the program using the command `python argparse_version.py`.

5. Use the command-line arguments to specify your search term, search mode (repositories, users, or both), programming language (optional), and maximum number of results to display (optional).

6. The program will fetch and display the search results based on your input.

### Example Usage

1. Simplest Command Example:

 `python argparse_version.py --user bob` 

2. Search with Language Filter:

 `python argparse_version.py --repo --language python --max_results 50`

3. Search for Both Repositories and Users:

 `python argparse_version.py --both --max_results 1000 openai`
