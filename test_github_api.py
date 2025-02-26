import unittest
from unittest.mock import patch, Mock
from github_api import get_repos

class TestGitHubAPI(unittest.TestCase):
    
    @patch('github_api.requests.get')
    def test_get_repos_normal_case(self, mock_get):
        # Mock the API responses
        mock_repo_response = Mock()
        mock_repo_response.json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_repo_response.raise_for_status.return_value = None
        
        mock_commits_response1 = Mock()
        mock_commits_response1.json.return_value = [{"sha": "abc123"}, {"sha": "def456"}]
        mock_commits_response1.raise_for_status.return_value = None
        
        mock_commits_response2 = Mock()
        mock_commits_response2.json.return_value = [{"sha": "ghi789"}]
        mock_commits_response2.raise_for_status.return_value = None
        
        # Configure the mock to return the responses
        mock_get.side_effect = [mock_repo_response, mock_commits_response1, mock_commits_response2]
        
        # Call the function
        result = get_repos("testuser")
        
        # Verify the results
        expected = [("repo1", 2), ("repo2", 1)]
        self.assertEqual(result, expected)
        
        # Verify the API calls
        calls = [
            unittest.mock.call("https://api.github.com/users/testuser/repos"),
            unittest.mock.call("https://api.github.com/repos/testuser/repo1/commits"),
            unittest.mock.call("https://api.github.com/repos/testuser/repo2/commits")
        ]
        mock_get.assert_has_calls(calls)
    
    @patch('github_api.requests.get')
    def test_get_repos_user_not_found(self, mock_get):
        # Mock a 404 response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_repos("nonexistentuser")
        
        # Verify empty result
        self.assertEqual(result, [])
    
    # Add more tests as needed

if __name__ == "__main__":
    unittest.main()
  
