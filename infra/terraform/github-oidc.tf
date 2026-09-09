variable "github_oidc_subject_prefix" {
  description = "GitHub OIDC subject prefix for the AI Job Platform repository."
  type        = string

  validation {
    condition     = can(regex("^repo:[^:]+/[^:]+$", var.github_oidc_subject_prefix))
    error_message = "github_oidc_subject_prefix must be a valid GitHub repository OIDC subject prefix."
  }
}

locals {
  github_oidc_main_subject = "${var.github_oidc_subject_prefix}:ref:refs/heads/main"
}

resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com",
  ]
}

data "aws_iam_policy_document" "github_actions_assume_role" {
  statement {
    sid    = "GitHubActionsAssumeRole"
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]

    principals {
      type = "Federated"

      identifiers = [
        aws_iam_openid_connect_provider.github_actions.arn,
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"

      values = [
        "sts.amazonaws.com",
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"

      values = [
        local.github_oidc_main_subject,
      ]
    }
  }
}

resource "aws_iam_role" "github_actions_ecr" {
  name        = "${local.name_prefix}-github-ecr-publisher"
  description = "Allows the AI Job Platform GitHub Actions workflow to publish images to ECR."

  assume_role_policy = data.aws_iam_policy_document.github_actions_assume_role.json

  max_session_duration = 3600
}

data "aws_iam_policy_document" "github_actions_ecr_publish" {
  statement {
    sid    = "EcrAuthentication"
    effect = "Allow"

    actions = [
      "ecr:GetAuthorizationToken",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    sid    = "PublishApplicationImage"
    effect = "Allow"

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:PutImage",
    ]

    resources = [
      aws_ecr_repository.app.arn,
    ]
  }
}

resource "aws_iam_role_policy" "github_actions_ecr_publish" {
  name = "${local.name_prefix}-ecr-publish"

  role   = aws_iam_role.github_actions_ecr.id
  policy = data.aws_iam_policy_document.github_actions_ecr_publish.json
}
