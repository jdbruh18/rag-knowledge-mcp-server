# Developer API Reference Guide

## REST Endpoints

### 1. User Management
- `GET /v1/users`: Retrieve paginated list of active users.
- `POST /v1/users`: Create a new user profile. Requires admin permission scope `users:write`.

### 2. Billing & Invoices
- `GET /v1/invoices/:id`: Fetch invoice details and PDF download links.
- `POST /v1/payments/charge`: Process payment transaction through Stripe gateway.

## Error Rate Limits
Requests exceeding 100 requests per minute per IP address will receive HTTP `429 Too Many Requests`.
