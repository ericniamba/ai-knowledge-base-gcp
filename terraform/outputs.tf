output "vpc_name" {
  description = "VPC Network Name"
  value       = google_compute_network.vpc.name
}

output "cloud_run_url" {
  description = "Live URL of the deployed FinGuard AI service"
  value       = google_cloud_run_v2_service.finguard_ai.uri
}

output "cloud_sql_connection_name" {
  description = "Cloud SQL instance connection name (used for Cloud Run's Unix socket connection)"
  value       = google_sql_database_instance.finguard_db.connection_name
}

output "storage_bucket" {
  description = "Cloud Storage Bucket Name"
  value       = google_storage_bucket.documents.name
}

output "artifact_registry" {
  description = "Artifact Registry URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_name}-repo"
}

output "service_account_email" {
  description = "Email of the dedicated FinGuard AI service account"
  value       = google_service_account.finguard_sa.email
}
