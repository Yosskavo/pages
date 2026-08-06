*This project has been created as part of the 42 curriculum by yel-mota.*

## Description

### Project Goal

- this project aim to teach docker and the usage of them by creating dockerfile and docker-compose.yml and learn how to use the cli docker

### What is Docker

- [Docker](https://docs.docker.com/get-started/docker-overview/) : A Docker container is a lightweight, standalone software package that contains an application and only its essential libraries and dependencies. Because a container virtualizes the operating system, it bypasses the need for a Guest OS by sharing the host machine's kernel directly. This makes containers incredibly efficient and portable—they only consume the exact resources the application actively uses, measure in megabytes rather than gigabytes, and spin up in milliseconds.

### Usage of Docker

When you want to show you  team mate your project and what you did , mostly they will not have the dependency or the same version you working in with that project, so the dockers could setup an isolated environment that will install the dependency you specified to make your app work in different environment without consuming much as virtual machine

### Virtual Machine vs Docker

- [Virtual Machine (VM)](https://www.vmware.com/topics/glossary/virtual-machine.html) : Virtual machines run on a hypervisor that virtualizes physical hardware, requiring a complete guest operating system (OS) with its own kernel, binaries, and libraries for each instance.
- [Docker Container](https://docs.docker.com/get-started/overview/#docker-architecture) : Containers virtualize at the operating system level, sharing the host machine's kernel directly while running isolated processes in user space with minimal overhead.


| Feature | Virtual Machine (VM) | Docker Container |
| :--- | :--- | :--- |
| **Virtualization Level** | Hardware-level (virtualizes physical CPU, RAM, disk via hypervisor). | OS-level (virtualizes user space, shares host OS kernel). |
| **Guest OS** | Requires a full, independent Guest OS for each VM. | No Guest OS required (shares host OS kernel). |
| **Resource Usage** | Heavy (requires gigabytes of RAM and disk storage). | Lightweight (requires megabytes of RAM and minimal disk storage). |
| **Startup Time** | Slow (takes minutes to boot the full guest OS). | Fast (starts in milliseconds to seconds). |
| **Isolation** | Hardware-level isolation (high security via hypervisor). | Process-level isolation (via Linux namespaces and cgroups). |
| **Portability** | Lower (large multi-gigabyte VM disk image files). | High (small, modular images that run identically anywhere Docker is installed). |
| **Main Use Case** | Running multi-OS environments or apps needing kernel isolation. | Microservices, modern web apps, cloud-native deployments, and dev environments. |


### Secrets vs Environment Variable

- [Secrets](https://docs.docker.com/compose/how-tos/use-secrets) : Sensitive information (such as passwords, API keys, or certificates) that must be kept secure and protected from unauthorized access or exposure in logs and process lists.
- [Environment Variable](https://docs.docker.com/compose/how-tos/environment-variables) : Key-value pairs used to pass dynamic configuration settings to an application (such as port numbers, debug modes, or hostnames) without hardcoding them into the application source code.


| Feature | Environment Variable | Secrets |
| :--- | :--- | :--- |
| **Primary Purpose** | Non-sensitive application configuration (e.g., ports, hostnames, debug flags). | Protecting confidential credentials (e.g., passwords, private keys, API tokens). |
| **Exposure Risk** | Higher risk (accessible to all container processes, visible via `ps` or `docker inspect`). | Lower risk (mounted as temporary read-only files in memory at `/run/secrets/`). |
| **Storage & Access** | Stored in process memory environment blocks and `.env` files. | Stored in dedicated secret managers or mounted temporary file systems (`tmpfs`). |
| **Main Use Case** | Customizing application behavior across different environments (dev, prod). | Safely managing credentials without exposing them in logs, images, or environment dumps. |


### Docker network vs Host Network

- [Docker Network (Bridge)](https://docs.docker.com/reference/compose-file/networks) : Creates an isolated virtual network where containers communicate securely with each other. Ports must be explicitly mapped (e.g. `80:80`) to be reached from outside.
- [Host Network](https://docs.docker.com/engine/network/drivers/host/) : Removes network isolation. The container shares the host machine's network stack directly, using the host's IP and ports without needing port mapping.


| Feature | Docker Network (Bridge) | Host Network |
| :--- | :--- | :--- |
| **Network Isolation** | Isolated (container gets its own private IP address). | None (shares the host's network namespace directly). |
| **Port Forwarding** | Required (must publish ports using `-p` or `ports:`). | Not required (ports are bound directly on the host). |
| **Container Communication** | Via container names or service aliases over private subnet. | Via host IP and localhost directly. |
| **Main Use Case** | Default choice for multi-container microservices and security. | High-performance apps requiring maximum network throughput. |


### Named volumes vs bind mounts

- [Volumes](https://docs.docker.com/engine/storage/volumes) : Volumes are persistent data stores for containers, created and managed by Docker . It created and stored in docker 
- [Mounts](https://docs.docker.com/engine/storage/bind-mounts) : maps a specific, user-defined absolute path on the host machine's file system directly to a directory inside the container. 


| Feature | Named Volumes | Bind Mounts |
| :--- | :--- | :--- |
| **Host Location** | Managed by Docker (e.g., `/var/lib/docker/volumes/<volume_name>`). | Anywhere on the host machine's file system (specified via absolute path). |
| **Management** | Fully managed via Docker CLI and API. | Managed manually by the user or OS filesystem. |
| **Initial Mount Behavior** | Populates empty volume with existing files from the container's mount path. | Obscures/hides the container's existing files; shows only host files. |
| **Portability** | High (independent of host OS file paths and directory structures). | Low (tied to the directory structure and paths of the specific host OS). |
| **Volume Drivers** | Supported (can connect to cloud providers, NFS, block storage, etc.). | Not supported (limited to the local host filesystem). |
| **Main Use Case** | Database storage, persistent production state, sharing data between containers. | Local development (real-time source code sharing), sharing host host configuration files. |


# Instructions

### dependency

Before installing this project you should check if you have this dependency first :

- [make](https://ftp.gnu.org/gnu/make/) (you can install it like this or go your package manager and install it)
- [docker](https://docs.docker.com/desktop/setup/install/linux/#supported-platforms)

### Installition

To install this project :

``` bash
# if you want to use the http
git clone https://github.com/Yosskavo/Inception.git
# if you want ssh
git clone git@github.com:yosskavo/Inception
```

### Set-up Environment

Before executing you can read this specific part [DOC_DEV.md](./DEV_DOC.md/#Setup-the-Environment) or you can run this commmand

```bash
make env

```
it will generate a default env (default values are in [secrets](./secrets) folder in this repo)

### Usage

You can run the project by this command
```bash
make run
```
and if you want more specific rules you can read this part from [DOC_DEV.md](./DEV_DOC.md/#Lunching-the-project)

# Resources

- Docker : https://docs.docker.com/
- Volume named vs bind mount : https://youtu.be/keINzeYs_lc?si=7-oi2ZBSiRNjDH6M

#### Ai usage
The Ai used for searching or explaining some variable

