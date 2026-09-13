variable "aws_region" {
  description = "AWS Region used for the ephemeral EKS environment."
  type        = string
  default     = "us-east-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]+$", var.aws_region))
    error_message = "aws_region must be a valid AWS Region name."
  }
}

variable "aws_account_id" {
  description = "Expected AWS account ID used as a safety guard."
  type        = string

  validation {
    condition     = can(regex("^[0-9]{12}$", var.aws_account_id))
    error_message = "aws_account_id must contain exactly 12 digits."
  }
}

variable "project_name" {
  description = "Project identifier used for naming and tagging."
  type        = string
  default     = "ai-job-platform"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.environment))
    error_message = "environment may contain only lowercase letters, numbers, and hyphens."
  }
}

variable "cluster_version" {
  description = "Kubernetes minor version used by Amazon EKS."
  type        = string
  default     = "1.35"
}

variable "admin_cidr" {
  description = "Single public IPv4 CIDR allowed to reach the public EKS API endpoint."
  type        = string

  validation {
    condition = (
      can(cidrhost(var.admin_cidr, 0)) &&
      can(regex("/32$", var.admin_cidr))
    )
    error_message = "admin_cidr must be a valid single-host IPv4 /32 CIDR."
  }
}

variable "admin_principal_arn" {
  description = "IAM user or role granted administrative Kubernetes access through an EKS access entry."
  type        = string

  validation {
    condition = can(regex(
      "^arn:aws:iam::[0-9]{12}:(user|role)/.+$",
      var.admin_principal_arn
    ))
    error_message = "admin_principal_arn must be an IAM user or role ARN."
  }
}
variable "vpc_cidr" {
  description = "CIDR block allocated to the ephemeral EKS VPC."
  type        = string
  default     = "10.20.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "vpc_cidr must be a valid IPv4 CIDR block."
  }
}

variable "public_subnets" {
  description = "Public subnet configuration for the ephemeral EKS environment."

  type = map(object({
    cidr_block        = string
    availability_zone = string
  }))

  default = {
    "public-a" = {
      cidr_block        = "10.20.0.0/20"
      availability_zone = "us-east-1a"
    }

    "public-b" = {
      cidr_block        = "10.20.16.0/20"
      availability_zone = "us-east-1b"
    }
  }
}
variable "node_instance_type" {
  description = "EC2 instance type used by the ephemeral EKS managed node group."
  type        = string
  default     = "t3.medium"
}
