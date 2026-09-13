output "cluster_name" {
  description = "Name of the ephemeral Amazon EKS cluster."
  value       = aws_eks_cluster.this.name
}

output "cluster_version" {
  description = "Kubernetes version running on the Amazon EKS cluster."
  value       = aws_eks_cluster.this.version
}

output "vpc_id" {
  description = "VPC ID used by the ephemeral EKS environment."
  value       = aws_vpc.eks.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs used by the EKS environment."
  value = [
    for subnet in aws_subnet.public : subnet.id
  ]
}
