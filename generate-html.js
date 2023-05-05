const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');
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

  // Create and write HTML file
  const html = `
    <html>
      <head>
        <title>Test Summary</title>
      </head>
      <body>
        <h1>Test Summary</h1>
        <table>
          <tr>
            <th>Total tests</th>
            <th>Passed</th>
            <th>Failed</th>
            <th>Others</th>
          </tr>
          <tr>
            <td>16</td>
            <td>16</td>
            <td>0</td>
            <td>0</td>
          </tr>
        </table>
        <canvas id="myChart"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
          const data = ${JSON.stringify(data)};
          const ctx = document.getElementById('myChart').getContext('2d');
          const myChart = new Chart(ctx, {
            type: 'pie',
            data: data
          });
        </script>
      </body>
    </html>
  `;
  fs.writeFileSync('test-summary.html', html);

  // Upload HTML file to artifacts
  const artifactName = 'test-summary';
  const artifactPath = './test-summary.html';
  const artifactClient = github.getOctokit(process.env.GITHUB_TOKEN);
  const uploadUrl = await artifactClient.actions.createArtifact({
    owner: github.context.repo.owner,
    repo: github.context.repo.repo,
    name: artifactName,
    // Archive the HTML file in a zip
    archive_format: 'zip',
    archive_file: artifactName + '.zip',
  }).then(response => response.data.upload_url);
  const fileContent = fs.readFileSync(artifactPath);
  await artifactClient.rest.artifacts.uploadArtifact({
    url: uploadUrl,
    headers: {
      'content-type': 'application/octet-stream',
      'content-length': Buffer.byteLength(fileContent)
    },
    name: artifactName,
    file: artifactPath,
    // Mark the artifact as complete so that it can be downloaded
    // even if the job fails
    complete: true
  });

  // Create review comment with HTML file link
  const prNumber = github.context.payload.pull_request.number;
  const comment = `Test summary is available [here](https://github.com/${github.context.repo.owner}/${github.context.repo.repo}/actions/artifacts/${prNumber}/download)`;
  await artifactClient.pulls.createReview({
    owner: github.context.repo.owner,
    repo: github.context.repo.repo,
    pull_number: prNumber,
    event: 'COMMENT',
    body: comment
  })
}
