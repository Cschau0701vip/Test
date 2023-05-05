script: const github1 = require('@actions/github');
const octokit = new github1.GitHub(process.env.GITHUB_TOKEN, {baseUrl: 'https://github.com/api/v3'});
const artifactUrl = await github1.rest.actions.downloadArtifact({
  artifact_id: null,
  archive_format: 'zip'
});
const artifactLink = `[View Test Results](${artifactUrl})`;
const commentBody = `Test results for this pull request: ${artifactLink}`;
await github1.rest.issues.createComment({
  issue_number: context.issue.number,
  body: commentBody
});
