const artifactUrl = github.rest.actions.downloadArtifact({
  artifact_id: null,
  archive_format: 'zip'
});
const artifactLink = `[View Test Results](${artifactUrl})`;
const commentBody = `Test results for this pull request: ${artifactLink}`;
github.rest.issues.createComment({
  issue_number: context.issue.number,
  body: commentBody
});
