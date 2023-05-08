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
total_runs = 1
pass_runs = 1
fail_runs = 0
num_tests = 16
num_passed = 16
num_failed = 0
num_others = 0
pass_percentage = 100
test_not_reported = 0
time_duration = '16m \\ 9s'

messageBody = f'## UI Tests Summary\n\n'
messageBody += f'**{total_runs}** Run(s) Completed (${{\color{{green}} {pass_runs} \ Passed}}$, ${{\color{{red}}{fail_runs} \ Failed}}$)\n\n'
messageBody += f'| Total tests | ✅ Passed | ❌ Failed | 🗃️ Others |\n'
messageBody += f'| -----------| ------ | ------ | ------ |\n'
messageBody += f'| $${{\color{{black}}{num_tests}}}$$        |  $${{\color{{green}}{num_passed}}}$$  | $${{\color{{red}} {num_failed}}}$$     | $${{\color{{purple}}{num_others}}}$$      |\n\n'
messageBody += f'✅ Pass percentage: ${{\color{{green}}{pass_percentage} ﹪}}$\n\n'
messageBody += f'⏱️ Run duration: ${{\color{{black}} {time_duration} }}$\n\n'
messageBody += f'👾 Tests not reported:  ${{\color{{purple}} {test_not_reported} }}$'

# Post a message on the pull request
try:
    pull_request.create_issue_comment(messageBody)
    print("Message posted successfully.")
except GithubException as e:
    print(f"An error occurred: {e}")
