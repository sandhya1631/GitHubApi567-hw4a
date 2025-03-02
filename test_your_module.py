import unittest
from unittest.mock import patch, Mock
import json
from your_module import get_repo_info, get_user_repos, get_repo_commits, count_user_commits

class TestGitHubAPI(unittest.TestCase):
    
    @patch('your_module.requests.get')
    def test_get_repo_info(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 12345,
            "name": "test-repo",
            "full_name": "test-user/test-repo",
            "private": False,
            "owner": {
                "login": "test-user",
                "id": 54321
            },
            "html_url": "https://github.com/test-user/test-repo",
            "description": "Test repository for mocking",
            "fork": False,
            "stargazers_count": 10,
            "watchers_count": 10,
            "language": "Python"
        }
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_repo_info("test-user", "test-repo")
        
        # Assertions
        self.assertEqual(result["name"], "test-repo")
        self.assertEqual(result["owner"]["login"], "test-user")
        self.assertEqual(result["stargazers_count"], 10)
        
        # Verify the mock was called with the expected URL
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/test-user/test-repo",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
    
    @patch('your_module.requests.get')
    def test_get_repo_info_error(self, mock_get):
        # Setup mock response for an error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Check that the function raises an exception
        with self.assertRaises(Exception):
            get_repo_info("test-user", "nonexistent-repo")
    
    @patch('your_module.requests.get')
    def test_get_user_repos(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"name": "repo1", "id": 1},
            {"name": "repo2", "id": 2},
            {"name": "repo3", "id": 3}
        ]
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_user_repos("test-user")
        
        # Assertions
        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        
        # Verify the mock was called with the expected URL
        mock_get.assert_called_once_with(
            "https://api.github.com/users/test-user/repos",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
    
    @patch('your_module.requests.get')
    def test_get_repo_commits(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "sha": "commit1",
                "commit": {"message": "First commit"}
            },
            {
                "sha": "commit2",
                "commit": {"message": "Second commit"}
            }
        ]
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_repo_commits("test-user", "test-repo")
        
        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["sha"], "commit1")
        self.assertEqual(result[1]["commit"]["message"], "Second commit")
        
        # Verify the mock was called with the expected URL
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/test-user/test-repo/commits",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
    
    @patch('your_module.get_user_repos')
    @patch('your_module.get_repo_commits')
    def test_count_user_commits(self, mock_get_repo_commits, mock_get_user_repos):
        # Setup mocks
        mock_get_user_repos.return_value = ["repo1", "repo2"]
        
        # Mock different responses for different repos
        def side_effect(username, repo):
            if repo == "repo1":
                return [{"sha": "a1"}, {"sha": "a2"}, {"sha": "a3"}]
            elif repo == "repo2":
                return [{"sha": "b1"}, {"sha": "b2"}]
            return []
            
        mock_get_repo_commits.side_effect = side_effect
        
        # Call the function
        result = count_user_commits("test-user")
        
        # Assertions
        self.assertEqual(result, {"repo1": 3, "repo2": 2})
        
        # Verify the mocks were called correctly
        mock_get_user_repos.assert_called_once_with("test-user")
        self.assertEqual(mock_get_repo_commits.call_count, 2)
    
    @patch('your_module.get_user_repos')
    @patch('your_module.get_repo_commits')
    def test_count_user_commits_with_error(self, mock_get_repo_commits, mock_get_user_repos):
        # Setup mocks
        mock_get_user_repos.return_value = ["repo1", "repo2", "repo3"]
        
        # Mock with an exception for one repo
        def side_effect(username, repo):
            if repo == "repo1":
                return [{"sha": "a1"}, {"sha": "a2"}]
            elif repo == "repo2":
                raise Exception("API error")
            elif repo == "repo3":
                return [{"sha": "c1"}]
            return []
            
        mock_get_repo_commits.side_effect = side_effect
        
        # Call the function
        result = count_user_commits("test-user")
        
        # Assertions
        self.assertEqual(result, {"repo1": 2, "repo2": 0, "repo3": 1})
        
        # Verify the mocks were called correctly
        mock_get_user_repos.assert_called_once_with("test-user")
        self.assertEqual(mock_get_repo_commits.call_count, 3)

if __name__ == '__main__':
    unittest.main()
