# FinGuard AI

**Built by [Eric Niamba](https://github.com/ericniamba) — Cloud Engineer · GCP ACE Certified · Austin, TX**

> AI-powered compliance intelligence for banks. Upload regulatory documents, ask questions in natural language, and get answers backed by a full audit trail, PII protection, and automated regulatory drift detection.

**Live Demo → http://34.55.52.205**

---

## What Makes This Different

Most AI knowledge base projects upload documents and answer questions. FinGuard AI was built for regulated financial institutions, where "the AI answered it" isn't enough — every answer needs to be provable, safe, and auditable.

| Feature | What It Does |
|---|---|
| **Query Provenance Ledger** | Every query, retrieved context, and answer is logged in a SHA-256 hash-chained audit trail. Any tampering with past records breaks the chain and is immediately detectable. |
| **Confidence-Gated Escalation** | Low-confidence answers are never guessed — they're automatically flagged for human compliance review instead. |
| **Regulatory Drift Detector** | Compares document versions over time and flags what changed, with automatic risk scoring (LOW/MEDIUM/HIGH) based on regulatory keyword analysis. |
| **Cross-Tenant Isolation** | Bank-grade data separation between tenants, tested against adversarial prompt-injection attempts at the database layer. |
| **Compliance Score Trend Dashboard** | Tracks cumulative regulatory risk over time as documents change, turning point-in-time compliance checks into a real trend. |
| **PII Redaction Firewall** | Sensitive data (SSNs, card numbers, account numbers, emails) is detected and redacted *before* it ever reaches the LLM — not after. |

---

## Architecture

## Architecture

User Request -> GCP Load Balancer -> VPC (GKE Cluster + Cloud SQL + Cloud Storage) -> Vertex AI Gemini

The backend runs as a 3-node GKE cluster inside a private VPC. Cloud SQL (PostgreSQL + pgvector) handles vector similarity search. Vertex AI Gemini sits outside the VPC as a Google-managed service, reached only after PII redaction has already run.

## Compliance Pipeline

1. User submits a question
2. PII Redaction Firewall scans and redacts sensitive data, logs the redaction event
3. Relevant document context is retrieved via pgvector
4. Vertex AI Gemini generates an answer with a self-reported confidence score
5. Low-confidence answers are flagged for human review instead of returned as-is
6. Every step is recorded in the hash-chained Query Provenance Ledger

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + TypeScript |
| Backend | FastAPI Python |
| AI Engine | Vertex AI Gemini |
| Database | Cloud SQL PostgreSQL + pgvector |
| Storage | Cloud Storage |
| Orchestration | GKE 3-node Kubernetes cluster |
| IaC | Terraform |
| CI/CD | Cloud Build + GitHub |
| Security | IAM + Secret Manager + PII Redaction |

## About the Author

**Eric Niamba** — Cloud Engineer, Austin, TX

- Apple + Banking Infrastructure background
- GCP Associate Cloud Engineer (ACE) Certified
- GCP, Kubernetes, Terraform, IAM, VPC, Fintech Infrastructure

Connect: [github.com/ericniamba](https://github.com/ericniamba)
