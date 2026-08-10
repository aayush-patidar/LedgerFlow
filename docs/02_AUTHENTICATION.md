# Chapter 02 — Authentication & Authorization

## Objective

Make authentication and authorization production-ready.

---

## Requirements

### Authentication

- JWT Bearer authentication
- Secure password hashing
- Token expiration
- Token validation
- Invalid token rejection

### Authorization

Protected endpoints must use:

Depends(get_user)

Users may only access resources they own.

---

## User Endpoint

Implement:

GET /user/me

Returns the authenticated user's safe public information.

Never return:

- password
- password hash
- secret
- JWT

---

## Authorization Rules

A user cannot:

- access another user's wallet
- modify another user's wallet
- initiate unauthorized operations
- access private transaction information belonging to another user

---

## Security

Authentication errors must not leak sensitive information.

JWT verification failures return 401.

---

## Definition of Done

Authenticated user can access /user/me.

Unauthenticated request returns 401.

Invalid token returns 401.

User cannot access another user's resources.