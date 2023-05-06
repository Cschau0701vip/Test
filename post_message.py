from github import Github
from github import GithubException
import os

# Get the access token from environment variables
access_token = os.environ['ACCESS_TOKEN']

# Create a PyGithub instance
g = Github(access_token)

# Get the repository where the pull request was submitted
owner = 'Cschau0701vip'
repo_name = 'Test'
repo = g.get_repo(f"{owner}/{repo_name}")

# Get the pull request object
pull_request_number = int(os.environ['PR_NUMBER'])
pull_request = repo.get_pull(pull_request_number)

# Post a message on the pull request
try:
    pull_request.create_issue_comment("<your message>")
    print("Message posted successfully.")
except GithubException as e:
    print(f"An error occurred: {e}")
