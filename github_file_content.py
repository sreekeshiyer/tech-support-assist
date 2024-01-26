## List down the files and code in a GitHub Repository

from config import GITHUB_USERNAME, GITHUB_REPO
import requests
import base64

def get_file_content(owner, repo_name, file_path):
    """
    Fetch the content of a file from a public GitHub repository.

    Args:
        owner (str): The username or organization name that owns the repository.
        repo_name (str): The name of the GitHub repository.
        file_path (str): The path to the file in the repository.

    Returns:
        str: Content of the file in markdown format.
    """
    base_url = "https://api.github.com/repos"
    url = f"{base_url}/{owner}/{repo_name}/contents/{file_path}"

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content_data = response.json()
        content = base64.b64decode(content_data['content']).decode('utf-8')
        return f"## {file_path}\n\n```\n{content}\n```\n\n"
    else:
        print(f"Failed to fetch content for {file_path}. Status code: {response.status_code}")
        return ""

def list_files_and_content_in_repo(owner, repo_name):
    """
    List file paths and their content in a public GitHub repository.

    Args:
        owner (str): The username or organization name that owns the repository.
        repo_name (str): The name of the GitHub repository.

    Returns:
        str: Markdown formatted content of all files in the repository.
    """
    base_url = "https://api.github.com/repos"
    url = f"{base_url}/{owner}/{repo_name}/git/trees/main?recursive=1"

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    markdown_content = ""

    if response.status_code == 200:
        data = response.json()
        file_paths = [item['path'] for item in data.get('tree', []) if item['type'] == 'blob']

        for file_path in file_paths:
            if file_path.endswith("py"):
                markdown_content += get_file_content(owner, repo_name, file_path)

        return markdown_content
    else:
        print(f"Failed to fetch files. Status code: {response.status_code}")
        return ""
        
        
        
def generate_prompt_template():

    username = GITHUB_USERNAME
    repo_name = GITHUB_REPO
    
    prompt = list_files_and_content_in_repo(username, repo_name)
    
    return prompt