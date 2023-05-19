from github import Github
from github import GithubException
import os
    
import glob
import xml.etree.ElementTree as ET

# Get the access token from environment variables
access_token = os.environ['ACCESS_TOKEN']

# Create a PyGithub instance
g = Github(access_token)
file_path = glob.glob('./*.xml')
print(file_path)
if(len(file_path) > 0):
    tree = ET.parse(file_path[0]) #/Users/chetanchaudhari/Downloads/results/test_id_209506257/9648608_Samsung_Galaxy_S21_Ultra__1_-CAI-API31-9648608_TEST-all.xml')
    root = tree.getroot()

    # Get the number of testsuites
    num_testsuite = len(root.findall('.')) #len(root.findall('testsuite'))

    # Print the result
    print("Number of testsuite:", num_testsuite)

    failures_total = 0
    skipped_total = 0
    tests_total = 0
    total_time = 0

    for testsuite in root.iter('testsuite'):
        failures = int(testsuite.get('failures'))
        skipped = int(testsuite.get('skipped'))
        tests = int(testsuite.get('tests'))
        time = 0
        # for test in testsuite.iter('testcase'):
        time +=  float(testsuite.get('time'))

        failures_total += failures
        skipped_total += 0 #skipped
        tests_total += tests
        total_time += time

    minutes = int(total_time / 60)
    seconds = round(total_time % 60, 2)

    # Get the repository where the pull request was submitted
    owner = 'Cschau0701vip'
    repo_name = 'Test'
    repo = g.get_repo(f"{owner}/{repo_name}")

    # Get the pull request object
    pull_request_number = int(os.environ['PR_NUMBER'])
    pull_request = repo.get_pull(pull_request_number)

    # Construct the comment message
    total_runs = num_testsuite #1
    pass_runs = num_testsuite #1
    fail_runs = num_testsuite - num_testsuite
    num_tests = tests_total #16
    num_passed = tests_total - failures_total - skipped_total #16
    num_failed = failures_total #0
    num_others = skipped_total #0
    pass_percentage = tests_total / num_passed * 100 #100
    test_not_reported = skipped_total #0
    time_duration = f'{minutes}m \\ {seconds}s'

    messageBody = f'## UI Tests Summary\n\n'
    messageBody += f'**{total_runs}** Run(s) Completed (${{\color{{green}} {pass_runs} \ Passed}}$, ${{\color{{red}}{fail_runs} \ Failed}}$)\n\n'
    messageBody += f'| Total tests | ✅ Passed | ❌ Failed | 🗃️ Others |\n'
    messageBody += f'| -----------| ------ | ------ | ------ |\n'
    messageBody += f'| $${{\color{{black}}{num_tests}}}$$        |  $${{\color{{green}}{num_passed}}}$$  | $${{\color{{red}} {num_failed}}}$$     | $${{\color{{purple}}{num_others}}}$$      |\n\n'
    messageBody += f'✅ Pass percentage: ${{\color{{green}}{pass_percentage} ﹪}}$\n\n'
    messageBody += f'⏱️ Run duration: ${{\color{{black}} {time_duration} }}$\n\n'
    messageBody += f'👾 Tests not reported:  ${{\color{{purple}} {test_not_reported} }}$'
    print(messageBody)
    
    # Post a message on the pull request
    try:
        pull_request.create_issue_comment(messageBody)
        print("Message posted successfully.")
    except GithubException as e:
        print(f"An error occurred: {e}")
