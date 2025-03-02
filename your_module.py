import requests

def get_repo_info(username, repo_name):
    """
    Get basic information about a GitHub repository.
    Returns the repository data as a dictionary.
    """
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get repository info: {response.status_code}")

def get_user_repos(username):
    """
    Get a list of repositories for a given GitHub user.
    Returns a list of repository names.
    """
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        return [repo["name"] for repo in repos]
    else:
        raise Exception(f"Failed to get user repositories: {response.status_code}")

def get_repo_commits(username, repo_name):
    """
    Get a list of commits for a specific repository.
    Returns a list of commit dictionaries.
    """
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get repository commits: {response.status_code}")

def count_user_commits(username):
    """
    Count the total number of commits across all repositories for a user.
    Returns a dictionary with repo names as keys and commit counts as values.
    """
    repos = get_user_repos(username)
    commit_counts = {}
    
    for repo in repos:
        try:
            commits = get_repo_commits(username, repo)
            commit_counts[repo] = len(commits)
        except Exception:
            commit_counts[repo] = 0
    
    return commit_counts
