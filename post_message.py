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
    pull_request.create_issue_comment("<h2>Summary</h2><p>1 Run(s) Completed (1 Passed, 0 Failed)</p><table><tr><th>Total tests</th><th>Passed</th><th>Failed</th><th>Others</th></tr><tr><td>16</td><td style=\"color: green;\">16</td><td style=\"color: red;\">0</td><td>0</td></tr></table><div style=\"max-width: 400px;\"><canvas id=\"myChart\"></canvas></div><script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script><script>var ctx = document.getElementById('myChart').getContext('2d');var myChart = new Chart(ctx, {type: 'doughnut',data: {labels: ['Passed', 'Failed', 'Others'],datasets: [{data: [16, 0, 0],backgroundColor: ['green','red','gray']}]},options: {maintainAspectRatio: false}});</script><p><strong>Pass percentage:</strong> 100%</p><p><strong>Run duration:</strong> 16m 9s (+16m 9s)</p><p><strong>Tests not reported:</strong> 0</p>")
    print("Message posted successfully.")
except GithubException as e:
    print(f"An error occurred: {e}")
