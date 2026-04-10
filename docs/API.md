# API Documentation

## Overview
This is the REST API documentation for the Bank Chatbot. The API is built with FastAPI and uses JWT for authentication.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints require a JWT token in the `Authorization` header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Authentication

#### POST /auth/login
Login with email and password.

**Request**:
```json
{
    "email": "user@bank.com",
    "password": "secure_password"
}
```

**Response** (200):
```json
{
    "access_token": "eyJhbGciOiJIUzI1...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
        "id": "uuid",
        "email": "user@bank.com",
        "role": "employee"
    }
}
```

### Documents

#### POST /documents/upload
Upload a document for ingestion.

**Parameters**:
- `file` (file, required): PDF, DOCX, or TXT file
- `access_level` (string, optional): Default "employee"

**Response** (201):
```json
{
    "id": "doc_001",
    "name": "Procedure_Manual.pdf",
    "chunks": 42,
    "status": "processing",
    "uploaded_at": "2025-04-10T14:30:00Z"
}
```

#### GET /documents
List all accessible documents.

**Query Parameters**:
- `skip` (int, default 0)
- `limit` (int, default 10)
- `search` (string, optional)

**Response** (200):
```json
{
    "total": 15,
    "items": [
        {
            "id": "doc_001",
            "name": "Procedure Manual",
            "uploaded_at": "2025-04-10T14:30:00Z",
            "chunks": 42
        }
    ]
}
```

### Queries (Q&A)

#### POST /query
Submit a question to the chatbot.

**Request**:
```json
{
    "question": "What is the process for employee onboarding?",
    "top_k": 5
}
```

**Response** (200):
```json
{
    "id": "query_001",
    "question": "What is the process for employee onboarding?",
    "answer": "The employee onboarding process involves...",
    "sources": [
        {
            "document_id": "doc_001",
            "document_name": "HR Procedures",
            "chunk_index": 5,
            "relevance_score": 0.94
        }
    ],
    "confidence": 0.92,
    "response_time_ms": 1250,
    "created_at": "2025-04-10T14:35:00Z"
}
```

#### GET /query/{query_id}
Retrieve a previous query and answer.

**Response** (200):
```json
{
    "id": "query_001",
    "question": "...",
    "answer": "...",
    "sources": [...],
    "confidence": 0.92
}
```

### Admin

#### GET /admin/logs
Get audit logs (admin only).

**Query Parameters**:
- `skip` (int, default 0)
- `limit` (int, default 50)
- `user_id` (string, optional)
- `action` (string, optional)

**Response** (200):
```json
{
    "total": 150,
    "items": [
        {
            "id": "log_001",
            "user_id": "user_001",
            "action": "query",
            "timestamp": "2025-04-10T14:35:00Z",
            "details": {...}
        }
    ]
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid request format",
    "detail": "Field 'email' is required"
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid or expired token",
    "detail": "Token expired at 2025-04-10T14:30:00Z"
}
```

### 403 Forbidden
```json
{
    "error": "Access denied",
    "detail": "You do not have permission to access this document"
}
```

### 404 Not Found
```json
{
    "error": "Resource not found",
    "detail": "Document with ID 'doc_999' does not exist"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error",
    "detail": "An unexpected error occurred. Please try again later."
}
```

## Rate Limiting
- 100 requests per minute per user
- 1000 requests per hour per user

---

For more details, visit: http://localhost:8000/docs (Swagger UI)
