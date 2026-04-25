variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "project-35d5c8cd-c2c7-40ef-9e5"
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
  description = "Project Name"
  type        = string
  default     = "ai-knowledge-base-gcp"
}
