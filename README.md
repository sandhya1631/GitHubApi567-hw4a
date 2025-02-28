# GitHubApi567-hw4a

Modularity for Better Testability
I structured the code into separate functions:
•	One function to fetch repositories.
•	Another function to fetch commit counts for each repository.
•	A main function to combine these results and format the output.
CircleCI Integration for Continuous Testing
To ensure the function runs correctly in different environments, I:
•	Added unit tests that run automatically in CircleCI.
•	Configured a .circleci/config.yml file to install dependencies and execute tests on every push.

