# GitHunt

GitHunt: A powerful GitHub Repository Search tool to discover relevant repositories based on your search terms and preferred language. Simplify your code exploration today!

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

GitHunt is a Python-based GitHub Repository Search tool that allows users to find relevant repositories on GitHub based on their search terms and preferred programming language. The program makes use of the `requests` module to interact with the GitHub API, fetching repository data and displaying key information for user exploration.

## Features

- Search GitHub repositories using custom search terms.
- Optionally filter results by programming language.
- Display repository name, description, URL, and language.
- User-friendly command-line interface.

## Requirements

- Python 3.x
- `requests` module
- `python-dotenv` module

## Usage

1. Clone the repository or download from the `latest release` section.

2. Install the required `requests` and `python-dotenv` modules by using this command:
<button class="btn" data-clipboard-text="pip install python-dotenv requests">Copy</button>

3. The first time you run the program, it will ask you to enter your GitHub access token. For subsequent runs, the program will use the stored token from the environment variable.

4. Run the program:

5. Follow the on-screen prompts to enter your search term and, optionally, a programming language.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

...
