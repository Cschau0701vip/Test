import os
import base64
import github
from github import Github


async def main():

    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
    issue = os.environ['GITHUB_REF'].split('/')[-1]
    owner = os.environ['GITHUB_ACTOR']

    filename = 'chart.png'
    path = f'chart/{filename}'
    branch = os.environ['GITHUB_HEAD_REF']

    contents = base64.b64encode("Hello")
    try:
        repo.get_contents(path=path, ref=branch)
        message = 'Update chart in pull request'
        repo.update_file(path=path, message=message, content=contents, sha=contents.sha, branch=branch)
    except github.GithubException as e:
        if e.status == 404:
            message = 'Add chart to pull request'
            repo.create_file(path=path, message=message, content=contents, branch=branch)
        else:
            raise e

    pull_request = repo.get_pull(int(issue.split('/')[-1]))
    review_comment = f'![chart](https://raw.githubusercontent.com/{owner}/{repo.name}/{branch}/{path})'
    pull_request.create_review_comment(body=review_comment)

if __name__ == '__main__':
    main()
