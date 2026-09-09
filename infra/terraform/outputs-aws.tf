output "ecr_repository_url" {
  description = "URL of the ECR repository used for application images."
  value       = aws_ecr_repository.app.repository_url
}

output "github_actions_ecr_role_arn" {
  description = "IAM role ARN assumed by GitHub Actions through OIDC."
  value       = aws_iam_role.github_actions_ecr.arn
}
