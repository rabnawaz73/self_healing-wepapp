variable "aws_region" {
  description = "AWS region where CloudRescue is deployed"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Resource name prefix"
  type        = string
  default     = "cloudrescue"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "image_uri" {
  description = "Immutable ECR image URI for the Lambda container"
  type        = string
  default     = ""
}

variable "app_version" {
  description = "Application version stored in the container"
  type        = string
  default     = "1.0"
}

variable "github_owner" {
  description = "GitHub account or organization allowed to assume the deployment role"
  type        = string
  default     = "rabnawaz73"
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the deployment role"
  type        = string
  default     = "self_healing-wepapp"
}

variable "github_branch" {
  description = "GitHub branch allowed to assume the deployment role"
  type        = string
  default     = "main"
}
