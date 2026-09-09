#!/usr/bin/env bash

aws_dev_session() {
  export AWS_PROFILE="ai-job-platform-dev"
  export AWS_REGION="us-east-1"
  export AWS_DEFAULT_REGION="$AWS_REGION"

  echo "Checking AWS authentication..."

  if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo "AWS session expired. Starting login..."

    aws login --profile "$AWS_PROFILE" || return 1
  fi

  local account_id

  account_id="$(
    aws sts get-caller-identity \
      --query Account \
      --output text
  )" || return 1

  if [[ ! "$account_id" =~ ^[0-9]{12}$ ]]; then
    echo "Invalid AWS account ID"
    return 1
  fi

  local github_oidc_subject_prefix

  github_oidc_subject_prefix="$(
    curl --fail --silent --show-error \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2026-03-10" \
      "https://api.github.com/repos/SamehYahia/ai-job-platform/actions/oidc/customization/sub" \
      | python3 -c 'import json, sys; print(json.load(sys.stdin)["sub_claim_prefix"])'
  )" || return 1

  if [[ ! "$github_oidc_subject_prefix" =~ ^repo:.+/.+$ ]]; then
    echo "Invalid GitHub OIDC subject prefix"
    return 1
  fi

  export AWS_ACCOUNT_ID="$account_id"
  export TF_VAR_aws_account_id="$account_id"
  export TF_STATE_BUCKET="ai-job-platform-tfstate-$account_id"
  export TF_VAR_github_oidc_subject_prefix="$github_oidc_subject_prefix"

  echo "AWS development session ready."
  echo "Profile: $AWS_PROFILE"
  echo "Region: $AWS_REGION"
  echo "GitHub OIDC subject: configured"
}

aws_dev_session
