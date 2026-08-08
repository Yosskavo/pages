# Low-Level Kernel & Operating System Concepts

A foundational research path into x86 architecture, CPU privilege rings, memory paging, and kernel-level interrupt handling.

---

## 1. Research Objectives

To gain deep, firsthand comprehension of the boundary between user-space execution and kernel-space privileges by prototyping bare-metal and low-level kernel mechanisms.

---

## 2. Core Concepts Under Exploration

1. **CPU Modes & Privilege Levels:**
   * Transitioning from Real Mode to 32-bit Protected Mode and 64-bit Long Mode.
   * Ring 0 (Kernel) vs Ring 3 (User-space) protection and Segment Selectors (GDT/IDT).
2. **Virtual Memory & Multi-Level Paging:**
   * Physical vs Virtual address translation via Page Tables (`CR3` register).
   * Page faults (`#PF`), Translation Lookaside Buffer (TLB) flushing, and memory page permissions (Read/Write/Execute).
3. **Interrupt Handling & System Call Mechanics:**
   * Interrupt Descriptor Table (IDT) configuration.
   * Hardware interrupts (IRQs) vs software interrupts (`sysenter`, `syscall`, `int 0x80`).

---

## 3. Milestones & Future Experiments

* [x] Basic x86 assembly bootloader prototype loaded into QEMU.
* [ ] Multi-stage bootloader setting up GDT and jumping to C kernel entry point.
* [ ] Implementing a bare-metal serial port driver (UART) and VGA text buffer output.
* [ ] Basic round-robin task scheduler using timer interrupts (`PIT`).
