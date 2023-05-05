import os
import base64
import github
from github import Github
import chartjs_node_canvas


async def main():
    data = {
        'labels': ['Passed', 'Failed', 'Others'],
        'datasets': [{
            'data': [16, 0, 0],
            'backgroundColor': ['#4CAF50', '#F44336', '#9E9E9E']
        }]
    }

    width = 400
    height = 400
    chart_callback = lambda chartjs: chartjs.defaults.global_.update({
        'responsive': True,
        'maintainAspectRatio': False
    })
    canvas = chartjs_node_canvas.Canvas(width=width, height=height, chart_callback=chart_callback)

    chart = await canvas.render_to_buffer({
        'type': 'pie',
        'data': data
    })

    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
    issue = os.environ['GITHUB_REF'].split('/')[-1]
    owner = os.environ['GITHUB_ACTOR']

    filename = 'chart.png'
    path = f'chart/{filename}'
    branch = os.environ['GITHUB_HEAD_REF']

    contents = base64.b64encode(chart.getvalue()).decode()
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
