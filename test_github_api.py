import unittest
from unittest.mock import patch, Mock
from github_api import get_repos
import requests

class TestGitHubAPI(unittest.TestCase):
    
    @patch('github_api.requests.get')
    def test_get_repos_success(self, mock_get):
        """ Test normal API call where user has two repositories with commits """
        
        mock_repo_response = Mock()
        mock_repo_response.json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        mock_repo_response.raise_for_status.return_value = None
        
        mock_commit_response1 = Mock()
        mock_commit_response1.json.return_value = [{"sha": "abc123"}, {"sha": "def456"}]
        mock_commit_response1.raise_for_status.return_value = None

        mock_commit_response2 = Mock()
        mock_commit_response2.json.return_value = [{"sha": "ghi789"}]
        mock_commit_response2.raise_for_status.return_value = None
        
        # Simulating API responses
        mock_get.side_effect = [mock_repo_response, mock_commit_response1, mock_commit_response2]

        result = get_repos("testuser")
        expected = [("repo1", 2), ("repo2", 1)]
        self.assertEqual(result, expected)

    @patch('github_api.requests.get')
    def test_get_repos_user_not_found(self, mock_get):
        """ Test when user does not exist (404) """
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response

        result = get_repos("nonexistentuser")
        self.assertEqual(result, [])

    @patch('github_api.requests.get')
    def test_get_repos_no_commits(self, mock_get):
        """ Test when repositories exist but have zero commits """
        
        mock_repo_response = Mock()
        mock_repo_response.json.return_value = [{"name": "repo1"}]
        mock_repo_response.raise_for_status.return_value = None

        mock_commit_response = Mock()
        mock_commit_response.json.return_value = []
        mock_commit_response.raise_for_status.return_value = None

        mock_get.side_effect = [mock_repo_response, mock_commit_response]

        result = get_repos("testuser")
        expected = [("repo1", 0)]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
