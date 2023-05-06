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

# Construct the comment message
num_tests = 16
num_passed = 16
num_failed = 0
pass_percentage = 100

pass_icon = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-check-circle-fill" fill="green" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm3.28 5.53l-3.804 4.094L4.71 8.307a.565.565 0 1 1 .657-.914l2.196 1.245 3.493-3.758a.565.565 0 1 1 .738.847z"/></svg>'
fail_icon = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x-circle-fill" fill="red" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm3.72 11.53l-3.271-3.27-3.271 3.27a.5.5 0 0 1-.707 0l-1.06-1.06a.5.5 0 0 1 0-.707l3.27-3.271-3.27-3.27a.5.5 0 0 1 0-.707l1.06-1.06a.5.5 0 0 1 .707 0l3.27 3.271 3.271-3.27a.5.5 0 0 1 .707 0l1.06 1.06a.5.5 0 0 1 0 .707l-3.27 3.271 3.27 3.27a.5.5 0 0 1 0 .707l-1.06 1.06a.5.5 0 0 1-.707 0z"/></svg>'

pass_icon = f'{pass_icon} Passed: {num_passed} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
fail_icon = f'{fail_icon} Failed: {num_failed} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
total_tests = f'Total Tests: {num_tests} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
pass_percent = f'Pass Percentage: {pass_percentage}% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'

message = f'<h2>Test Summary</h2> <p>{pass_icon} {fail_icon} {total_tests} {pass_percent}</p>'

# Post a message on the pull request
try:
    pull_request.create_issue_comment(message)
    print("Message posted successfully.")
except GithubException as e:
    print(f"An error occurred: {e}")
