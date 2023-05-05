const core = require('@actions/core');
const github = require('@actions/github');
const { CanvasRenderService } = require('chartjs-node-canvas');

async function main() {
  const data = {
    labels: ['Passed', 'Failed', 'Others'],
    datasets: [{
      data: [16, 0, 0],
      backgroundColor: ['#4CAF50', '#F44336', '#9E9E9E']
    }]
  };

  const width = 400;
  const height = 400;
  const chartCallback = (ChartJS) => {
    ChartJS.defaults.global.responsive = true;
    ChartJS.defaults.global.maintainAspectRatio = false;
  };
  const canvasRenderService = new CanvasRenderService(width, height, chartCallback);

  const image = await canvasRenderService.renderToBuffer({
    type: 'pie',
    data: data
  });

  const octokit = github.getOctokit(${{ secrets.GITHUB_TOKEN }});
  const { owner, repo, number } = github.context.issue;
  const filename = 'chart.png';

  const uploadUrl = await octokit.repos.createOrUpdateFileContents({
    owner: owner,
    repo: repo,
    path: `chart/${filename}`,
    message: 'Add chart to pull request',
    content: image.toString('base64'),
    branch: github.context.payload.pull_request.head.ref,
  }).then(response => response.data.content.upload_url);

  await octokit.pulls.createReview({
    owner: owner,
    repo: repo,
    pull_number: number,
    body: `![chart](${uploadUrl})`
  });
}

main().catch(error => {
  core.setFailed(error.message);
});
