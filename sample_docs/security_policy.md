# Enterprise Security & Compliance Policy

## Data Encryption Standard
- All sensitive customer data must be encrypted at rest using AES-256 encryption keys managed in AWS KMS.
- In-transit communication requires TLS 1.3 encryption across all public and internal endpoints.

## Authentication & Authorization
- **OAuth 2.0 / OpenID Connect**: All external requests must be authenticated via bearer JWT tokens.
- **RBAC**: Service accounts must adhere to the principle of least privilege. Database write access is restricted to primary services.

## Vulnerability Scans & Backups
- Nightly automated static analysis (SAST) and container vulnerability scanning are mandatory.
- Daily incremental backups and weekly full database snapshots are stored in multi-region cold storage.
