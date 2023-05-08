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

messageBody = f'## UI Tests Summary\n\n'
messageBody += '**1** Run(s) Completed (${{\color{{green}}1 \ Passed}}$, ${{\color{{red}}0 \ Failed}}$)\n\n'
messageBody += '| Total tests | ✅ Passed | ❌ Failed | 🗃️ Others |\n'
messageBody += '| -----------| ------ | ------ | ------ |\n'
messageBody += '| $${{\color{{green}}{num_tests}}}$$        |  $${{\color{{green}}{num_passed}}}$$  | $${{\color{{red}} {num_failed}}}$$     | $${{\color{{green}}0}}}}$$      |\n\n'
messageBody += '✅ Pass percentage: ${{\color{{green}}{pass_percentage} ﹪}}$\n\n'
messageBody += '⏱️ Run duration: ${{\color{{black}} 16m \\ 9s}}$\n\n'
messageBody += '👾 Tests not reported:  ${{\color{{purple}} 0 }}}$'

pass_icon = f'{pass_icon} Passed: {num_passed} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
fail_icon = f'{fail_icon} Failed: {num_failed} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
total_tests = f'Total Tests: {num_tests} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
pass_percent = f'Pass Percentage: {pass_percentage}% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'

message = f'<h2>Test Summary</h2> <p>{pass_icon} {fail_icon} {total_tests} {pass_percent}</p>'

# Post a message on the pull request
try:
    pull_request.create_issue_comment(messageBody)
    print("Message posted successfully.")
except GithubException as e:
    print(f"An error occurred: {e}")
