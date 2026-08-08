# Unix Processes & Signal Handling

A technical deep-dive into how Unix systems create, manage, and communicate with child processes, along with robust asynchronous signal handling patterns in C.

---

## 1. Process Lifecycle (`fork` & `execve`)

In Unix-like operating systems, process creation follows a two-stage mechanism:

1. **`fork()`**: Clones the current calling process, creating an exact replica as a child process. Both share identical address space mappings at the time of the fork (optimized using Copy-On-Write).
2. **`execve()`**: Replaces the current process image with a new executable program, initializing new stack, heap, and data segments.

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void)
{
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return EXIT_FAILURE;
    } else if (pid == 0) {
        // Child Process
        char *args[] = {"/bin/ls", "-la", NULL};
        char *envp[] = {NULL};
        execve(args[0], args, envp);
        perror("execve failed");
        exit(EXIT_FAILURE);
    } else {
        // Parent Process
        int status;
        waitpid(pid, &status, 0);
        if (WIFEXITED(status)) {
            printf("Child exited with status %d\n", WEXITSTATUS(status));
        }
    }
    return EXIT_SUCCESS;
}
```

---

## 2. Inter-Process Communication (Pipes)

Pipes provide a unidirectional byte stream between two related processes via file descriptors:

* `pipefd[0]`: Read end of the pipe.
* `pipefd[1]`: Write end of the pipe.

```c
int pipefd[2];
if (pipe(pipefd) == -1) {
    perror("pipe");
    exit(EXIT_FAILURE);
}

// Redirect standard output of writer to pipe write-end
dup2(pipefd[1], STDOUT_FILENO);
close(pipefd[0]);
close(pipefd[1]);
```

---

## 3. Asynchronous Signal Handling (`sigaction`)

Signals are software interrupts sent to a process by the kernel or other processes. Traditional `signal()` is deprecated in favor of `sigaction()` due to defined POSIX semantics and prevention of race conditions.

### Safe Signal Handler Pattern:

Because signal handlers can interrupt code at any arbitrary CPU instruction, only **async-signal-safe functions** (like `write()`, `_exit()`) or updating a `volatile sig_atomic_t` flag should be executed inside the handler:

```c
#include <signal.h>
#include <unistd.h>

volatile sig_atomic_t g_shutdown = 0;

static void handle_sigint(int sig)
{
    (void)sig;
    g_shutdown = 1;
}

int main(void)
{
    struct sigaction sa;
    sa.sa_handler = handle_sigint;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;

    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);

    while (!g_shutdown) {
        // Main event loop
        sleep(1);
    }

    const char msg[] = "Clean shutdown initiated.\n";
    write(STDOUT_FILENO, msg, sizeof(msg) - 1);
    return 0;
}
```

---

## Summary Keypoints

* Always prevent zombie processes by reaping children with `waitpid()`.
* Avoid non-reentrant functions (e.g. `printf`, `malloc`) inside signal handlers.
* Use `dup2()` to construct multi-stage command pipelines (as in shells like `minishell`).
