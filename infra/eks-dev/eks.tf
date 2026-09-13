# EKS 1.28 and later encrypt all Kubernetes API data by default with an
# AWS-owned KMS key. A customer-managed key is not required for this temporary
# development environment.
# This temporary cluster keeps private endpoint access enabled and restricts
# public administration to the single-host CIDR validated by admin_cidr.
# trivy:ignore:AWS-0039 trivy:ignore:AWS-0040
resource "aws_eks_cluster" "this" {
  name     = local.cluster_name
  role_arn = aws_iam_role.eks_cluster.arn
  version  = var.cluster_version

  access_config {
    authentication_mode                         = "API"
    bootstrap_cluster_creator_admin_permissions = false
  }

  upgrade_policy {
    support_type = "STANDARD"
  }

  vpc_config {
    subnet_ids = [
      for subnet in aws_subnet.public : subnet.id
    ]

    endpoint_private_access = true
    endpoint_public_access  = true

    public_access_cidrs = [
      var.admin_cidr
    ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster
  ]
}
