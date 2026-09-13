resource "aws_eks_node_group" "general" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${local.name_prefix}-general"
  node_role_arn   = aws_iam_role.eks_node.arn

  subnet_ids = [
    for subnet in aws_subnet.public : subnet.id
  ]

  version       = var.cluster_version
  ami_type      = "AL2023_x86_64_STANDARD"
  capacity_type = "ON_DEMAND"

  instance_types = [
    var.node_instance_type
  ]

  scaling_config {
    min_size     = 1
    desired_size = 1
    max_size     = 1
  }

  update_config {
    max_unavailable = 1
  }

  labels = {
    workload    = "general"
    environment = var.environment
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_node_worker,
    aws_iam_role_policy_attachment.eks_node_ecr,
    aws_iam_role_policy_attachment.eks_node_cni,
  ]
}
