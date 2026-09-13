# FinGuard AI — Terraform Infrastructure

This directory defines FinGuard AI's infrastructure as code: a dedicated VPC
with default-deny ingress, a private-IP Cloud SQL (PostgreSQL) instance, a
Cloud Run service running the FastAPI backend, Secret Manager for credentials,
and a least-privilege service account with only the three IAM roles the app
actually needs (Cloud SQL Client, Secret Accessor, Vertex AI User).

## Usage

```bash
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars with real values — this file is gitignored

terraform init
terraform plan
terraform apply
```

## Notes

- The live deployment (https://finguard-ai-283915220530.us-central1.run.app)
  was originally provisioned via `gcloud` CLI commands during initial
  development. This Terraform configuration codifies that same architecture
  as reusable, version-controlled infrastructure — the standard next step
  once a manually-built system's shape is proven out.
- `db_password` is marked `sensitive` and must be supplied via
  `terraform.tfvars` or `-var`, never hardcoded.
- The VPC includes an explicit default-deny ingress rule (priority 65534)
  as a defense-in-depth baseline, in addition to Cloud Run's own IAM-based
  access control.
