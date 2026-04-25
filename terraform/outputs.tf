output "vpc_name" {
  description = "VPC Network Name"
  value       = google_compute_network.vpc.name
}

output "cluster_name" {
  description = "GKE Cluster Name"
  value       = google_container_cluster.primary.name
}

output "storage_bucket" {
  description = "Cloud Storage Bucket Name"
  value       = google_storage_bucket.documents.name
}

output "artifact_registry" {
  description = "Artifact Registry URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_name}-repo"
}
