import requests
import json

def get_repos(user_id):
    """
    Retrieves a list of repositories for a given GitHub user along with the number of commits for each.
    
    Args:
        user_id (str): GitHub user ID to query
    
    Returns:
        list: A list of tuples containing (repo_name, number_of_commits)
              Returns an empty list if the user doesn't exist or has no repositories
    """
    # Implementation here
    def get_repos(user_id):
    """
    Retrieves a list of repositories for a given GitHub user along with the number of commits for each.
    
    Args:
        user_id (str): GitHub user ID to query
    
    Returns:
        list: A list of tuples containing (repo_name, number_of_commits)
              Returns an empty list if the user doesn't exist or has no repositories
    """
    repos = []
    
    # Get user's repositories
    repo_url = f"https://api.github.com/users/{user_id}/repos"
    try:
        response = requests.get(repo_url)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        # Process each repository
        for repo in response.json():
            repo_name = repo["name"]
            
            # Get commits for this repository
            commits_url = f"https://api.github.com/repos/{user_id}/{repo_name}/commits"
            try:
                commits_response = requests.get(commits_url)
                commits_response.raise_for_status()
                commits_count = len(commits_response.json())
                
                repos.append((repo_name, commits_count))
                
            except (requests.RequestException, ValueError, KeyError) as e:
                # Handle errors for individual repositories gracefully
                print(f"Error retrieving commits for {repo_name}: {str(e)}")
                repos.append((repo_name, "Error"))
                
    except (requests.RequestException, ValueError) as e:
        print(f"Error retrieving repositories for user {user_id}: {str(e)}")
    
    return repos
