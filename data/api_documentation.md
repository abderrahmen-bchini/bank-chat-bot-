# Wifak Bank - API Developer Documentation

**API Version:** v1.2.0  
**Base URL:** `https://api.wifakbank.com/v1`  
**Contact Support:** `api-support@wifakbank.com`  

---

## 1. Authentication and Security
All requests to the Wifak Bank API must be authenticated using an API Key or a Bearer Token.

### 1.1 API Key Authentication
Pass your private API key in the custom header `X-Bank-API-Key`.
```http
X-Bank-API-Key: otb_live_8f3a9b1c7d2e4f0a
```

### 1.2 Rate Limiting
To ensure system stability, rate limiting is applied:
* **Rate Limit:** **100 requests per minute** per API key/IP address.
* **Exceeded Limit:** Returns HTTP status code `429 Too Many Requests`.
* **Headers Returned:**
  * `X-RateLimit-Limit`: The total allowed requests per window (100).
  * `X-RateLimit-Remaining`: The number of requests left in the current 1-minute window.
  * `X-RateLimit-Reset`: The UNIX timestamp when the current window resets.

---

## 2. API Endpoints

### 2.1 Get Account Details
Retrieve details for a specific bank account.

* **Endpoint:** `GET /accounts/{account_id}`
* **Headers:** `X-Bank-API-Key: <your_key>`
* **Sample Response (200 OK):**
```json
{
  "account_id": "act_88329910",
  "client_id": "cli_449201",
  "account_type": "checking",
  "currency": "USD",
  "balance": 14250.75,
  "status": "active",
  "created_at": "2024-05-12T10:30:00Z"
}
```

### 2.2 List Transactions
List recent transactions for a specific account.

* **Endpoint:** `GET /accounts/{account_id}/transactions`
* **Query Parameters:**
  * `limit` (optional): Maximum number of transactions to return (default: 20, max: 100).
  * `offset` (optional): Offset for pagination.
* **Sample Response (200 OK):**
```json
{
  "account_id": "act_88329910",
  "transactions": [
    {
      "transaction_id": "tx_992011",
      "amount": -45.50,
      "type": "debit",
      "description": "Starbucks Coffee Chicago",
      "status": "completed",
      "timestamp": "2026-03-01T08:45:00Z"
    },
    {
      "transaction_id": "tx_992012",
      "amount": 2500.00,
      "type": "credit",
      "description": "Direct Deposit Salary OTB",
      "status": "completed",
      "timestamp": "2026-03-01T09:00:00Z"
    }
  ]
}
```

### 2.3 Initiate Bank Transfer
Transfer funds from a local account to an external or internal account.

* **Endpoint:** `POST /transfers`
* **Request Body (JSON):**
```json
{
  "source_account_id": "act_88329910",
  "destination_iban": "US89303000112233445566",
  "destination_bank_code": "CHASUS33XXX",
  "amount": 500.00,
  "currency": "USD",
  "description": "Monthly Rent Payment"
}
```
* **Sample Response (201 Created):**
```json
{
  "transfer_id": "tr_7718290",
  "status": "pending_approval",
  "reference_number": "OTB-9988221",
  "estimated_delivery": "2026-03-02T12:00:00Z"
}
```

---

## 3. Error Handling
Wifak Bank API uses standard HTTP response codes to indicate success or failure.

| Status Code | Meaning | Description |
| :--- | :--- | :--- |
| **200** | OK | Request completed successfully. |
| **210** | Created | Resource successfully created. |
| **400** | Bad Request | Missing or invalid parameters in request payload. |
| **401** | Unauthorized | Missing or invalid API key. |
| **403** | Forbidden | API key is valid but does not have permission to access the resource. |
| **429** | Too Many Requests | Rate limit exceeded. Slow down your calls. |
| **500** | Internal Error | An error occurred on Wifak Bank's servers. Contact support. |
