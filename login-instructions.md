# Login & Registration Implementation Guide

This document outlines the steps and requirements for adding login and registration functionality to the `Chatbot with RAG` application, following the project's architecture and conventions.

## Overview

The goal is to enable users to register and log in using their email, name, and password. Authentication will be handled using JWT (JSON Web Tokens) for secure session management. The implementation will cover both backend (API) and frontend (UI) integration.

## Backend (FastAPI)

### 1. Data Model
- Add a `User` model/schema with fields: `id`, `name`, `email`, `hashed_password`.
- Store users in a database (SQLite or other, separate from ChromaDB).

### 2. Password Handling
- Use a secure hashing library (e.g., `passlib`) to hash passwords before storing.
- Never store plain-text passwords.

### 3. API Endpoints
- **POST /api/register**: Accepts `name`, `email`, `password`. Creates a new user.
- **POST /api/login**: Accepts `email`, `password`. Returns a JWT if credentials are valid.
- **GET /api/me**: Returns current user info (requires JWT auth).

### 4. JWT Authentication
- Use a library like `pyjwt` or FastAPI's `fastapi.security` utilities.
- Issue JWTs on successful login; validate JWTs for protected endpoints.
- Store JWT secret securely (use environment variables).

### 5. Error Handling & Validation
- Validate email format and password strength.
- Handle duplicate email registration.
- Return appropriate error messages for failed login/registration.

## Frontend (Next.js)

### 1. Registration & Login Forms
- Create pages/components for registration and login.
- Request only `name`, `email`, and `password` from the user.
- Validate inputs client-side before submitting.

### 2. API Integration
- Use `fetch` or Axios to call backend endpoints (`/api/register`, `/api/login`).
- Store JWT in `localStorage` or `cookie` (prefer HttpOnly cookie for security).
- Show error messages for failed attempts.

### 3. Auth State Management
- Track login state (JWT presence/validity).
- Protect chat and other pages for authenticated users only.
- Implement logout by removing JWT from storage.

### 4. UI Feedback
- Show loading indicators and error messages.
- Redirect users after successful login/registration.

## Security Considerations
- Always hash passwords before storing.
- Use HTTPS in production.
- Store JWT secret and other sensitive config in environment variables.
- Protect sensitive endpoints with JWT authentication.

## Next Steps (JWT Implementation)
- After basic login/registration, implement JWT issuance and validation.
- Update protected routes to require JWT.
- Add user context to chat responses if needed.

## References
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- Next.js Auth Patterns: https://nextjs.org/docs/authentication
- Passlib: https://passlib.readthedocs.io/en/stable/
- PyJWT: https://pyjwt.readthedocs.io/en/stable/

---

Follow this guide to plan and implement login/registration in your project. For code structure, see `.github/copilot-instructions.md` for conventions and folder organization.
