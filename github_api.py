import requests

def get_repos(username):
    """
    Fetches a GitHub user's repositories and their commit counts.
    
    :param username: GitHub username
    :return: List of tuples (repository_name, commit_count)
    """
    base_url = "https://api.github.com/users/{}/repos".format(username)
    
    try:
        repo_response = requests.get(base_url)
        repo_response.raise_for_status()  # Raise error if the request fails
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")
        return []

    repos = repo_response.json()
    result = []

    for repo in repos:
        repo_name = repo.get("name", "")
        commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        
        try:
            commits_response = requests.get(commits_url)
            commits_response.raise_for_status()
            commit_count = len(commits_response.json())  # Count commits
        except requests.exceptions.RequestException as e:
            print(f"Error fetching commits for {repo_name}: {e}")
            commit_count = 0  # Assume 0 commits on failure
        
        result.append((repo_name, commit_count))
    
    return result

    
