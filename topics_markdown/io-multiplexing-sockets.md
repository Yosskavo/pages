# Sockets & I/O Multiplexing (select, poll, epoll)

An exploration of non-blocking networking models and building scalable HTTP/1.1 servers using asynchronous I/O multiplexing in C and C++98.

---

## 1. The Problem with Blocking I/O

In a standard multithreaded or multi-process server architecture, each client connection blocks an entire thread while waiting for network packet arrival. As concurrent connections scale to thousands (the C10K problem), thread context-switching overhead degrades CPU performance and exhausts system memory.

---

## 2. Asynchronous Multiplexing with `select()` & `poll()`

I/O Multiplexing monitors multiple file descriptors simultaneously with a single thread, unblocking only when one or more sockets become ready for reading or writing without stalling:

### Non-Blocking Socket Setup in C++:

```cpp
#include <fcntl.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

void set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}
```

### Event Monitoring Loop using `poll()`:

```cpp
#include <poll.h>
#include <vector>
#include <iostream>

void event_loop(int server_fd) {
    std::vector<struct pollfd> fds;
    struct pollfd server_poll;
    server_poll.fd = server_fd;
    server_poll.events = POLLIN;
    fds.push_back(server_poll);

    while (true) {
        int ret = poll(&fds[0], fds.size(), -1);
        if (ret < 0) break;

        for (size_t i = 0; i < fds.size(); ++i) {
            if (fds[i].revents & POLLIN) {
                if (fds[i].fd == server_fd) {
                    // Accept incoming new client connection
                    int client_fd = accept(server_fd, NULL, NULL);
                    set_nonblocking(client_fd);
                    struct pollfd client_poll;
                    client_poll.fd = client_fd;
                    client_poll.events = POLLIN;
                    fds.push_back(client_poll);
                } else {
                    // Handle client HTTP request without blocking
                    char buffer[4096];
                    ssize_t bytes = recv(fds[i].fd, buffer, sizeof(buffer), 0);
                    if (bytes <= 0) {
                        close(fds[i].fd);
                        fds.erase(fds.begin() + i);
                        --i;
                    }
                }
            }
        }
    }
}
```

---

## 3. Multiplexing Primitives Comparison

| Mechanism | Kernel Complexity | Max File Descriptors | Scalability |
|---|---|---|---|
| **`select()`** | $O(N)$ linear scan | 1024 (`FD_SETSIZE`) | Low |
| **`poll()`** | $O(N)$ linear scan | Dynamic (system memory limited) | Medium |
| **`epoll()`** (Linux) | $O(1)$ event callback | Dynamic (millions) | Very High |
| **`kqueue()`** (BSD/macOS) | $O(1)$ event filter | Dynamic (millions) | Very High |

---

## Architectural Applications:

* **webserv (1337 project):** Implements `poll()` / `select()` for non-blocking HTTP/1.1 parsing, CGI execution, and chunked transfer encoding.
* **Modern Reverse Proxies:** Nginx and HAProxy rely on `epoll()` / `kqueue()` loops for microsecond latency.
