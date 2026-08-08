# Container Isolation Mechanics: Namespaces & Cgroups

An architectural breakdown of how containers operate under the hood in modern Linux systems without full machine virtualization.

---

## 1. Containers vs Virtual Machines

Unlike hardware hypervisors (KVM, VMware) that virtualize guest kernels and virtual hardware, containers share the **host Linux kernel** and isolate user-space environments using native kernel primitives:

* **Linux Namespaces:** Control what a process can **see** (PID, Network, Mount, User, IPC, UTS).
* **Control Groups (cgroups):** Control what a process can **use** (CPU, RAM, Block I/O, Network Bandwidth).
* **chroot / pivot_root:** Isolates the root file system hierarchy.

---

## 2. Linux Namespaces Breakdown

The Linux kernel provides 6 core namespaces instantiated via the `clone()` system call with specific flags:

| Namespace | Clone Flag | Isolated Resource |
|---|---|---|
| **PID** | `CLONE_NEWPID` | Process IDs (allows PID 1 inside container) |
| **NET** | `CLONE_NEWNET` | Network devices, IP routing tables, port bindings |
| **MNT** | `CLONE_NEWNS` | Mount points and file system views |
| **IPC** | `CLONE_NEWIPC` | POSIX message queues and System V shared memory |
| **UTS** | `CLONE_NEWUTS` | Hostname and NIS domain name |
| **USER** | `CLONE_NEWUSER` | Maps container root (UID 0) to unprivileged host UID |

```c
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static int child_exec(void *arg)
{
    printf("Child process running in isolated UTS/PID namespace.\n");
    sethostname("isolated-box", 12);
    char *args[] = {"/bin/sh", NULL};
    execvp(args[0], args);
    return 0;
}

int main(void)
{
    char *stack = malloc(STACK_SIZE);
    if (!stack) {
        perror("malloc");
        return 1;
    }

    int flags = CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS | SIGCHLD;
    pid_t pid = clone(child_exec, stack + STACK_SIZE, flags, NULL);

    waitpid(pid, NULL, 0);
    free(stack);
    return 0;
}
```

---

## 3. Resource Constraints with Cgroups v2

Control groups prevent a runaway container from starving the host OS of memory or CPU cycles:

```bash
# Create a dedicated cgroup slice
mkdir /sys/fs/cgroup/webapp_group

# Restrict maximum memory to 512 MB
echo "536870912" > /sys/fs/cgroup/webapp_group/memory.max

# Attach target process PID to cgroup
echo "$TARGET_PID" > /sys/fs/cgroup/webapp_group/cgroup.procs
```

---

## Key Takeaways

1. A container is simply a standard Linux process wrapped in **Namespaces** and throttled by **Cgroups**.
2. **Inception / Docker Compose** utilizes these primitives to provide deterministic microservices architectures.
