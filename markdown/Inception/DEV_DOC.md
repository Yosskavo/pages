# Developer Documentation

This document provides developer-level instructions for building, maintaining, debugging, and extending the **Inception** infrastructure.

---

## 1. Environment Setup from Scratch

### Prerequisites
Ensure the host operating system has the following dependencies installed:
- **GNU Make** (`make`)
- **Docker Engine** (v24.0+)
- **Docker Compose Plugin** (`docker compose`)

### Initializing Environment Files & Secrets

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Yosskavo/Inception.git
   cd Inception
   ```

2. **Generate environment configuration and secrets**:
   Run the Makefile target to create `srcs/.env` and populate default secret files inside `secrets/`:
   ```bash
   make env
   ```

   This creates the following files:
   - `srcs/.env` containing non-sensitive configuration (`DOMAIN_NAME`, `MYSQL_DATABASE`, `MYSQL_USER`, `WP_ADMIN_USERNAME`, `WP_USER`, `FTP_USER`, etc.).
   - `secrets/db_root_password.txt`
   - `secrets/db_password.txt`
   - `secrets/wp_admin_password.txt`
   - `secrets/wp_client_password.txt`
   - `secrets/ftp_password.txt`

3. **Map Domain Name in `/etc/hosts`**:
   ```bash
   echo "127.0.0.1 yel-mota.42.fr" | sudo tee -a /etc/hosts
   ```

---

## 2. Building and Launching with Makefile & Docker Compose

The root `Makefile` wraps Docker Compose CLI commands with ANSI colorized progress logging for building, running, and managing the multi-container stack.

### Key Makefile Targets

| Target | Command | Description |
| :--- | :--- | :--- |
| `all` / `up` / `run` | `docker compose -f srcs/docker-compose.yml up -d --build` | Initializes host directories, builds images, and starts containers in detached mode. |
| `build` | `docker compose -f srcs/docker-compose.yml build` | Builds or rebuilds image layers without starting containers. |
| `start` | `docker compose -f srcs/docker-compose.yml start` | Starts stopped containers. |
| `restart` | `docker compose -f srcs/docker-compose.yml restart` | Restarts all active containers. |
| `stop` | `docker compose -f srcs/docker-compose.yml stop` | Gracefully stops all active containers. |
| `down` | `docker compose -f srcs/docker-compose.yml down` | Stops and removes containers and networks. |
| `logs` | `docker compose -f srcs/docker-compose.yml logs -f` | Streams live logs from all containers (Press `Ctrl+C` to exit). |
| `status` / `ps` | `docker compose -f srcs/docker-compose.yml ps` | Displays service status and container health. |
| `containers` | `docker ps -a` | Lists all active project Docker containers. |
| `images` | `docker images` | Lists all built Docker images for Inception. |
| `volumes` | `docker volume ls` | Lists all active Docker volumes. |
| `prune` | `docker system prune -af --volumes` | Removes unused Docker resources and build cache. |
| `clean` | `docker compose -f srcs/docker-compose.yml down --rmi local` | Stops containers and removes locally built images. |
| `fclean` | `make clean` + deletes volumes & `~/data/` | Complete wipe of containers, images, volumes, host data, and `.env`. |
| `re` | `make fclean && make all` | Fully rebuilds the stack from a completely clean state. |
| `help` | Interactive Makefile help menu | Displays all available Makefile commands with color highlights. |

---

## 3. Data Persistence Layout on Host

Per the project specification, data persistence is configured using **named Docker volumes with local bind options** pointing to designated directories on the host machine:

- **Host Path for MariaDB**: `/home/yosskavo/data/mariadb` $\leftrightarrow$ Mounted to `/var/lib/mysql` inside `mariadb` container.
- **Host Path for WordPress**: `/home/yosskavo/data/wordpress` $\leftrightarrow$ Mounted to `/var/www/html` inside `wordpress`, `nginx`, and `ftp` containers.
- **Host Path for Uptime Kuma**: `/home/yosskavo/data/kuma` $\leftrightarrow$ Mounted to `/app/data` inside `kuma` container.

### Host Volume Creation
Host data directories are created automatically by the `make init` target before starting containers:
```bash
mkdir -p ~/data/mariadb ~/data/wordpress ~/data/kuma
```

---

## 4. Bonus Architecture: Adminer, Redis Cache, FTP, Uptime Kuma & Static Site

### MariaDB InnoDB Configuration Tuning (`50-server.cnf`)
To allow Uptime Kuma 2.X to create large table schemas without InnoDB row size limit errors:
```ini
[mariadb]
user = mysql
datadir = /var/lib/mysql
bind-address = 0.0.0.0
innodb_strict_mode = OFF
innodb_default_row_format = DYNAMIC
```

### Adminer (Database Management Interface)
- **Container Image**: `adminer:inception` (built from `debian:12`).
- **PHP Engine**: Runs `php-fpm8.2` listening internally on port `9000`.
- **Application Script**: Downloads official Adminer `index.php` into `/var/www/html/index.php`.
- **NGINX Reverse Proxy**: NGINX routes `/adminer` requests to `adminer:9000` via FastCGI.

### Redis Cache (WordPress Object Caching)
- **Container Image**: `redis:inception` (built from `debian:12`).
- **Daemon Process**: Runs `redis-server /etc/redis/redis.conf --daemonize no` listening internally on port `6379`.
- **Configuration Directives (`redis.conf`)**: `bind 0.0.0.0`, `protected-mode no`, `maxmemory 256mb`, `maxmemory-policy allkeys-lru`.
- **WordPress Integration**: Automated Redis host configuration and plugin enabling via WP-CLI.

### FTP Server (`vsftpd` File Transfer)
- **Container Image**: `ftp:inception` (built from `debian:12`).
- **Daemon Process**: Runs `vsftpd /etc/vsftpd.conf` listening on control port `21` and passive range `21100-21110`.
- **Volume Mount**: Mounts `wordpress_data` volume to home directory `/var/www/html`.

### Uptime Kuma (Service Health Dashboard)
- **Container Image**: `kuma:inception` (built from `debian:12` with Node.js 20).
- **Daemon Process**: Runs `node server/server.js` listening on port `3001`.
- **Database Engine**: Connects across `inception` bridge network to `mariadb:3306` database `Hadono`.

### Static Website (Developer Portfolio & Showcase)
- **Container Image**: `site:inception` (built from `debian:12` with NGINX).
- **Daemon Process**: Runs `nginx -g 'daemon off;'` listening on port `8080`.
- **Content**: Serves static HTML5 portfolio (`index.html`) with Tokyo Night dark theme CSS (`style.css`).

---

## 5. Helpful Debugging & Maintenance CLI Commands

### Executing Commands inside Containers
```bash
# Open interactive shell in containers
docker compose -f srcs/docker-compose.yml exec mariadb bash
docker compose -f srcs/docker-compose.yml exec wordpress bash
docker compose -f srcs/docker-compose.yml exec nginx bash
docker compose -f srcs/docker-compose.yml exec adminer bash
docker compose -f srcs/docker-compose.yml exec redis bash
docker compose -f srcs/docker-compose.yml exec ftp bash
docker compose -f srcs/docker-compose.yml exec kuma bash
docker compose -f srcs/docker-compose.yml exec site bash
```

### Inspecting Docker Volumes & Logs
```bash
# List all Docker volumes
docker volume ls

# Stream logs for all containers
make logs

# Stream logs for a specific service
docker logs -f kuma
docker logs -f site
```
