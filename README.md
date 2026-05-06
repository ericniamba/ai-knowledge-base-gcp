# AI Knowledge Base on GCP

![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![Vertex AI](https://img.shields.io/badge/Vertex_AI-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

**Built by [Eric Niamba](https://github.com/ericniamba) — Cloud Engineer · GCP ACE Certified · Austin, TX**

> A production-grade AI-powered knowledge base running live on Google Cloud.
> Upload any document. Ask questions in natural language. Get answers powered by Google Vertex AI.

🔴 **[Live Demo → http://34.55.52.205](http://34.55.52.205)**

---

## What This Project Demonstrates

| Skill Area | Implementation |
|---|---|
| **Infrastructure as Code** | 100% Terraform — VPC, GKE, Cloud SQL, IAM, Storage |
| **Container Orchestration** | GKE 3-node cluster with Kubernetes manifests |
| **AI/ML Integration** | Vertex AI Gemini for embeddings + LLM inference |
| **Security** | IAM least-privilege roles, Secret Manager, VPC firewall rules |
| **Networking** | Custom VPC, private subnets, firewall rules, external load balancer |
| **CI/CD** | Cloud Build pipeline triggered on GitHub push |
| **Observability** | Cloud Monitoring uptime checks every 60 seconds + email alerts |
| **Data** | Cloud SQL PostgreSQL + pgvector for vector similarity search |

---

## Architecture

\`\`\`
User Request
     │
     ▼
External IP (34.55.52.205)
     │
     ▼
GCP Load Balancer
     │
     ▼
┌─────────────────────────────────────────┐
│  VPC — Private Network                  │
│                                         │
│  ┌──────────────┐  ┌──────────────────┐ │
│  │  GKE Cluster │  │   Cloud SQL      │ │
│  │  (3 nodes)   │  │   PostgreSQL     │ │
│  │              │  │   + pgvector     │ │
│  │  frontend/   │  └──────────────────┘ │
│  │  backend     │                       │
│  │  pods        │  ┌──────────────────┐ │
│  └──────┬───────┘  │  Cloud Storage   │ │
│         │          │  (documents)     │ │
│         │          └──────────────────┘ │
└─────────┼───────────────────────────────┘
          │
          ▼
   Vertex AI (Gemini)
   [Google-managed, outside VPC]
\`\`\`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + TypeScript |
| Backend | FastAPI Python |
| AI Engine | Vertex AI Gemini |
| Database | Cloud SQL — PostgreSQL + pgvector |
| Storage | Cloud Storage |
| Orchestration | GKE 3-node Kubernetes cluster |
| IaC | Terraform |
| CI/CD | Cloud Build + GitHub |
| Security | IAM + Secret Manager |
| Networking | VPC + Firewall Rules |

---

## GCP Services Used

| Service | Purpose |
|---|---|
| Google Kubernetes Engine | 3-node cluster running all services |
| Vertex AI | Embeddings and LLM inference |
| Cloud SQL | Managed PostgreSQL with pgvector |
| Cloud Storage | Document upload and storage |
| Artifact Registry | Docker image storage |
| Cloud Build | CI/CD pipeline |
| Secret Manager | Secure API key storage |
| VPC + Firewall | Private networking and security |
| Cloud Monitoring | Uptime checks + alerting |
| IAM | Role-based access control |

---

## Project Structure

\`\`\`
ai-knowledge-base-gcp/
├── frontend/          # Next.js + TypeScript application
├── backend/           # FastAPI application with Vertex AI integration
├── terraform/         # All GCP infrastructure as code
│   ├── main.tf        # VPC, GKE cluster, Cloud SQL
│   ├── iam.tf         # Service accounts and IAM bindings
│   └── networking.tf  # Subnets, firewall rules
├── kubernetes/        # Kubernetes deployment manifests
└── docs/              # Architecture documentation
\`\`\`

---

## Deploy It Yourself

\`\`\`bash
# 1. Provision all GCP infrastructure
cd terraform
terraform init
terraform apply

# 2. Deploy application to GKE
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml

# 3. Verify
kubectl get pods
kubectl get services
\`\`\`

---

## About the Author

**Eric Niamba** — Cloud Engineer · Austin, TX

- 🏢 Apple + Banking Infrastructure background
- ☁️ GCP Associate Cloud Engineer (ACE) Certified
- 🏅 64 Cloud Badges on LinkedIn
- 🔧 GCP · Kubernetes · Terraform · IAM · VPC · Fintech Infrastructure

**Connect:**
- GitHub: [github.com/ericniamba](https://github.com/ericniamba)
- Live App: [http://34.55.52.205](http://34.55.52.205)
