locals {
  name_prefix  = "${var.project_name}-${var.environment}"
  cluster_name = "${local.name_prefix}-eks"

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    Component   = "eks-dev"
    Lifecycle   = "ephemeral"
    ManagedBy   = "Terraform"
    Repository  = "ai-job-platform"
  }
}
