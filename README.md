# RDS Ping

A simple Flask application to test RDS connectivity using IAM authentication.

## Endpoints

### `GET /reachability/app`
Health check endpoint for the application.

**Response:** `ok`

### `GET /reachability/db`
Tests RDS database connectivity using IAM authentication.

**Query Parameters:**
- `connect_to` (optional) - Override the database name to connect to

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-10-26 12:00:00"
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Error 1"
}
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DB_ENDPOINT` | Yes | - | RDS endpoint URL |
| `DB_USER` | Yes | - | Database username |
| `DB_NAME` | No | `mydb` | Default database name |
| `DB_PORT` | No | `5432` | Database port |
| `AWS_REGION` | No | `us-east-1` | AWS region |
| `AWS_PROFILE` | No | `default` | AWS credentials profile |
| `SSL_CERTIFICATE` | No | `SSLCERTIFICATE` | Path to SSL certificate |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
export DB_ENDPOINT="your-rds-endpoint.rds.amazonaws.com"
export DB_USER="your_username"
export DB_NAME="mydb"
export AWS_PROFILE="RDSCreds"

python app.py
```

## Testing

```bash
# Test application health
curl http://localhost:5000/reachability/app

# Test database connection with default database
curl http://localhost:5000/reachability/db

# Test database connection with specific database
curl http://localhost:5000/reachability/db?connect_to=testdb
```
