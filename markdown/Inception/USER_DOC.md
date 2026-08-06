# User Documentation

This document provides user-level instructions for navigating, running, and managing the **Inception** infrastructure.

---

## 1. Stack Services Overview

The application stack consists of isolated Docker services running on a private bridge network:

1. **NGINX (Web Server & Reverse Proxy)**
   - Entry point into the infrastructure.
   - Listens on HTTPS port `443` using TLS v1.2 / TLS v1.3.
   - Routes web traffic to WordPress and Adminer, and serves static assets.

2. **WordPress + PHP-FPM (Application Server)**
   - Runs WordPress powered by FastCGI Process Manager (PHP 8.2).
   - Listens internally on port `9000`.
   - Handles web application logic, user sessions, and database queries.
   - Integrated with Redis Object Cache for database query caching.

3. **MariaDB (Database Server)**
   - Database engine storing WordPress tables, user data, posts, site options, and Uptime Kuma application tables.
   - Listens internally on port `3306`.
   - Stores database files persistently in named volumes bound to the host filesystem (`~/data/mariadb`).

4. **Adminer (Bonus - Database Management Interface)**
   - Web-based graphical database management tool.
   - Listens internally on port `9000` and proxied by NGINX at `/adminer`.
   - Allows inspection, editing, and querying of MariaDB tables through a web browser.

5. **Redis Cache (Bonus - In-Memory Object Store)**
   - High-performance in-memory cache server.
   - Listens internally on port `6379`.
   - Caches WordPress database queries and objects to speed up response times.

6. **FTP Server (Bonus - vsftpd File Transfer)**
   - Secure FTP server for managing WordPress files.
   - Listens on control port `21` and passive ports `21100-21110`.
   - Provides direct file access to `/var/www/html` (`wordpress_data` volume).

7. **Uptime Kuma (Bonus - Service Health Dashboard)**
   - Self-hosted monitoring dashboard.
   - Listens on port `3001`.
   - Stores application data directly in MariaDB database `Hadono`.
   - Provides real-time uptime status monitoring for all infrastructure services.

8. **Static Website (Bonus - Developer Showcase & Portfolio)**
   - Personal developer portfolio showcasing 42 projects and social profiles.
   - Listens on port `8080`.
   - Built with modern HTML5 and Tokyo Night dark theme CSS.

---

## 2. Starting and Stopping the Project

All container operations are managed via the root `Makefile` inside the repository:

### Start the infrastructure:
```bash
make run
```
*Builds images, creates volumes and network, and starts all containers in detached mode.*

### Stop the infrastructure (without deleting data):
```bash
make stop
```
*Stops running containers while preserving all persistent data.*

### Restart the infrastructure:
```bash
make restart
```

### Shut down and remove containers:
```bash
make down
```

### Full Clean (Wipe containers, images, volumes & data):
```bash
make fclean
```

---

## 3. Accessing Services & Web Interfaces

### Main WordPress Website Access
1. Ensure your host machine resolves `yel-mota.42.fr` to `127.0.0.1` in `/etc/hosts`:
   ```text
   127.0.0.1 yel-mota.42.fr
   ```
2. Open your web browser and navigate to:
   ```text
   https://yel-mota.42.fr
   ```
   *(Accept the self-signed SSL certificate warning if prompted).*

### WordPress Admin Panel Access
Access the WordPress administration panel at:
```text
https://yel-mota.42.fr/wp-login.php
```

### Static Portfolio Showcase Access
Access the developer portfolio website at:
```text
http://yel-mota.42.fr:8080
# or
http://localhost:8080
```

### Adminer Database Interface Access
Access the Adminer database management UI at:
```text
https://yel-mota.42.fr/adminer
```

#### How to Log In to Adminer:
| Field | Value to Select / Enter |
| :--- | :--- |
| **System** | **`MySQL`** (or `MariaDB`) |
| **Server** | **`mariadb`** |
| **Username** | **`Assuma`** *(or `root`)* |
| **Password** | Password from `secrets/db_password.txt` (`Huncho!@#$9876`) or `secrets/db_root_password.txt` |
| **Database** | **`Hadono`** |

### FTP Server Access (FileZilla / Terminal)
Connect to the FTP server using FileZilla or command-line FTP client:

| Connection Parameter | Value |
| :--- | :--- |
| **Host** | `127.0.0.1` (or `yel-mota.42.fr`) |
| **Port** | `21` |
| **Protocol** | `FTP` |
| **Logon Type** | `Normal` |
| **User** | `ftpuser` |
| **Password** | Password from `secrets/ftp_password.txt` (`Shikamaru@1991`) |

### Uptime Kuma Health Dashboard Access
Access the Uptime Kuma monitoring UI at:
```text
http://yel-mota.42.fr:3001
# or
http://localhost:3001
```

---

## 4. Checking Redis Object Cache Health

To verify that WordPress is successfully caching data in Redis:

```bash
docker exec -it wordpress wp redis status --allow-root --path=/var/www/html
```

*Expected Output:* `Status: Connected`

---

## 5. Locating and Managing Credentials & Secrets

Sensitive credentials are stored in local text files inside the `./secrets/` directory and environment configuration at `srcs/.env`.

### Secrets Directory (`./secrets/`)
- `secrets/db_root_password.txt` : Root password for MariaDB database.
- `secrets/db_password.txt` : Application database password for user `Assuma`.
- `secrets/wp_admin_password.txt` : WordPress Primary Administrator password (`Tobirama`).
- `secrets/wp_client_password.txt` : WordPress Secondary User password (`Danzo`).
- `secrets/ftp_password.txt` : FTP user password (`ftpuser`).

---

## 6. Checking Service Health & Logs

### Check Running Container Health:
```bash
make status
# or
docker compose -f srcs/docker-compose.yml ps
```

### View Service Logs:
```bash
make logs
# or for a specific container:
docker logs nginx
docker logs wordpress
docker logs mariadb
docker logs adminer
docker logs redis
docker logs ftp
docker logs kuma
docker logs site
```
