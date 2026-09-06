locals {
  state_bucket_name = "${var.project_name}-tfstate-${data.aws_caller_identity.current.account_id}"

  common_tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
    Purpose   = "TerraformRemoteState"
  }
}