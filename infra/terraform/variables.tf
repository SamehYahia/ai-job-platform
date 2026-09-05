variable "aws_region" {
  description = "AWS Region used for the project infrastructure."
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