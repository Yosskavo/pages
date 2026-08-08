# ft_transcendence: Full-Stack Multiplayer Web Platform

The final capstone project of the 1337 School common core: building a production-grade, secure, multi-tier web application centered around real-time multiplayer Pong, live chat, and microservices architecture.

---

## 1. Architectural Architecture

ft_transcendence requires strict separation of concerns across a containerized microservices stack:

* **Frontend:** Single-Page Application (SPA) with dynamic real-time canvas rendering.
* **Backend:** Asynchronous Python / Django / FastAPI or Node.js backend.
* **Real-Time Layer:** Full-duplex WebSockets for synchronized multiplayer gameplay and live notifications.
* **Database & Cache:** PostgreSQL for persistent data and Redis for ephemeral session caching and WebSocket channel broadcasting.

---

## 2. Key Modules & Security Standards

1. **OAuth2 & Two-Factor Authentication (2FA):**
   * Secure integration with the 42 API OAuth provider.
   * Time-based One-Time Password (TOTP) 2FA verification using Google Authenticator / Authy.
2. **Real-Time Multiplayer Engine:**
   * Authoritative server-side game state calculations to prevent client desynchronization or cheating.
   * Smooth 60 FPS client prediction and interpolation.
3. **Cybersecurity Hardening:**
   * Protection against CSRF, XSS, SQL Injection, and timing attacks.
   * Secure HTTPS termination and WSS (Secure WebSockets) with TLS.
