# AI Knowledge Base on GCP
Built by Eric Niamba — Cloud Engineer

## Live Demo
http://34.55.52.205

A production-grade AI-powered knowledge base running live on Google Kubernetes Engine. Upload any document and ask questions using natural language — powered by Google Vertex AI.

## Tech Stack
- Frontend: Next.js + TypeScript
- Backend: FastAPI Python
- AI: Vertex AI Gemini — Google enterprise AI
- Database: Cloud SQL + pgvector
- Storage: Cloud Storage
- Orchestration: GKE Kubernetes — 3 node cluster
- Infrastructure: Terraform — all infra as code
- CI/CD: Cloud Build + GitHub
- Security: IAM + Secret Manager
- Networking: VPC + Firewall Rules

## GCP Services Used
- Google Kubernetes Engine GKE — 3-node cluster running all services
- Vertex AI — Google enterprise AI for embeddings and LLM
- Cloud Storage — Document upload and storage
- Cloud SQL — Managed PostgreSQL with pgvector extension
- Artifact Registry — Docker image storage
- Cloud Build — CI/CD pipeline
- Secret Manager — Secure API key storage
- VPC and Firewall — Private networking and security
- Cloud Monitoring — Observability and alerting
- IAM — Role-based access control

## Project Structure
- frontend/ — Next.js application
- backend/ — FastAPI application with Vertex AI integration
- terraform/ — All GCP infrastructure as code
- kubernetes/ — Kubernetes deployment manifests
- docs/ — Documentation

## Setup Instructions
Prerequisites: Google Cloud account, gcloud CLI, Terraform, kubectl, Docker

Deploy Infrastructure:
cd terraform
terraform init
terraform apply

Deploy Application:
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml

## Author
Eric Niamba — Cloud Engineer
GitHub: https://github.com/ericniamba
Live App: http://34.55.52.205
# CI/CD Pipeline Active
