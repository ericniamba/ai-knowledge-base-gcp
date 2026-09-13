variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "handsonproject-485816"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-central1-a"
}

variable "project_name" {
  description = "Project Name (used as a prefix for all resource names)"
  type        = string
  default     = "finguard-ai"
}

variable "db_password" {
  description = "Password for the Cloud SQL postgres user. Pass via terraform.tfvars or -var, never commit a real value."
  type        = string
  sensitive   = true
}
