# webserv: Custom HTTP/1.1 Web Server in C++98

An in-depth roadmap for building a fully compliant, non-blocking HTTP/1.1 web server from scratch in C++98 as part of the 1337 School curriculum.

---

## 1. Project Objectives & Architecture

The objective is to implement a robust, production-grade HTTP/1.1 server modeled after **Nginx**. The server must handle multiple concurrent client connections asynchronously without blocking the main event loop.

### Core Architectural Components:

1. **I/O Multiplexing Loop:** Using `select()`, `poll()`, or `kqueue()` to manage non-blocking socket descriptors.
2. **Nginx-style Configuration Engine:** Custom recursive descent parser for routing blocks, server names, ports, client body size limits, and error pages.
3. **HTTP/1.1 Protocol Parser:** Strict request line parsing (`GET`, `POST`, `DELETE`), header normalization, and support for chunked transfer encodings.
4. **CGI Gateway (RFC 3875):** Forking child processes to execute dynamic scripts (PHP, Python) with environmental variable binding and bidirectional pipe streaming.

---

## 2. Technical Stack & Primitives

* **Language:** C++98 (Strict standard compliance without modern C++11 features).
* **System Calls:** `socket()`, `bind()`, `listen()`, `accept()`, `poll()`, `fcntl(O_NONBLOCK)`, `fork()`, `execve()`, `pipe()`, `dup2()`.
* **State Machine:** Non-blocking request buffering and streaming response chunking to prevent memory exhaustion on large file uploads.

---

## 3. Milestone Roadmap

| Milestone | Deliverable | Status |
|---|---|---|
| **Phase 1** | Configuration parser and virtual server routing | Complete |
| **Phase 2** | Non-blocking socket listener and `poll()` event loop | In Progress |
| **Phase 3** | HTTP/1.1 request validator, multipart uploads, and error pages | In Progress |
| **Phase 4** | Full CGI execution pipeline (Python / PHP scripts) | Planned |
| **Phase 5** | Stress testing with Siege and concurrency benchmarking | Planned |
