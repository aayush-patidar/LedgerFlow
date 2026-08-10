# Chapter 09 — Error Handling

Implement centralized application error handling.

---

# Standard Errors

400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
429 Too Many Requests
500 Internal Server Error

---

# Financial Errors

Insufficient balance

Wallet not found

Wallet inactive

Currency mismatch

Duplicate idempotency key

Invalid transfer

---

# Rules

Never expose:

stack traces
database errors
password information
JWT secrets
internal implementation details

Production responses must be safe.

---

# Definition of Done

Errors use consistent JSON structure.

Logs contain detailed internal information.

Clients receive safe messages.