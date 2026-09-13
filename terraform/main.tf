# FinGuard AI — Infrastructure as Code
# Reflects the actual deployed architecture: Cloud Run + Cloud SQL + Vertex AI
# (Earlier versions of this file targeted GKE; updated to match the real,
#  live deployment at https://finguard-ai-283915220530.us-central1.run.app)

# Enable required GCP APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "storage.googleapis.com",
    "secretmanager.googleapis.com",
    "aiplatform.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "compute.googleapis.com",
  ])
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

# ---------------------------------------------------------------------------
# Networking — dedicated VPC for FinGuard AI
# ---------------------------------------------------------------------------

resource "google_compute_network" "vpc" {
  name                    = "${var.project_name}-vpc"
  auto_create_subnetworks = false
  depends_on              = [google_project_service.apis]
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_name}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
  private_ip_google_access = true
}

resource "google_compute_firewall" "allow_internal" {
  name    = "${var.project_name}-allow-internal"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  source_ranges = ["10.0.0.0/24"]
}

resource "google_compute_firewall" "deny_all_ingress" {
  name      = "${var.project_name}-deny-all-ingress"
  network   = google_compute_network.vpc.name
  priority  = 65534
  direction = "INGRESS"

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_global_address" "private_ip_range" {
  name          = "${var.project_name}-private-ip-range"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_range.name]
}

# ---------------------------------------------------------------------------
# Database — Cloud SQL (PostgreSQL)
# ---------------------------------------------------------------------------

resource "google_sql_database_instance" "finguard_db" {
  name             = "${var.project_name}-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled    = true
      private_network = google_compute_network.vpc.id
    }

    backup_configuration {
      enabled = true
    }
  }

  depends_on = [
    google_project_service.apis,
    google_service_networking_connection.private_vpc_connection,
  ]
}

resource "google_sql_database" "finguard" {
  name     = "finguard"
  instance = google_sql_database_instance.finguard_db.name
}

resource "google_sql_user" "app_user" {
  name     = "postgres"
  instance = google_sql_database_instance.finguard_db.name
  password = var.db_password
}

# ---------------------------------------------------------------------------
# Storage & Artifact Registry
# ---------------------------------------------------------------------------

resource "google_storage_bucket" "documents" {
  name          = "${var.project_name}-documents"
  location      = var.region
  force_destroy = true
  uniform_bucket_level_access = true
}

resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "${var.project_name}-repo"
  format        = "DOCKER"
  depends_on    = [google_project_service.apis]
}

# ---------------------------------------------------------------------------
# Secrets — database credentials, never stored in code
# ---------------------------------------------------------------------------

resource "google_secret_manager_secret" "db_url" {
  secret_id = "${var.project_name}-database-url"

  replication {
    auto {}
  }

  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret_version" "db_url_version" {
  secret      = google_secret_manager_secret.db_url.id
  secret_data = "postgresql://${google_sql_user.app_user.name}:${var.db_password}@/${google_sql_database.finguard.name}?host=/cloudsql/${google_sql_database_instance.finguard_db.connection_name}"
}

# ---------------------------------------------------------------------------
# IAM — dedicated service account, least-privilege roles
# ---------------------------------------------------------------------------

resource "google_service_account" "finguard_sa" {
  account_id   = "${var.project_name}-sa"
  display_name = "FinGuard AI Service Account"
}

resource "google_project_iam_member" "cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.finguard_sa.email}"
}

resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.finguard_sa.email}"
}

resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.finguard_sa.email}"
}

# ---------------------------------------------------------------------------
# Compute — Cloud Run (the actual, live deployment target)
# ---------------------------------------------------------------------------

resource "google_cloud_run_v2_service" "finguard_ai" {
  name     = var.project_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.finguard_sa.email

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_name}-repo/${var.project_name}:latest"

      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_url.secret_id
            version = "latest"
          }
        }
      }

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "VERTEX_AI_LOCATION"
        value = var.region
      }
    }

    vpc_access {
      network_interfaces {
        network    = google_compute_network.vpc.id
        subnetwork = google_compute_subnetwork.subnet.id
      }
      egress = "PRIVATE_RANGES_ONLY"
    }
  }

  depends_on = [
    google_project_service.apis,
    google_sql_database_instance.finguard_db,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "public_access" {
  location = google_cloud_run_v2_service.finguard_ai.location
  name     = google_cloud_run_v2_service.finguard_ai.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
